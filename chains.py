from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import LITERARY_UNIFIED_PROMPT
import config


# Gemini LLM 초기화
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   # 안정성 최우선
    temperature=0.8,
    google_api_key=config.GEMINI_API_KEY
)

# PromptTemplate
literary_prompt = PromptTemplate(
    input_variables=["concept"],
    template=LITERARY_UNIFIED_PROMPT
)

# Runnable Chain (LangChain 1.x 권장)
story_chain = literary_prompt | llm
