import google.generativeai as genai
from config import configure_next_key, api_keys

def generate_text(prompt: str) -> str:
    last_error = None

    for _ in range(len(api_keys)):
        key = configure_next_key()
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            last_error = e
            print(f"[WARN] API KEY 실패 → 다음 키로 전환: {e}")
            continue

    raise RuntimeError("모든 Gemini API Key 접근이 거부되었습니다.") from last_error
