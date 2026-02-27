// Antigravity Intelligence Hub - Frontend Application
// API 연동 및 실시간 업데이트 로직

const API_BASE_URL = 'http://localhost:8000';
let ws = null;
let reconnectInterval = null;

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    connectWebSocket();
    setInterval(updateStatus, 5000); // 5초마다 상태 업데이트
});

// 앱 초기화
async function initializeApp() {
    await loadScripts();
    await updateStatus();
}

// WebSocket 연결
function connectWebSocket() {
    try {
        ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onopen = () => {
            console.log('WebSocket 연결 성공');
            addLog('시스템', 'WebSocket 연결 성공', 'success');
            if (reconnectInterval) {
                clearInterval(reconnectInterval);
                reconnectInterval = null;
            }
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket 오류:', error);
            addLog('시스템', 'WebSocket 연결 오류', 'error');
        };
        
        ws.onclose = () => {
            console.log('WebSocket 연결 종료');
            addLog('시스템', 'WebSocket 연결 종료 - 재연결 시도 중...', 'info');
            
            // 재연결 시도
            if (!reconnectInterval) {
                reconnectInterval = setInterval(() => {
                    console.log('WebSocket 재연결 시도...');
                    connectWebSocket();
                }, 5000);
            }
        };
    } catch (error) {
        console.error('WebSocket 연결 실패:', error);
    }
}

// WebSocket 메시지 처리
function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'task_started':
            addLog(data.task_id, '작업 시작됨', 'info');
            updateScriptStatus(data.task_id, 'running');
            break;
            
        case 'task_completed':
            addLog(data.task_id, `작업 완료 (${data.status})`, data.status === 'success' ? 'success' : 'error');
            updateScriptStatus(data.task_id, data.status);
            updateStatus(); // 전체 상태 갱신
            break;
            
        case 'task_error':
            addLog(data.task_id, `오류: ${data.error}`, 'error');
            updateScriptStatus(data.task_id, 'error');
            break;
            
        case 'log':
            const modalLog = document.getElementById('modalLog');
            if (modalLog && document.getElementById('taskModal').classList.contains('active')) {
                addModalLog(data.message, data.stream === 'stderr' ? 'error' : 'info');
            }
            addLog(data.task_id, data.message, data.stream === 'stderr' ? 'error' : 'info');
            break;
    }
}

// 스크립트 목록 로드
async function loadScripts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/scripts`);
        const data = await response.json();
        
        const scriptsGrid = document.getElementById('scriptsGrid');
        scriptsGrid.innerHTML = '';
        
        Object.entries(data.scripts).forEach(([id, script]) => {
            const card = createScriptCard(id, script);
            scriptsGrid.appendChild(card);
        });
    } catch (error) {
        console.error('스크립트 로드 실패:', error);
        addLog('시스템', 'API 서버에 연결할 수 없습니다. 백엔드를 시작해주세요.', 'error');
    }
}

// 스크립트 카드 생성
function createScriptCard(id, script) {
    const card = document.createElement('div');
    card.className = 'script-card';
    card.id = `script-${id}`;
    
    card.innerHTML = `
        <div class="script-header">
            <span class="script-icon">${script.icon}</span>
            <h3 class="script-title">${script.name}</h3>
        </div>
        <p class="script-description">${script.description}</p>
        <div class="script-actions">
            <button class="btn btn-primary" onclick="executeScript('${id}')">
                실행
            </button>
            <button class="btn btn-secondary" onclick="viewLogs('${id}')">
                로그 보기
            </button>
        </div>
        <span class="script-status status-idle" id="status-${id}">대기 중</span>
    `;
    
    return card;
}

// 스크립트 실행
async function executeScript(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/execute/${taskId}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            const error = await response.json();
            addLog(taskId, `실행 실패: ${error.error}`, 'error');
            return;
        }
        
        const data = await response.json();
        addLog(taskId, '작업이 시작되었습니다', 'success');
        
        // 모달 열기
        openTaskModal(taskId);
        
    } catch (error) {
        console.error('스크립트 실행 실패:', error);
        addLog(taskId, `실행 오류: ${error.message}`, 'error');
    }
}

// 스크립트 상태 업데이트
function updateScriptStatus(taskId, status) {
    const statusElement = document.getElementById(`status-${taskId}`);
    if (!statusElement) return;
    
    statusElement.className = 'script-status';
    
    switch (status) {
        case 'running':
            statusElement.classList.add('status-running');
            statusElement.textContent = '실행 중...';
            break;
        case 'success':
            statusElement.classList.add('status-success');
            statusElement.textContent = '완료';
            setTimeout(() => {
                statusElement.className = 'script-status status-idle';
                statusElement.textContent = '대기 중';
            }, 5000);
            break;
        case 'failed':
        case 'error':
            statusElement.classList.add('status-error');
            statusElement.textContent = '실패';
            setTimeout(() => {
                statusElement.className = 'script-status status-idle';
                statusElement.textContent = '대기 중';
            }, 5000);
            break;
        default:
            statusElement.classList.add('status-idle');
            statusElement.textContent = '대기 중';
    }
}

// 전체 상태 업데이트
async function updateStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/status`);
        const data = await response.json();
        
        // 통계 업데이트
        document.getElementById('totalArticles').textContent = data.news_data.total_articles;
        document.getElementById('uploadedArticles').textContent = data.news_data.total_articles;
        document.getElementById('activeTasks').textContent = Object.keys(data.active_tasks).length;
        
        // 최근 업데이트 시간
        if (data.news_data.last_updated) {
            const date = new Date(data.news_data.last_updated);
            const timeAgo = getTimeAgo(date);
            document.getElementById('lastUpdate').textContent = timeAgo;
        }
        
        // 뉴스 목록 업데이트
        updateNewsList(data.news_data.articles);
        
    } catch (error) {
        console.error('상태 업데이트 실패:', error);
    }
}

