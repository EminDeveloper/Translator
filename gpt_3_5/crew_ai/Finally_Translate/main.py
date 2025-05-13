from fastapi import FastAPI, HTTPException
import json

from db import search_word, insert_word_to_db
from redis_cache import redis_client
from gpt_translator import translate_with_crewai

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/translate")
def translate(word: str):
    key = f"word:{word.lower()}"

    # 1. Redis
    try:
        cached = redis_client.get(key)
        if cached:
            return {
                "source": "redis",
                "data": json.loads(cached)
            }
    except Exception as e:
        print("⚠️ Redis error:", e)

    # 2. MySQL
    db_result = search_word(word)
    if db_result:
        try:
            redis_client.set(key, json.dumps(db_result), ex=2592000)
        except:
            pass
        return {
            "source": "mysql",
            "data": db_result
        }

    # 3. GPT
    gpt_response = translate_with_crewai(word)
    try:
        data = json.loads(gpt_response)
        insert_word_to_db(gpt_response)
        try:
            redis_client.set(key, json.dumps(data), ex=2592000)
        except:
            pass
        return {
            "source": "gpt",
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPT Error: {e}")
