import hmac
import hashlib
import json
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings
from app.schemas.message import ChatRequest
from app.services.chat_service import process_chat

router = APIRouter()


@router.get("/whatsapp")
async def verify_webhook(
    hub_mode: str | None = None,
    hub_challenge: str | None = None,
    hub_verify_token: str | None = None,
):
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        if hub_challenge is None:
            return 0
        try:
            return int(hub_challenge)
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid challenge")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def receive_whatsapp_message(request: Request, db: AsyncSession = Depends(get_db)):
    raw_body = await request.body()

    # Verify HMAC-SHA256 signature from Meta/WhatsApp
    signature_header = request.headers.get("X-Hub-Signature-256", "")
    expected_sig = "sha256=" + hmac.new(
        settings.WHATSAPP_VERIFY_TOKEN.encode(), raw_body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected_sig, signature_header):
        raise HTTPException(status_code=403, detail="Invalid signature")

    body = json.loads(raw_body)
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "ok"}

        msg = messages[0]
        from_number = msg.get("from", "")
        msg_text = msg.get("text", {}).get("body", "")

        if not msg_text:
            return {"status": "ok"}

        chat_req = ChatRequest(message=msg_text, language="en")
        result = await process_chat(db, chat_req)

        return {"status": "ok", "response_preview": result.response[:100]}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "detail": str(e)}
