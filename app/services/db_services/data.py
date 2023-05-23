from dotenv import load_dotenv

load_dotenv()

from supabase import create_client, Client

from langchain.embeddings import OpenAIEmbeddings
import os
import openai
from datetime import datetime
import requests
import httpx
import pytz
import traceback
import requests
import json
import csv
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
supabaseurl = os.getenv("SUPABASE_URL")
supabasekey = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabaseurl, supabasekey)


embedding_model = OpenAIEmbeddings()
with open("supportsSummarized.csv", 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        query_embedding = embedding_model.embed_query(row["generatedSummary"])
        data = {
            "title":row["title"],
            "content":row["generatedSummary"],
            "embed" :query_embedding
        }
        result = supabase.table("supports").insert(data).execute()