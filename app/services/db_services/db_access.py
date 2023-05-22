from dotenv import load_dotenv

load_dotenv()
import os
from pydantic import Field, BaseModel
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
import weaviate
import json

client = weaviate.Client(
    url=WEAVIATE_URL,  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(
        api_key=WEAVIATE_API_KEY
    ),  # Replace w/ your Weaviate instance API key
    additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},
)

class DBLayer(BaseModel):
    # ===== import data =====

    def get_user_id_from_line_id(self,line_user_id: str)->str:
        where_filter = {
        "path": ["line_user_id"],
        "operator": "Equal",
        "valueString": line_user_id
        }

        query_result = (
        client.query
        .get("User", "id")
        .with_where(where_filter)
        .do()
        )
        if len(query_result["data"]["Get"]["User"]) > 0:
            return query_result["data"]["Get"]["User"][0]["id"]
        else:
            
            return None

    def create_user(self,line_user_id:str)->str:
        properties = {
            "id": line_user_id,
            "profile":"profile"
        }
        client.batch.add_data_object(properties, "User")

        return client.batch.create_objects()

    def update_user_profile(user_id:str,profile:str)->str:
        properties = {
            "profile": profile
        }
        client.data_object.update(
            properties,
            class_name="User",
            uuid=user_id,
            consistency_level=weaviate.data.replication.ConsistencyLevel.ALL,  # default QUORUM
        )

        return "OK"

    def get_user_profile(user_id:str)->str:
        user = client.data_object.get(user_id)
        return user["profile"]