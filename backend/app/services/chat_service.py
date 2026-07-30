import anthropic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.message import ChatRequest, ChatResponse
from app.services.rag_service import get_context_for_query, search_schemes
from app.services.translation_service import detect_language, translate_text
from app.config import settings
import uuid

SYSTEM_PROMPT = """You are a helpful government services assistant for Andhra Pradesh and India.
You help citizens understand government schemes, check eligibility, and learn how to apply.
Be concise, friendly, and factual. Always cite the scheme name when discussing specific schemes.
If you don't know something, say so clearly and suggest where to find the information.
Respond in the same language the user writes in."""


async def process_chat(db: AsyncSession, request: ChatRequest) -> ChatResponse:
    detected_lang = await detect_language(request.message)
    # Use the caller-supplied language if explicitly non-English; otherwise auto-detect.
    # "en" is treated as the default/unspecified sentinel — callers wanting forced English
    # should rely on detect_language returning "en" for English text anyway.
    language = detected_lang if request.language == "en" else request.language

    query_in_english = request.message
    if language != "en":
        query_in_english = await translate_text(request.message, language, "en")

    if request.conversation_id:
        result = await db.execute(select(Conversation).where(Conversation.id == request.conversation_id))
        conversation = result.scalar_one_or_none()
    else:
        conversation = None

    if not conversation:
        conversation = Conversation(channel="web", language=language)
        db.add(conversation)
        await db.flush()

    context = get_context_for_query(query_in_english)
    schemes = search_schemes(query_in_english, top_k=1)
    scheme_referenced = schemes[0]["name"] if schemes else None

    history_result = await db.execute(
        select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at).limit(10)
    )
    history = list(history_result.scalars().all())

    messages_for_api = []
    for msg in history:
        messages_for_api.append({"role": msg.role, "content": msg.content})

    user_content = f"""User query: {request.message}

Relevant scheme information:
{context}

Please answer the user's question based on the scheme information above."""

    messages_for_api.append({"role": "user", "content": user_content})

    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-haiku-4-5-20250514",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages_for_api,
        )
        assistant_reply = response.content[0].text
    except Exception:
        assistant_reply = f"I found information about: {scheme_referenced or 'government schemes'}. {context[:300] if context else 'Please contact your local government office for more details.'}"

    if language != "en":
        localized_reply = await translate_text(assistant_reply, "en", language)
    else:
        localized_reply = assistant_reply

    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
        language=language,
    )
    db.add(user_msg)

    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=localized_reply,
        original_content=assistant_reply,
        language=language,
        scheme_referenced=scheme_referenced,
        confidence_score=0.85 if schemes else 0.4,
    )
    db.add(assistant_msg)
    await db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        response=localized_reply,
        language=language,
        scheme_referenced=scheme_referenced,
        confidence_score=0.85 if schemes else 0.4,
    )
