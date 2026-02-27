"""
Antigravity Intelligence Hub - Backend API
실시간 자동화 모니터링 및 제어 시스템
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import os

app = FastAPI(title="Antigravity Intelligence Hub API")

# CORS 설정 (Next.js 프론트엔드와 통신)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).parent.parent
EXECUTION_DIR = BASE_DIR / "execution"
TMP_DIR = BASE_DIR / ".tmp"
LOGS_DIR = BASE_DIR / ".tmp" / "logs"

# 로그 디렉토리 생성
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 실행 중인 작업 추적
active_tasks: Dict[str, dict] = {}

# WebSocket 연결 관리
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# 자동화 스크립트 정의
AUTOMATION_SCRIPTS = {
    "fetch_news": {
        "name": "뉴스 수집",
        "description": "보험 전문지 3사에서 최신 뉴스 수집",
        "script": "fetch_news.py",
        "icon": "📰",
        "category": "data_collection"
    },
    "upload_news": {
        "name": "NotebookLM 업로드",
        "description": "수집된 뉴스를 NotebookLM에 자동 업로드",
        "script": "upload_news.py",
        "icon": "📤",
        "category": "knowledge_transfer"
    },
    "publish_blog": {
        "name": "네이버 블로그 발행",
        "description": "가공된 콘텐츠를 네이버 블로그에 자동 발행",
        "script": "publish_naver_blog.py",
        "icon": "✍️",
        "category": "publishing"
    },
    "publish_cafe": {
        "name": "네이버 카페 발행",
        "description": "가공된 콘텐츠를 네이버 카페에 자동 발행",
        "script": "publish_naver_cafe.py",
        "icon": "💬",
        "category": "publishing"
    }
}

class TaskRequest(BaseModel):
    task_id: str

class TaskLog(BaseModel):
    timestamp: str
    task_id: str
    status: str
    message: str

@app.get("/")
async def root():
    return {
        "service": "Antigravity Intelligence Hub",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/scripts")
async def get_scripts():
    """사용 가능한 모든 자동화 스크립트 목록 반환"""
    return {
        "scripts": AUTOMATION_SCRIPTS,
        "active_tasks": len(active_tasks)
    }

@app.get("/api/status")
async def get_status():
    """현재 시스템 전체 상태 반환"""
    
    # 최근 뉴스 데이터 확인
    news_data = None
    news_file = TMP_DIR / "news_data.json"
    if news_file.exists():
        with open(news_file, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
    
    # 실행 로그 확인
    recent_logs = []
    if LOGS_DIR.exists():
        log_files = sorted(LOGS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)[:10]
        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8') as f:
                recent_logs.append(json.load(f))
    
    return {
        "timestamp": datetime.now().isoformat(),
        "news_data": {
            "last_updated": news_data.get("timestamp") if news_data else None,
            "total_articles": len(news_data.get("insurance_news", [])) if news_data else 0,
            "articles": news_data.get("insurance_news", []) if news_data else []
        },
        "active_tasks": active_tasks,
        "recent_logs": recent_logs
    }

@app.post("/api/execute/{task_id}")
async def execute_task(task_id: str, background_tasks: BackgroundTasks):
    """특정 자동화 스크립트 실행"""
    
    if task_id not in AUTOMATION_SCRIPTS:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task '{task_id}' not found"}
        )
    
    if task_id in active_tasks:
        return JSONResponse(
            status_code=409,
            content={"error": f"Task '{task_id}' is already running"}
        )
    
    script_info = AUTOMATION_SCRIPTS[task_id]
    script_path = EXECUTION_DIR / script_info["script"]
    
    if not script_path.exists():
        return JSONResponse(
            status_code=404,
            content={"error": f"Script file not found: {script_info['script']}"}
        )
    
    # 백그라운드에서 스크립트 실행
    background_tasks.add_task(run_script, task_id, script_path)
    
    return {
        "task_id": task_id,
        "status": "started",
        "script": script_info["name"],
        "timestamp": datetime.now().isoformat()
    }

async def run_script(task_id: str, script_path: Path):
    """백그라운드에서 Python 스크립트 실행"""
    
    active_tasks[task_id] = {
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "script": str(script_path)
    }
    
    # WebSocket으로 시작 알림
    await manager.broadcast({
        "type": "task_started",
        "task_id": task_id,
        "timestamp": datetime.now().isoformat()
    })
    
    log_file = LOGS_DIR / f"{task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_data = {
        "task_id": task_id,
        "started_at": datetime.now().isoformat(),
        "logs": []
    }
    
    try:
        # Python 스크립트 실행
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(EXECUTION_DIR)
        )
        
        # 실시간 로그 수집
        async def read_stream(stream, stream_name):
            while True:
                line = await stream.readline()
                if not line:
                    break
                text = line.decode('utf-8', errors='ignore').strip()
                if text:
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "stream": stream_name,
                        "message": text
                    }
                    log_data["logs"].append(log_entry)
                    
                    # WebSocket으로 실시간 전송
                    await manager.broadcast({
                        "type": "log",
                        "task_id": task_id,
                        **log_entry
                    })
        
        # stdout, stderr 동시 읽기
        await asyncio.gather(
            read_stream(process.stdout, "stdout"),
            read_stream(process.stderr, "stderr")
        )
        
        # 프로세스 종료 대기
        await process.wait()
        
        # 결과 저장
        status = "success" if process.returncode == 0 else "failed"
        log_data["status"] = status
        log_data["completed_at"] = datetime.now().isoformat()
        log_data["return_code"] = process.returncode
        
        active_tasks[task_id] = {
            "status": status,
            "completed_at": datetime.now().isoformat(),
            "return_code": process.returncode
        }
        
        # WebSocket으로 완료 알림
        await manager.broadcast({
            "type": "task_completed",
            "task_id": task_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        log_data["status"] = "error"
        log_data["error"] = str(e)
        log_data["completed_at"] = datetime.now().isoformat()
        
        active_tasks[task_id] = {
            "status": "error",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        }
        
        await manager.broadcast({
            "type": "task_error",
            "task_id": task_id,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
    
    finally:
        # 로그 파일 저장
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        # 일정 시간 후 active_tasks에서 제거
        await asyncio.sleep(60)
        if task_id in active_tasks:
            del active_tasks[task_id]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """실시간 로그 스트리밍용 WebSocket"""
    await manager.connect(websocket)
    try:
        while True:
            # 클라이언트로부터 메시지 대기 (연결 유지용)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/logs/{task_id}")
async def get_task_logs(task_id: str):
    """특정 작업의 최근 로그 조회"""
    log_files = sorted(
        LOGS_DIR.glob(f"{task_id}_*.json"),
        key=os.path.getmtime,
        reverse=True
    )
    
    if not log_files:
        return JSONResponse(
            status_code=404,
            content={"error": f"No logs found for task '{task_id}'"}
        )
    
    # 가장 최근 로그 반환
    with open(log_files[0], 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
