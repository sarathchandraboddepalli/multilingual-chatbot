from typing import List, Dict, Any
import re

# In-memory scheme knowledge base (populated from DB on startup)
_scheme_index: Dict[str, Dict] = {}


def index_scheme(scheme_id: str, name: str, description: str, eligibility: str = "", benefits: str = "", documents: str = "", url: str = ""):
    text = f"{name} {description} {eligibility} {benefits}".lower()
    keywords = set(re.findall(r'\w+', text))
    _scheme_index[scheme_id] = {
        "name": name,
        "description": description,
        "eligibility": eligibility,
        "benefits": benefits,
        "documents_required": documents,
        "application_url": url,
        "keywords": keywords,
        "text": text,
    }


def search_schemes(query: str, top_k: int = 3) -> List[Dict]:
    if not _scheme_index:
        seed_default_schemes()

    query_words = set(re.findall(r'\w+', query.lower()))
    scored = []
    for scheme_id, scheme in _scheme_index.items():
        overlap = len(query_words & scheme["keywords"])
        if overlap > 0:
            scored.append((overlap, scheme_id, scheme))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [{"scheme_id": sid, **s} for _, sid, s in scored[:top_k]]


def seed_default_schemes():
    """Seed with common AP government schemes for demo."""
    default_schemes = [
        {
            "scheme_id": "YSR-PENSION",
            "name": "YSR Pension Kanuka",
            "description": "Monthly pension for elderly, disabled, widows, and weavers in Andhra Pradesh",
            "eligibility": "Age above 65 for old age pension. Disability certificate required for disabled persons. For widows, death certificate of husband required.",
            "benefits": "Rs 2750 per month for old age, Rs 3000 for disabled persons, Rs 2750 for widows",
            "documents": "Aadhaar card, bank account, age proof, caste certificate if applicable",
            "url": "https://www.apcivilsupplies.gov.in",
        },
        {
            "scheme_id": "YSR-RYTHU-BHAROSA",
            "name": "YSR Rythu Bharosa",
            "description": "Financial assistance of Rs 13,500 per year to farmer families in Andhra Pradesh",
            "eligibility": "Farmers who own land or are tenant farmers in Andhra Pradesh. Should have valid Rythu Bharosa Card.",
            "benefits": "Rs 13,500 per year per farmer family in three installments",
            "documents": "Aadhaar card, land documents or tenant agreement, bank account linked to Aadhaar",
            "url": "https://www.apagriportal.gov.in",
        },
        {
            "scheme_id": "YSR-AAROGYASRI",
            "name": "YSR Aarogyasri",
            "description": "Free health insurance up to Rs 5 lakh per year for BPL families in Andhra Pradesh",
            "eligibility": "Below Poverty Line (BPL) families in Andhra Pradesh with Aarogyasri card",
            "benefits": "Free treatment up to Rs 5 lakh per year at empanelled hospitals for 2449 procedures",
            "documents": "Aarogyasri card, Aadhaar, ration card",
            "url": "https://www.aarogyasri.ap.gov.in",
        },
        {
            "scheme_id": "PM-KISAN",
            "name": "PM Kisan Samman Nidhi",
            "description": "Rs 6000 per year financial support to small and marginal farmers across India",
            "eligibility": "Farmers with less than 2 hectares of land. Family includes husband, wife and minor children.",
            "benefits": "Rs 6000 per year in three equal installments of Rs 2000 each",
            "documents": "Aadhaar, bank account, land records",
            "url": "https://pmkisan.gov.in",
        },
        {
            "scheme_id": "PMAY-GRAMIN",
            "name": "Pradhan Mantri Awas Yojana Gramin",
            "description": "Financial assistance for construction of houses for rural BPL families",
            "eligibility": "BPL families in rural areas who are houseless or living in kutcha houses",
            "benefits": "Rs 1.20 lakh in plains and Rs 1.30 lakh in hilly areas for house construction",
            "documents": "Aadhaar, SECC 2011 inclusion, bank account",
            "url": "https://pmayg.nic.in",
        },
    ]
    for s in default_schemes:
        index_scheme(
            s["scheme_id"],
            s["name"],
            s["description"],
            s.get("eligibility", ""),
            s.get("benefits", ""),
            s.get("documents", ""),
            s.get("url", ""),
        )


def get_context_for_query(query: str) -> str:
    schemes = search_schemes(query)
    if not schemes:
        return "No specific government scheme information found for this query."

    context_parts = []
    for s in schemes:
        context_parts.append(f"""
Scheme: {s['name']}
Description: {s['description']}
Eligibility: {s.get('eligibility', 'N/A')}
Benefits: {s.get('benefits', 'N/A')}
Documents Required: {s.get('documents_required', 'N/A')}
Application URL: {s.get('application_url', 'N/A')}
""")
    return "\n---\n".join(context_parts)
