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

    # 3. 기존 노트북 ID (매일의경제흐름읽기)
    notebook_id = "0770f952-5f73-4acf-a56a-43d279b75225"

    # 4. 최종 벌크업된 블로그 초안
    final_blog_content = """# 코스피 5,500 시대 개막, 삼성 HBM4가 쏘아 올린 역사적 변곡점 📈

## 1. 마침내 뚫린 천장, 우리는 어떤 시대를 맞이하고 있는가?
오늘 오전 9시, 대한민국 증시는 그동안 누구도 가보지 못한 5,500선이라는 고지를 점령했습니다. 3,000선 돌파가 '유동성의 힘'이었다면, 이번 5,500선 안착은 '실질적 이익의 성장'이라는 점에서 그 궤를 달리합니다. 네이버, 다음, 네이트 등 주요 포털의 경제 섹션은 온종일 이 역사적인 순간을 실시간으로 중계하고 있습니다.

## 2. 삼성전자 HBM4, 'AI 공포'를 기술로 잠재우다
글로벌 시장에서 번지고 있는 'AI 수익성 회의론'과 그로 인한 시장의 공포를 잠재운 것은 결국 기술이었습니다. 삼성전자가 차세대 HBM4 경쟁에서 압도적인 주도권을 확보했다는 소식은 반도체 섹션의 부활을 알리는 신호탄이 되었습니다. 기관과 외국인의 대규모 순매수가 삼성전자와 SK하이닉스에 집중되며 코스피의 기초체력을 증명했습니다.

## 3. 변동성의 파도 속에서 빛나는 안전자산, '금'의 질주
시장의 환호 이면에는 여전히 신중함이 공존합니다. 글로벌 통상 압박과 AI 시장의 변동성에 대비하려는 스마트 머니들은 금 가드(Gold Guard)를 구축하고 있습니다. 금값이 g당 23만 원을 넘어서는 등 사상 최고치를 경신한 것은, 지금의 상승장이 단순한 투기가 아닌 '철저한 리스크 관리' 위에서 움직이고 있음을 시사합니다.

## 4. 대표님의 인사이트: 지금 당장 주목해야 할 전략
지수가 높다고 두려워할 필요는 없습니다. 다만 '묻지마 투자'는 금물입니다. 
- 공격: HBM4 기술력을 바탕으로 한 반도체 가치 사슬(소부장 포함)에 주목하십시오.
- 수비: 지정학적 리스크와 통화 정책의 변화에 대비해 포트폴리오의 10~15%는 안전자산인 금이나 실물 자산으로 채우는 '바벨 전략'이 유효합니다.

## 5. 맺음말: 매일의 경제 흐름이 당신의 자산이 됩니다
오늘의 흐름을 읽는 자가 내일의 부를 선점합니다. 이 기록은 [매일의경제흐름읽기] 프로젝트에 저장되어 대표님만의 강력한 데이터베이스로 남을 것입니다. 
"""
    print(f"노트북({notebook_id})에 최종 탈고본 업데이트 중...")
    result = client.add_text_source(notebook_id, final_blog_content, "2026-02-13 오전 경제 브리핑 (최종본)")

    if result:
        print("성공! 최종 탈고본이 NotebookLM에 동기화되었습니다.")
    else:
        print("에러: 데이터 동기화에 실패했습니다.")

if __name__ == "__main__":
    main()
