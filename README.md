# CHUCK — AI 동화 생성기

컨셉 한 줄을 입력하면 **기승전결 구조를 갖춘 7문장의 동화**를 생성하는 웹 서비스입니다.
교내 축제 전시를 위해 제작했으며, 관람객이 직접 주제를 입력하고 결과를 그 자리에서 확인할 수 있습니다.

생성된 이야기는 작성자 이름과 함께 Firestore에 저장되어 기록으로 남습니다.

---

## 만들면서 고민한 것

### 출력이 매번 달라지면 화면에 띄울 수 없다

생성형 AI의 결과를 그대로 웹에 표시하려면, **형식이 항상 같아야 합니다.** 어떤 때는 5문장, 어떤 때는 앞에 설명이 붙는다면 파싱이 깨지고 화면이 무너집니다.

그래서 프롬프트에 제약을 명시했습니다.

- 정확히 **7문장**
- **기·승·전·결** 구조 필수
- 지정된 **JSON 스키마**로만 출력
- 분석 과정이나 설명 문구 금지
- 폭력적·선정적 표현 금지 (전시 대상이 청소년을 포함)

### 그래도 형식이 어긋날 때가 있다

LLM은 지시를 받아도 응답을 ```` ```json ```` 코드블록으로 감싸거나 앞뒤에 문장을 덧붙이곤 합니다.
프롬프트만 믿지 않고, 서버에서 한 번 더 정제합니다.

```python
def extract_json(raw: str) -> str:
    raw = re.sub(r"^```json\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    match = re.search(r"\{[\s\S]*\}", raw)   # 중괄호 구간만 추출
    return match.group(0) if match else raw
```

### 전시 중에 멈추면 안 된다

관람객이 몰리면 API 호출이 집중되어 쿼터 초과나 일시적 거부가 발생합니다. 전시 도중 서비스가 멈추면 복구할 시간이 없습니다.

여러 개의 API 키를 `itertools.cycle`로 순환시키고, 호출이 실패하면 **다음 키로 자동 전환해 최대 5회까지 재시도**하도록 했습니다.

```python
for _ in range(5):
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.8,
            google_api_key=configure_next_key()   # 순환 키
        )
        chain = literary_prompt | llm
        return chain.invoke({"concept": concept})
    except Exception as e:
        continue   # 다음 키로
```

### 창작에는 다양성이 필요하다

`temperature`를 **0.8**로 설정했습니다. 같은 컨셉을 입력해도 매번 다른 이야기가 나와야, 관람객이 여러 번 시도해볼 이유가 생깁니다. 형식은 프롬프트로 고정하되 내용은 자유롭게 두는 구성입니다.

---

## 동작 흐름

```
[웹 UI]  이름 + 컨셉 입력
    │  POST /generate
    ▼
[Flask]  입력 검증 (빈 값이면 400)
    │
    ▼
[LangChain]  PromptTemplate | Gemini 2.5 Flash
    │         (키 순환 재시도)
    ▼
[Flask]  코드블록 제거 → JSON 파싱
    │
    ├──▶ [Firestore]  이름·컨셉·이야기·시각 저장
    └──▶ [웹 UI]  기승전결 요약 + 7문장 표시
```

---

## API

### `POST /generate`

**요청**

```json
{
  "name": "관람객 이름",
  "concept": "달을 사랑한 고양이"
}
```

**응답**

```json
{
  "structure": {
    "기": "도입 요약",
    "승": "전개 요약",
    "전": "갈등 요약",
    "결": "마무리 요약"
  },
  "story": ["문장 1", "문장 2", "문장 3", "문장 4", "문장 5", "문장 6", "문장 7"]
}
```

**오류 응답**

| 상태 | 상황 |
|------|------|
| `400` | `name` 또는 `concept`가 비어 있음 |
| `500` | JSON 파싱 실패 (원본 응답을 `raw`에 포함해 반환) |
| `500` | 모든 API 키 실패 등 서버 오류 |

---

## 파일 구성

| 파일 | 역할 |
|------|------|
| `main.py` | Flask 서버, 라우팅, JSON 정제, Firestore 저장 호출 |
| `chains.py` | LangChain 체인 구성, API 키 순환 재시도 |
| `prompt.py` | 생성 규칙과 출력 형식을 정의한 프롬프트 |
| `config.py` | 환경변수에서 여러 API 키를 읽어 순환 공급 |
| `firebase.py` | Firestore에 생성 결과 저장 |
| `templates/index.html` | 입력 UI 및 결과 표시 |

---

## 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| 언어 | Python 3.10 |
| 서버 | Flask 3.0 |
| 체인 | LangChain 0.2, langchain-google-genai |
| 모델 | Google Gemini 2.5 Flash (temperature 0.8) |
| 저장 | Firebase Firestore |
| 프론트 | HTML / CSS / JavaScript |

---

## 실행 방법

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install firebase-admin
```

**환경 설정**

`.env` 파일에 API 키를 쉼표로 구분해 넣습니다. 키가 여러 개일수록 전시 중 안정성이 올라갑니다.

```
GEMINI_API_KEYS=키1,키2,키3
```

Firebase 서비스 계정 키(`firebase-key.json`)를 프로젝트 루트에 둡니다.

> `.env`와 `firebase-key.json`은 반드시 `.gitignore`에 포함해야 합니다.

```bash
python main.py
# http://127.0.0.1:5000
```

---

## 개선 아이디어

- **키 순환의 한계** — 현재는 실패 시 즉시 다음 키로 넘어갑니다. 지수 백오프를 넣으면 일시적 오류에 더 잘 대응할 수 있습니다.
- **생성 이력 조회** — Firestore에 쌓인 이야기를 열람하는 화면이 없습니다. 전시 후 결과를 모아 보여주면 활용도가 높아집니다.
- **스트리밍 출력** — 생성이 끝날 때까지 기다려야 합니다. 토큰 단위로 흘려보내면 체감 대기 시간이 줄어듭니다.
- **입력 필터링** — 부적절한 컨셉 입력에 대한 사전 검증이 프롬프트 지시에만 의존하고 있습니다.
