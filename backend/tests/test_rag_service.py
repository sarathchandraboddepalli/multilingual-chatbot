from app.services.rag_service import search_schemes, get_context_for_query, seed_default_schemes


def test_search_pension_scheme():
    seed_default_schemes()
    results = search_schemes("pension elderly monthly benefit")
    assert len(results) > 0
    names = [r["name"] for r in results]
    assert any("Pension" in n for n in names)


def test_search_farmer_scheme():
    seed_default_schemes()
    results = search_schemes("farmer land financial assistance")
    assert len(results) > 0


def test_no_results_for_unknown():
    seed_default_schemes()
    results = search_schemes("xyzzy completely unknown topic zzz")
    assert len(results) == 0


def test_context_has_scheme_info():
    seed_default_schemes()
    context = get_context_for_query("pension benefits for elderly")
    assert len(context) > 0
    assert "Scheme:" in context or "pension" in context.lower() or "No specific" in context


def test_search_housing_scheme():
    seed_default_schemes()
    results = search_schemes("housing construction rural BPL house")
    assert len(results) > 0
