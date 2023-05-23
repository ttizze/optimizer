from dotenv import load_dotenv

load_dotenv()
import os
from pydantic import Field, BaseModel
from app.services.ai.ai_service import AIService
from app.services.db_services.db_access import DBLayer
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
from app.routers import linebot
import guidance


line_user_id:str ="121131e"
user_id = DBLayer().get_user_id_from_line_id(line_user_id)
print(user_id)
user_message = "お金がない"

if user_id is None:
    if user_message == "同意する":
        DBLayer().create_user(line_user_id)
        user_id = DBLayer().get_user_id_from_line_id(line_user_id)
        personal_information = linebot.get_personal_information_from_api()
        first_message = linebot.first_message(personal_information)
        profile = linebot.second_message(personal_information).text
        DBLayer().update_profile(user_id, profile)
        print(profile)
        result = linebot.search_support(profile)
        print(result.text)
        linebot.after_search_result()
    else:
        linebot.agreement_message()
else:
    line_bot_obj = linebot.update_profile(user_id, user_message)
    DBLayer().update_profile(user_id, line_bot_obj.text)
    print(line_bot_obj.text)
    result = linebot.search_support(line_bot_obj.text)
    print(result.text)
