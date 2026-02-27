# Orchestration: Agent Master Control

## 🎯 Current Project Goal
- 집 컴퓨터(Home PC) 환경 초기 셋팅 및 3계층 아키텍처(Directive-Orchestration-Execution) 최적화.

## 🚦 System Status
- **Phase**: Initial Setup
- **Architecture**: 3-Layer (agent.md 기반)
- **Environment**: Windows (Google Drive Workspace)

## 🗺️ Roadmap & Task List
- [x] Planning & Analysis
- [x] Step 1: Create `orchestration.md`
- [x] Step 2: Virtual Environment & Dependency Check (Python 3.12.10 + venv + libraries installed)
- [x] Step 3: Environment Variables (.env) Setup
- [x] Step 4: Fix Hardcoded Paths in `execution/` (Refactored with `utils.py`)
- [ ] Step 5: System Verification Test (Ready to execute)

## 📝 Recent Updates & Learnings
- **2026-02-13 23:30**: 집 컴퓨터 초기 셋팅 완료. Python 3.12.10 설치, 가상환경 생성, 필수 라이브러리(notebooklm-mcp, python-dotenv) 설치 완료.
- **Issue Resolved**: 하드코딩된 경로를 `utils.py`로 통합하여 환경 독립성 확보.
- **Next**: `.env` 파일 설정 및 `auth.json` 배치 후 스크립트 실행 테스트.

## 🛠️ Active Directives
- `agent.md`: Core operating instructions.
- `directives/economy_blog_automation.md`
- `directives/insurance_planner_growth.md`
