import os
from dotenv import load_dotenv
import google.generativeai as genai
from itertools import cycle

load_dotenv()

# 여러 API Key 로드
keys = os.getenv("GEMINI_API_KEYS")
if not keys:
    raise ValueError("GEMINI_API_KEYS가 설정되지 않았습니다.")

api_keys = [k.strip() for k in keys.split(",")]
key_cycle = cycle(api_keys)


def configure_next_key():
    key = next(key_cycle)
    genai.configure(api_key=key)
    return key
