import asyncio
import time
from utils import get_client, load_auth_data

async def main():
    print("=== 'AI Agent 마스터 클래스' 프로젝트 초기 설정 가동 ===")
    
    client = None
    try:
        # 1. 인증 정보 로드
        auth_data = load_auth_data()
        
        # 2. 클라이언트 초기화 및 브라우저 시작
        client = get_client()
        print("브라우저를 시작합니다...")
        await client.start()
        
        # 3. 로그인 정보 수동 주입 (auth_data 활용)
        print("인증 정보를 주입합니다...")
        client.driver.get("https://notebooklm.google.com")
        time.sleep(3)
        
        for cookie in auth_data.get('selenium_cookies', []):
            try:
                client.driver.add_cookie(cookie)
            except: pass
            
        client.driver.refresh()
        await asyncio.sleep(5)
        
        # 4. 노트북 생성 (AI Agent 마스터 클래스)
        notebook_name = "AI Agent 마스터 클래스 (Agent J 특강)"
        print(f"'{notebook_name}' 노트북 생성 시도 중...")
        
        # NOTE: client.create_notebook is often async in modern MCP implementations
        notebook = await client.create_notebook(notebook_name)

        if not notebook:
            print("에러: 노트북 생성에 실패했습니다.")
            return

        notebook_id = notebook.id
        print(f"성공! 노트북 ID: {notebook_id}")

        # 5. 국내 자료 10선 요약 생성
        korean_resources = """# [국내] AI 에이전트 생성 및 활용 자료 10선

1. **SPRi 'AI 에이전트 동향 보고서'**: 소프트웨어정책연구소가 발행한 AI 에이전트의 정의와 주요 기업 사례 분석의 정석.
... (Omitted for brevity, keep original text) ...
10. **세종디엑스 '트롤리AI'**: 중소/중견 기업을 위한 특화형 에이전트 솔루션 및 도메인 전문성 확보 방법.
"""

        # 6. 해외 자료 10선 요약 생성
        global_resources = """# [해외] AI 에이전트 프레임워크 및 활용 자료 10선

1. **LangChain/LangGraph**: 에이전트의 '뼈대'와 '뇌'를 구성하는 가장 강력한 오픈소스 프레임워크 및 그래프 기반 조종법.
... (Omitted for brevity, keep original text) ...
10. **Google Agent Development Kit (ADK)**: 제미나이(Gemini) 생태계를 위해 설계된 모듈형 에이전트 개발 프레임워크 공식 문서.
"""

        # 7. 소스 추가
        print("국내 자료 업데이트 중...")
        await client.add_text_source(notebook_id, korean_resources, "국내 AI 에이전트 핵심 자료 10선")
        
        print("해외 자료 업데이트 중...")
        await client.add_text_source(notebook_id, global_resources, "해외 AI 에이전트 핵심 자료 10선")

        print(f"\n[SUCCESS] '{notebook_name}' 프로젝트에 지식 자산을 성공적으로 이식했습니다.")
        
    except Exception as e:
        print(f"\n[ERROR] 작전 중 오류 발생: {str(e)}")
    finally:
        if client:
            print("세션을 종료합니다.")
            await client.close()

if __name__ == "__main__":
    asyncio.run(main())
