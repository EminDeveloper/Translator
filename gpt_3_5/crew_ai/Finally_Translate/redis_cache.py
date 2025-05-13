import redis
import os
from dotenv import load_dotenv

load_dotenv()  # 👈 Add this at the top

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASS"),
    decode_responses=True,
    ssl=True
)
