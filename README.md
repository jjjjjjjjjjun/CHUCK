# AI 동화 생성 시스템 (LangChain + Gemini)

본 프로젝트는 LangChain과 Google Gemini API를 활용하여
사용자가 입력한 컨셉을 기반으로 기승전결 구조를 갖춘 7문장의 동화형 문학 작품을 실시간 생성하는 웹 기반 인공지능 시스템입니다

교내 축제 전시를 목적으로 설계되었으며,
관람객이 직접 컨셉을 입력하고 AI가 생성한 문학 작품을 웹 UI를 통해 즉시 확인할 수 있도록 구성되어 있습니다

### 시스템 개요

##### 입력

사용자가 입력한 이야기 컨셉 문자열

#### 출력

기·승·전·결 구조 요약

정확히 7개의 문장으로 구성된 동화형 문학 작품

JSON 형식으로 구조화된 결과
### 작동 프롬프트
server.py 실행하면 메인 자동실행됨됨


### 파일별 기능 설명
#### server.py

Flask 기반 웹 서버

/ 경로에서 HTML 페이지 렌더링

/generate 경로에서 문학 작품 생성 API 제공

Gemini 응답에서 코드블록 제거 후 JSON 파싱 처리

#### chains.py

LangChain을 이용한 LLM 호출 로직

Gemini 모델과 프롬프트를 결합하여 story_chain 생성

서버에서 직접 호출되는 핵심 AI 처리 모듈

주요 객체

story_chain : 컨셉 입력 → 문학 작품 JSON 출력

#### prompts.py

AI에게 전달되는 문학 생성용 프롬프트 정의

기승전결 구조, 문장 수, 문체, 출력 형식(JSON)을 엄격히 제한

출력 일관성 및 파싱 안정성을 확보하기 위한 설계

주요 변수

LITERARY_UNIFIED_PROMPT

#### config.py

Gemini API Key 관리 파일

templates/index.html

사용자 컨셉 입력 UI

Flask 서버의 /generate API 호출

반환된 JSON 결과를 화면에 출력

주요 변수 및 로직 설명

concept

사용자가 입력하는 이야기 주제 문자열

story_chain.invoke({"concept": concept})

LangChain을 통한 Gemini API 호출

입력된 컨셉을 프롬프트에 삽입하여 문학 작품 생성

JSON 문자열 형태의 결과 반환

JSON 출력 형식
{
  "structure": {
    "기": "도입 요약",
    "승": "전개 요약",
    "전": "갈등 요약",
    "결": "마무리 요약"
  },
  "story": [
    "문장 1",
    "문장 2",
    "문장 3",
    "문장 4",
    "문장 5",
    "문장 6",
    "문장 7"
  ]
}

실행 방법

가상환경 생성 및 활성화

라이브러리 설치

config.py, .env 파일은 반드시 .gitignore에 포함한다

기술 스택

Python 3.10

Flask

LangChain

Google Gemini API

HTML / CSS / JavaScript
# ascii_art
