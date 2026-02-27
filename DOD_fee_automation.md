
# DOD: e-Partner 예상수수료 조회 자동화

## 1. 개요
삼성생명 e-Partner 시스템의 '예상수수료조회_AFC' 메뉴를 자동화하여, 매일 변경되는 예상 수수료 데이터를 엑셀로 추출하고 저장하는 RPA 스크립트를 구현함.

## 2. 구현 기능
- **자동 로그인**: 기존 프로세스 종료 후 클린 재실행, ID/PW 입력 및 중복 로그인 팝업 자동 처리.
- **메뉴 이동**: `수수료_AFC` > `예상수수료조회_AFC` 메뉴로 정확한 좌표 기반 이동.
- **조회 조건 설정**: 
  - `수수료레벨 생보L1`: 2단계 클릭 (선택 -> 확인)
  - `수수료레벨 손보L2`: 2단계 클릭 (선택 -> 확인)
- **데이터 조회 및 다운로드**: 조회 버튼 클릭 후 대기, 엑셀 다운로드 버튼 및 사유 입력('upmuyong') 자동화.
- **파일 저장**: `g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)` 경로에 `YYYYMMDD_HHMMSS_예상수수료.xlsx` 형식으로 자동 저장.

## 3. 기술 스택
- **Language**: Python 3.14.3 (rpa_venv)
- **Library**: 
  - `pyautogui`: 마우스/키보드 제어
  - `pywinauto`: 윈도우 창 제어 및 활성화 감지
  - `pyperclip`: 한글/특수문자 입력 안전성 확보
  - `subprocess`: 외부 프로그램 실행

## 4. 실행 방법
```bash
# 가상환경 활성화 (필요 시)
# Windows: rpa_venv\Scripts\activate

# 스크립트 실행
python execution/fee_automation.py
```

## 5. 유지보수 가이드
### 좌표 수정 필요 시
해상도 변경이나 UI 위치 변경 시 `execution/record_fee_coordinates.py`를 실행하여 좌표를 다시 측정하고, `execution/fee_automation.py` 상단 좌표 변수를 업데이트한다.

```python
# execution/fee_automation.py 상단
POS_MENU_FEE_AFC = (754, 59)             # 수수료_AFC
POS_SUBMENU_EXPECTED_FEE = (128, 230)     # 예상수수료조회_AFC
...
```

### 엑셀 저장 경로 변경 시
`save_excel_process` 함수 내 `target_dir` 변수를 수정한다.

```python
target_dir = r"g:\내 드라이브\안티그래비티\TEST\수수료관리(일자별)"
```
