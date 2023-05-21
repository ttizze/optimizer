import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, Header, Request, Response
from fastapi.responses import FileResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from starlette.exceptions import HTTPException
from supabase import create_client, Client
from starlette.middleware.cors import CORSMiddleware
from app.routers import linebot
from pydantic import BaseModel
import json
import requests
from typing import Optional
# FastAPIのインスタンス作成
app = FastAPI(title="linebot-sample", description="This is sample of LINE Bot.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
supabaseurl = os.getenv("SUPABASE_URL")
supabasekey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabaseurl, supabasekey)
# LINE Botに関するインスタンス作成
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

@app.get("/")
def root():
    """
    ルートにアクセスした際の処理です。APIの情報を返します。
    """

    return {"title": app.title, "description": app.description}

@app.post(
    "/callback",
    summary="LINE Message APIからのコールバックです。",
    description="ユーザーからメッセージが送信された際、LINE Message APIからこちらのメソッドが呼び出されます。",
)
async def callback(request: Request, x_line_signature=Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return "OK"