// 뉴스 목록 업데이트
function updateNewsList(articles) {
    const newsList = document.getElementById('newsList');
    
    if (!articles || articles.length === 0) {
        newsList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">수집된 뉴스가 없습니다.</p>';
        return;
    }
    
    newsList.innerHTML = articles.map(article => `
        <div class="news-item">
            <div class="news-header">
                <h4 class="news-title">${article.title}</h4>
                <span class="news-media">${article.media}</span>
            </div>
            <a href="${article.link}" target="_blank" class="news-link">${article.link}</a>
        </div>
    `).join('');
}

// 로그 추가
function addLog(source, message, type = 'info') {
    const logContainer = document.getElementById('logContainer');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    const now = new Date();
    const timeStr = now.toLocaleTimeString('ko-KR');
    
    logEntry.innerHTML = `
        <span class="log-time">[${timeStr}]</span>
        <span class="log-message log-${type}">[${source}] ${message}</span>
    `;
    
    logContainer.insertBefore(logEntry, logContainer.firstChild);
    
    // 최대 100개 로그만 유지
    while (logContainer.children.length > 100) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

// 모달 로그 추가
function addModalLog(message, type = 'info') {
    const modalLog = document.getElementById('modalLog');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;
    logEntry.textContent = message;
    
    modalLog.appendChild(logEntry);
    modalLog.scrollTop = modalLog.scrollHeight;
}

// 작업 모달 열기
function openTaskModal(taskId) {
    const modal = document.getElementById('taskModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalLog = document.getElementById('modalLog');
    const progressFill = document.getElementById('progressFill');
    
    modalTitle.textContent = `작업 실행 중: ${taskId}`;
    modalLog.innerHTML = '<div class="log-entry">작업을 시작합니다...</div>';
    progressFill.style.width = '100%';
    
    modal.classList.add('active');
}

// 모달 닫기
function closeModal() {
    const modal = document.getElementById('taskModal');
    modal.classList.remove('active');
}

// 로그 보기
async function viewLogs(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/logs/${taskId}`);
        
        if (!response.ok) {
            addLog(taskId, '로그를 찾을 수 없습니다', 'error');
            return;
        }
        
        const data = await response.json();
        
        const modal = document.getElementById('taskModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalLog = document.getElementById('modalLog');
        const progressFill = document.getElementById('progressFill');
        
        modalTitle.textContent = `로그: ${taskId}`;
        progressFill.style.width = '0%';
        
        modalLog.innerHTML = data.logs.map(log => `
            <div class="log-entry log-${log.stream === 'stderr' ? 'error' : 'info'}">
                [${new Date(log.timestamp).toLocaleTimeString()}] ${log.message}
            </div>
        `).join('');
        
        modal.classList.add('active');
        
    } catch (error) {
        console.error('로그 조회 실패:', error);
        addLog(taskId, `로그 조회 오류: ${error.message}`, 'error');
    }
}

// 시간 경과 계산
function getTimeAgo(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // 초 단위
    
    if (diff < 60) return '방금 전';
    if (diff < 3600) return `${Math.floor(diff / 60)}분 전`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`;
    return `${Math.floor(diff / 86400)}일 전`;
}

// ESC 키로 모달 닫기
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});
