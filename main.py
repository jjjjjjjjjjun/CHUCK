from chains import story_chain
import json

concept = input("이야기 컨셉을 입력하세요: ")

response = story_chain.invoke({"concept": concept})
raw = response.content

try:
    data = json.loads(raw)
    print(json.dumps(data, ensure_ascii=False, indent=2))
except json.JSONDecodeError:
    print("JSON 파싱 실패")
    print(raw)
