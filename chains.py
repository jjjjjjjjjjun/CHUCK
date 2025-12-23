from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import LITERARY_UNIFIED_PROMPT
from config import configure_next_key


literary_prompt = PromptTemplate(
    input_variables=["concept"],
    template=LITERARY_UNIFIED_PROMPT
)


def invoke_story_chain(concept: str):
    """
    API 접근 거부 시 다음 키로 자동 전환
    """
    last_error = None

    for _ in range(5):  # 키 개수만큼 시도 (필요시 len(api_keys))
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.8,
                google_api_key=configure_next_key()
            )

            chain = literary_prompt | llm
            return chain.invoke({"concept": concept})

        except Exception as e:
            last_error = e
            print(f"[WARN] Gemini Key 실패 → 다음 키 시도: {e}")
            continue

    raise RuntimeError("모든 Gemini API Key 접근 실패") from last_error
