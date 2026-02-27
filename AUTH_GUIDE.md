# NotebookLM 인증 정보 추출 가이드

## 방법 1: Chrome 개발자 도구 사용 (추천)

### 단계별 가이드:

1. **Chrome에서 NotebookLM 열기**
   - https://notebooklm.google.com 접속
   - Google 계정으로 로그인

2. **개발자 도구 열기**
   - `F12` 키를 누르거나
   - 우클릭 > "검사" 선택

3. **Application 탭으로 이동**
   - 개발자 도구 상단의 "Application" 탭 클릭
   - 왼쪽 메뉴에서 "Cookies" > "https://notebooklm.google.com" 선택

4. **필요한 쿠키 복사**
   다음 쿠키들을 찾아서 값을 복사하세요:
   - `SID`
   - `HSID`
   - `SSID`
   - `APISID`
   - `SAPISID`
   - `__Secure-1PSID`
   - `__Secure-3PSID`

5. **Network 탭에서 CSRF 토큰 찾기**
   - "Network" 탭으로 이동
   - NotebookLM에서 아무 작업이나 수행 (예: 새 노트 생성)
   - 요청 목록에서 POST 요청 찾기
   - "Headers" 탭에서 `x-csrf-token` 또는 `csrf-token` 값 복사

6. **auth.json 파일 생성**
   아래 템플릿을 사용하여 프로젝트 루트에 `auth.json` 파일을 만드세요:

```json
{
  "cookies": {
    "SID": "여기에_SID_값_붙여넣기",
    "HSID": "여기에_HSID_값_붙여넣기",
    "SSID": "여기에_SSID_값_붙여넣기",
    "APISID": "여기에_APISID_값_붙여넣기",
    "SAPISID": "여기에_SAPISID_값_붙여넣기",
    "__Secure-1PSID": "여기에_Secure-1PSID_값_붙여넣기",
    "__Secure-3PSID": "여기에_Secure-3PSID_값_붙여넣기"
  },
  "csrf_token": "여기에_CSRF_토큰_값_붙여넣기",
  "session_id": "여기에_SID_값_다시_붙여넣기"
}
```

## 방법 2: 기존 auth.json 파일 복사

만약 다른 컴퓨터에 이미 `auth.json` 파일이 있다면:

1. 기존 파일을 찾습니다:
   - `C:\Users\Direct\.notebooklm-mcp\auth.json` (이전 컴퓨터)
   
2. 이 프로젝트 루트로 복사:
   - `g:\내 드라이브\안티그래비티\TEST\auth.json`

## 주의사항

- 쿠키 값은 **절대 공유하지 마세요** (계정 보안 위험)
- 쿠키는 일정 시간 후 만료될 수 있습니다
- 만료되면 다시 추출해야 합니다

## 다음 단계

auth.json 파일을 생성했다면:
```bash
.venv\Scripts\python execution\init_notebook_api.py
```
위 명령어로 테스트해 보세요!
