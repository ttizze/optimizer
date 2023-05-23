import os
import traceback
import pytz
from datetime import datetime
from typing import Any, Dict, List, Union
from pydantic import BaseModel

from linebot.models import (
    BoxComponent,
    BubbleContainer,
    FlexSendMessage,
    ImageComponent,
    TextComponent,
    TextSendMessage,
    URIAction,
)

from ..services.db_services.db_access import DBLayer
from ..services.ai.ai_service import AIService


def handle_user_message(
    user_id: int, message: str
) -> Union[TextSendMessage, FlexSendMessage]:
    response = AIService().get_response(message)
    return TextSendMessage(text=response)

def agreement_message() -> TextSendMessage:
    response = "同意いただけない場合、本サービスはご利用いただけません。"
    return TextSendMessage(text=response)


def get_personal_information_from_api() -> str:
    return """
    特定個人情報等
        地方税法その他の地方税に関する法律に基づく条例の規定により算定した税額若しくはその算定の基礎となる事項に関する情報

        項目名,内容
        個人住民税情報,
        課税年度,2022
        総所得金額等,0円
        合計所得金額,0円
        合計所得金額情報,
        総所得金額,0円
        総所得金額情報,
        給与所得額,0円
        給与所得額情報,
        給与収入額,0円
        給与専従者収入額,0円
        特定支出の額,0円
        所得金額調整控除額,0円
        雑所得額（総合）,0円
        雑所得額（総合）情報,
        公的年金等所得額,0円
        公的年金等収入額,0円
        公的年金等以外雑所得額（総合課税）,0円
        事業所得額,0円
        事業所得額情報,
        営業等所得額,0円
        農業所得額,0円
        特例肉用牛所得額,0円
        不動産所得額,0円
        利子所得額（総合）,0円
        配当所得額（総合）,0円
        譲渡所得額（総合）,0円
        譲渡所得額（総合）情報,
        長期譲渡所得額（特別控除前）,0円
        特別控除額（長期譲渡所得）,0円
        短期譲渡所得額（特別控除前）,0円
        特別控除額（短期譲渡所得）,0円
        一時所得額（総合）,0円
        山林所得額,0円
        退職所得額（総合）,0円
        譲渡所得額（申告分離）,0円
        譲渡所得額（申告分離）情報,
        長期譲渡所得額（特別控除前）,0円
        特別控除額（長期譲渡所得）,0円
        長期一般所得額（特別控除前）,0円
        特別控除額（長期一般所得）,0円
        長期特定所得額,0円
        長期軽課所得額（特別控除前）,0円
        特別控除額（長期軽課所得）,0円
        短期譲渡所得額（特別控除前）,0円
        特別控除額（短期譲渡所得）,0円
        短期一般所得額（特別控除前）,0円
        特別控除額（短期一般所得）,0円
        短期軽減所得額（特別控除前）,0円
        特別控除額（短期軽減所得）,0円
        株式等譲渡所得額（申告分離）,0円
        株式等譲渡所得額（申告分離）情報,
        一般株式等譲渡所得額,0円
        上場株式等譲渡所得額,0円
        上場株式等配当等所得額（申告分離）,0円
        先物取引雑所得額（申告分離）,0円
        条約適用利子等の額,0円
        条約適用配当等の額,0円
        特例適用利子等の額,0円
        特例適用配当等の額,0円
        繰越控除額,0円
        繰越控除額情報,
        純損失繰越控除額,0円
        居住用財産譲渡損失繰越控除額,0円
        特定居住用財産譲渡損失繰越控除額,0円
        上場株式等譲渡損失繰越控除額,0円
        特定株式等譲渡損失繰越控除額,0円
        先物取引差金等決済損失繰越控除額,0円
        雑損失繰越控除額,0円
        雑損控除額,0円
        医療費控除額,0円
        小規模共済等掛金控除額,0円
        社会保険料控除額,0円
        生命保険料控除額,0円
        地震保険料控除額,0円
        配偶者特別控除額,0円
        配偶者控除等,配偶者控除等無し
        扶養控除,0円
        扶養控除情報,
        一般,0
        特定,0
        老人,0
        同老,0
        １６歳未満扶養者数,0
        障害者控除,0円
        障害者控除情報,
        普障,0
        特障,0
        同特,0
        本人該当区分,
        同一生計配偶者,非該当
        控除対象障害者,非該当
        控除対象寡婦・ひとり親,非該当
        控除対象勤労学生,非該当
        扶養控除対象,非該当
        １６歳未満扶養親族,非該当
        専従者控除額,0円
        所得控除合計額,0円
        課税所得額（課税標準額）,0円
        市町村民税＿税額控除前所得割額,0円
        市町村民税＿調整控除額,0円
        市町村民税＿調整額,0円
        市町村民税＿住宅借入金等特別税額控除額,0円
        市町村民税＿寄附金税額控除額,0円
        市町村民税＿外国税控除額,0円
        市町村民税＿配当控除額,0円
        市町村民税＿配当割額又は株式等譲渡所得割額の控除額,0円
        市町村民税所得割額,0円
        市町村民税均等割額,0円
        都道府県民税所得割額,0円
        都道府県民税均等割額,0円
        居住用損失額,0円
        市町村民税所得割額（減免前）,0円
        市町村民税均等割額（減免前）,0円
        減免税額,0円
        所得税確定申告書の提出の有無,提出無し
        住民税申告書の提出の有無,提出無し
        住民登録外課税の有無,非該当

        行政機関等
        行政機関等,東京都台東区
    """

def first_message(personal_information:str) -> TextSendMessage:
    response = f"""
    現在、あなたの個人情報を基に、OPTIMIZERがあなたの状況を推測しています。

    下記があなたの個人情報です。

    {personal_information}

        """
    return TextSendMessage(text=response)

def second_message(personal_information:str) ->TextSendMessage:
    profile = AIService().profile_from_personal_information(personal_information)
    return TextSendMessage(text=profile)

def search_support(profile:str) -> TextSendMessage:
    result = DBLayer().search_support(profile)
    return TextSendMessage(text=result)

def after_search_result() -> TextSendMessage:
    response = """
    あなたの現在の状況に対して、以上の支援が受けられそうです。他に何かお困りのことはありますか？
    """
    return TextSendMessage(text=response)

def update_profile(user_id:int,message:str) -> TextSendMessage:
    profile = DBLayer().get_profile(user_id)
    response = AIService().update_profile(profile,message)
    return TextSendMessage(text=response)
