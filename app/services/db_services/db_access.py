from dotenv import load_dotenv

load_dotenv()
import os
from pydantic import Field, BaseModel
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

import json

