from utils import setup_environment, load_auth_data
setup_environment()
from notebooklm_mcp.client import NotebookLMClient

def main():
    # 1. 인증 정보 로드
    try:
        auth_data = load_auth_data()
    except Exception as e:
        print(f"에러: {e}")
        return

    cookies = auth_data.get('cookies')
    csrf_token = auth_data.get('csrf_token')
    session_id = auth_data.get('session_id')

    # 2. 클라이언트 초기화
    client = NotebookLMClient(cookies=cookies, csrf_token=csrf_token, session_id=session_id)

    # 3. 마스터 클래스 노트북 ID (학습 전용 금고)
    notebook_id = "f097cbfd-b902-40a2-b309-a7c9c1a1d769"

    # 4. 왕초보용 MCP + NotebookLM 가이드
    beginner_guide = """# [왕초보 필독] AI 에이전트 + NotebookLM (MCP) 활용 백서

## 1. 이게 대체 뭔가요? (쉽게 이해하기)
*   **AI 에이전트(Antigravity 등)**: 일을 대신 해주는 '똑똑한 비서'입니다.
*   **NotebookLM**: 방대한 자료를 기억하고 대답해주는 '천재형 요약 노트'입니다.
*   **MCP (Model Context Protocol)**: 비서(에이전트)가 요약 노트(NotebookLM)를 직접 열어보고 읽을 수 있게 해주는 **'특수 연결선'**입니다.

**결론**: 예전에는 사람이 노트를 읽고 비서에게 알려줘야 했다면, 이제는 비서가 직접 노트를 보고 "대표님, 노트 3페이지에 이런 내용이 있네요!"라고 말해줍니다.

## 2. 왜 써야 하나요? (혁신적인 장점)
- **무한 기억력**: AI 비서의 기억력 한계를 넘어서서, 수천 페이지의 자료도 NotebookLM에 넣어두면 비서가 실시간으로 찾아냅니다.
- **백전백승 정확도**: AI가 짐작해서 답변(환각)하는 게 아니라, 실제로 존재하는 '노트 지식'을 기반으로 답하므로 매우 정확합니다.
- **수동 작업 제로**: 일일이 복사해서 붙여넣을 필요 없이, 비서가 알아서 자료를 찾고 정리합니다.

## 3. 왕초보를 위한 5가지 황금 활용 아이디어 💡
1.  **나만의 AI 비서**: 매일 쏟아지는 뉴스, 업무 메일, 보고서를 NotebookLM에 던져두세요. "오늘 중요한 거 위주로 브리핑해 줘" 한마디면 끝납니다.
2.  **지식 공장 (콘텐츠 제작)**: 유튜브 영상 대본, 블로그 원고, 뉴스레터를 만들 때 관련 자료를 NotebookLM에 넣으세요. 비서가 "대표님 인사이트"와 "자료 지식"을 섞어 명품 글을 써줍니다.
3.  **학습 멘토**: 자격증 공부나 새로운 기술 공부할 때 교재를 다 넣어두세요. 비서에게 "내 실력에 맞춰서 퀴즈 10개만 내봐"라고 하면 1:1 과외가 시작됩니다.
4.  **CS/상담 자동화**: 제품 설명서와 FAQ를 넣어두면, 고객 문의가 올 때마다 비서가 노트를 확인해 완벽한 답변을 작성해 줍니다.
5.  **기획서 생성기**: 과거에 썼던 모든 기획서를 넣어두세요. "이번에 새로 들어온 프로젝트, 예전 A 프로젝트 형식을 참고해서 초안 잡아줘"라고 하면 순식간에 완성됩니다.

## 4. 바로 시작하는 법 (3단계)
1.  **자료 수집**: 내가 공부하거나 활용하고 싶은 자료를 NotebookLM에 업로드한다.
2.  **에이전트 연결**: Antigravity 같은 에이전트에게 "내 NotebookLM 프로젝트 좀 봐줘"라고 지시한다.
3.  **질문/명령**: "여기 있는 자료들 요약해서 블로그 글로 만들어줘"라고 명령한다.
"""
    
    print("왕초보용 MCP 지침서 업데이트 중...")
    client.add_text_source(notebook_id, beginner_guide, "왕초보를 위한 AI 에이전트+NotebookLM 활용 백서")

    print(f"작전 완료! 마스터 클래스 프로젝트가 더욱 풍성해졌습니다.")

if __name__ == "__main__":
    main()
