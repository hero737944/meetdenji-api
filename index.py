from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

class ContactForm(BaseModel):
    telegram_username: str
    why_meet_denji: str

@app.get("/")
def root():
    return {"status": "Denji Contact API is running 🔥"}

@app.post("/contact")
async def contact(form: ContactForm):
    message = (
        f"📬 New Meet Request!\n\n"
        f"👤 Telegram: @{form.telegram_username}\n"
        f"💬 Why they want to meet Denji:\n{form.why_meet_denji}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={
            "chat_id": CHAT_ID,
            "text": message
        })

    if response.status_code == 200:
        return {"success": True, "message": "Request sent to Denji! 🚀"}
    else:
        return {"success": False, "message": "Something went wrong. Try again."}
