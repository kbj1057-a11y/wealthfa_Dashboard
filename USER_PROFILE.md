
# USER Profile & Working Style
**Updated: 2026-02-19**

## 1. Core Identity & Working Style
- **Efficiency-Driven Leader**: 불필요한 반복 업무를 극도로 싫어하며, 자동화를 통해 확보된 시간을 '휴식'과 '창의적 업무'에 쓰기를 원함.
- **Safety First**: 데이터 무결성을 중요시함. 항상 원본 백업을 먼저 요청하고, 새로운 데이터가 기존 데이터를 덮어쓰거나 손상시키는 것을 경계함.
- **Clear Confirmations**: 돌다리도 두드려보고 건너는 스타일. 중간 단계마다 확실한 브리핑과 승인(Confirmation)을 거쳐야 다음 단계로 진행함.
- **Human-Centric Tech**: 기술 자체가 목적이 아니라, 기술이 나에게 주는 '여유'와 '편리함'을 중시함. (예: 1분 전 팝업으로 휴식 시간 확보)

## 2. Technical Preferences
- **Excel Master Update**:
    - **Key**: `증권번호` (Unique Identifier)
    - **Logic**: 
        - 신규 증권번호 → 행 추가 (Append)
        - 기존 증권번호 → `RAWDATA` 시트의 특정 컬럼(`납입기간` 등)만 업데이트 (Update)
        - 마스터 파일 고유 데이터(`메모`, `시책` 등)는 절대 건드리지 않음 (Preserve)
- **Automation Flow**:
    - **One-Click Solution**: 여러 개의 스크립트를 따로 돌리는 것을 싫어함. 한 번 실행으로 모든 과정(로그인→수집→통합→종료)이 끝나는 것을 선호.
    - **Robust Error Handling**: 에러 발생 시 어설프게 복구하기보다, 깔끔하게 프로세스를 종료(`clean_start`)하고 처음부터 다시 시작하는 확실한 방법을 선호.
    - **User Interaction**: 자동화 시작 전 '준비 시간(1분)'과 '취소 옵션'을 제공하여, 사용자가 통제권을 가질 수 있도록 함.

## 3. Communication Style
- **Result-Oriented**: 과정이 복잡하더라도 결과는 "그래서 몇 건이 추가됐고, 몇 건이 업데이트됐는지" 명확한 수치로 보고받기를 원함.
- **Supportive Partner**: AI를 도구가 아닌 파트너로 대우함. ("고맙다", "수고했다" 등의 격려를 아끼지 않음)
- **Proactive Suggestions**: 사용자가 놓친 부분(예: 업데이트 결과 브리핑 누락 등)을 먼저 챙겨주고 제안하는 것을 좋아함.

## 4. Future Action Plan
- **Daily 10 AM Routine**: 매일 오전 10시 자동 실행 스케줄링 준수.
- **Maintenance**: `e-Partner` 사이트 UI 변경 시 즉각적인 좌표(`coordinates`) 수정 필요.
- **Expansion**: 추후 다른 업무(고객 관리, 메시지 발송 등) 자동화 요청 시, 이번 'One-Click & Safety First' 원칙을 그대로 적용할 것.
