from flask import Flask, request, jsonify, render_template
from chains import story_chain
import json
import re

app = Flask(__name__)


# ---------------------------
# JSON 코드블록 정제 함수
# ---------------------------
def extract_json(raw: str) -> str:
    """
    LLM 출력에서 ```json ``` 코드블록 및 불필요한 텍스트 제거
    """
    if not raw:
        return ""

    # ```json ... ``` 또는 ``` ... ``` 제거
    raw = raw.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    # 혹시 앞뒤에 설명이 붙은 경우 JSON만 추출
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        return match.group(0)

    return raw


# ---------------------------
# HTML 페이지
# ---------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------
# 이야기 생성 API
# ---------------------------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(force=True)
        concept = data.get("concept", "").strip()

        if not concept:
            return jsonify({"error": "concept가 비어 있습니다"}), 400

        # LangChain 호출
        response = story_chain.invoke({"concept": concept})
        raw = response.content

        # JSON 정제
        clean = extract_json(raw)

        # JSON 파싱
        parsed = json.loads(clean)

        return jsonify(parsed)

    except json.JSONDecodeError as e:
        return jsonify({
            "error": "JSON 파싱 실패",
            "detail": str(e),
            "raw": clean
        }), 500

    except Exception as e:
        return jsonify({
            "error": "서버 오류",
            "detail": str(e)
        }), 500


# ---------------------------
# 서버 실행
# ---------------------------
if __name__ == "__main__":
    print("✅ LangChain + Gemini 서버 실행 중...")
    print("🌐 http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
