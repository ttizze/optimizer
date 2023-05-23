import os
from fastapi import FastAPI, Header, Request, Response
from fastapi.responses import FileResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from app.routers import linebot
from pydantic import BaseModel
import json
import requests
from typing import Optional
from app.services.db_services.db_access import DBLayer
# FastAPIのインスタンス作成
app = FastAPI(title="linebot-sample", description="This is sample of LINE Bot.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    handler.handle(body.decode("utf-8"), x_line_signature)
    return "OK"


# @app.get(
#     "/auth_my_info_api",
#     summary="自己情報提供API認証のモック",
#     description="とりあえずクリックしたらLINE返信",
# )
# def auth_my_info_api(request: Request, x_line_signature=Header(None)):
#     body = request.body()
#     try:
#         handler.handle(body.decode("utf-8"), x_line_signature)
#     except InvalidSignatureError:
#         raise HTTPException(status_code=400, detail="InvalidSignatureError")
#     return "OK"



@handler.add(MessageEvent)
def handle_message(event):
    """
    LINE Messaging APIのハンドラより呼び出される処理です。
    受け取ったメッセージに従い返信メッセージを返却します。

    Parameters
    ----------
    event : MessageEvent
        送信されたメッセージの情報です。
    """
    line_user_id:str = event.source.user_id
    user_id = DBLayer().get_user_id_from_line_id(line_user_id)
    user_message = event.message.text
    #新規ユーザーの場合
    if user_id is None:
        if user_message == "同意する":
            DBLayer().create_user(line_user_id)
            user_id = DBLayer().get_user_id_from_line_id(line_user_id)
            personal_information = linebot.get_personal_information_from_api()
            messages = []
            first_message = linebot.first_message(personal_information)
            messages.append(first_message)
            profile = linebot.second_message(personal_information)
            messages.append(profile)
            DBLayer().update_profile(user_id, profile.text)
            result = linebot.search_support(profile.text)
            after_search_result = linebot.after_search_result()
            messages.append(after_search_result)
            line_bot_api.reply_message(event.reply_token, messages)
        else:
            line_bot_api.reply_message(event.reply_token, linebot.agreement_message())
    else:
        messages = []
        line_bot_obj = linebot.update_profile(user_id, user_message)
        messages.append(line_bot_obj)
        DBLayer().update_profile(user_id, line_bot_obj.text)
        result = linebot.search_support(line_bot_obj.text)
        print(result)
        messages.append(str(result))
        after_search_result = linebot.after_search_result()
        messages.append(after_search_result)
        line_bot_api.reply_message(event.reply_token, messages)


