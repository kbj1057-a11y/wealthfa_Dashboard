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

    # 3. 새 프로젝트 생성: 무한매수&VR 투자
    notebook_name = "무한매수&VR 투자 (라오어 공식 전략)"
    print(f"'{notebook_name}' 노트북 생성 시도 중...")
    notebook = client.create_notebook(notebook_name)

    if not notebook:
        print("에러: 노트북 생성에 실패했습니다.")
        return

    notebook_id = notebook.id
    print(f"성공! 노트북 ID: {notebook_id}")

    # 4. 무한매수 V2.2 정리
    v2_2_content = """# 라오어 무한매수법 V2.2 핵심 가이드 (안정형)

## 1. 개요
*   하락장 방어력을 높이고, 40회차 원금 소진 위험을 줄이는 데 집중한 버전입니다.
*   변동성이 큰 3배 레버리지 ETF(TQQQ, SOXL 등)를 40분할로 매수합니다.

## 2. 주요 로직
*   **분할**: 총 원금을 40분할하여 매수합니다.
*   **RSI 활용**: 고점 매수를 피하기 위해 RSI 지표를 참조하여 매수 여부를 결정합니다.
*   **매수 방식 변화 (20회차 기준)**:
    *   20회차 미만: LOC 큰 수 매수 (평소보다 공격적 평단 관리)
    *   20회차 이상: 평단 LOC 매수로 1회분만 매수 (방어적 전환)
*   **급등 방지**: LOC 큰 수 매수 시, 평단 대비 최대 +5%까지만 매수 가격을 제한하여 고점 매수를 방지합니다.

## 3. 수익 실현
*   평단 대비 10% 수익 시 지정가 매도.
*   20회차 이상 진행 시 5% 단위의 부분 익절을 병행하여 현금 흐름을 창출합니다.
"""

    # 5. 무한매수 V3.0 정리
    v3_0_content = """# 라오어 무한매수법 V3.0 핵심 가이드 (공격형/반복리)

## 1. 개요
*   상승장에서 고수익을 목표로 하는 공격형 버전입니다. (초보자 주의)
*   수익금을 재투자하는 '반복리' 개념이 핵심입니다.

## 2. 주요 로직
*   **분할**: 기존 40분할에서 **20분할**로 축소하여 더 빠른 자금 투입을 진행합니다.
*   **T값 활용**: (누적 매수액 / 1회 매수액)을 'T값'으로 설정하여 정밀하게 회차를 관리합니다.
*   **반복리 시스템**: 사이클이 수익으로 종료되거나 쿼터 매도 시 발생한 수익금의 절반을 다음 회차 원금에 40분할하여 더해줍니다. (눈덩이 효과)

## 3. 목표 수익률 상향
*   TQQQ: 15%
*   SOXL: 20%
*   단기적으로 높은 수익을 노리는 대신, 그만큼 리스크도 큽니다.
"""

    # 6. VR 5.0 정리
    vr_5_0_content = """# 라오어 VR 5.0 (Value Rebalancing) 장기 투자 가이드

## 1. 개요
*   무한매수법이 단기 수익 창출용이라면, VR은 **10년 이상의 장기 자산 증식**을 목표로 합니다.
*   목표 밸류(V값)에 맞춰 내 계좌의 평가액을 일정하게 유지하는 '리밸런싱' 전략입니다.

## 2. 핵심 지표: V값 (Value)
*   V값은 내 계좌가 유지해야 할 '목표 가격 가이드'입니다.
*   2주를 한 사이클로 하며, 매 사이클마다 POOL(예수금)의 1/10을 V값에 더해 우상향시킵니다.

## 3. 매수/매도 기준
*   **최댓값 (Upper Limit)**: V값의 +15% 이상일 때 '초과분 매도' (현금 확보)
*   **최솟값 (Lower Limit)**: V값의 -15% 이하일 때 'POOL의 일부로 매수' (평단 관리)
*   안전 범위: V값의 ±15% 내에 있으면 아무 작업도 하지 않고 다음 사이클로 넘어갑니다.

## 4. 자금 관리 (POOL)
*   초기 자본의 90%를 주식에, 10%를 현금(POOL)으로 시작합니다. 
*   주가 하락 시 POOL을 사용하여 매수하되, 한 사이클에 POOL의 50%를 넘지 않도록 제한합니다.
"""

    # 7. 소스 추가
    print("V2.2 업데이트 중...")
    client.add_text_source(notebook_id, v2_2_content, "무한매수법 V2.2 가이드")
    
    print("V3.0 업데이트 중...")
    client.add_text_source(notebook_id, v3_0_content, "무한매수법 V3.0 가이드")

    print("VR 5.0 업데이트 중...")
    client.add_text_source(notebook_id, vr_5_0_content, "밸류리밸런싱(VR) 5.0 가이드")

    print(f"작전 성공! '{notebook_name}' 프로젝트에 핵심 전략 3종이 세팅되었습니다.")

if __name__ == "__main__":
    main()
