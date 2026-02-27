import json
import os
import sys
from pathlib import Path
from notebooklm_mcp.client import NotebookLMClient
from notebooklm_mcp.config import ServerConfig, AuthConfig

def setup_environment():
    """환경 변수 및 경로 설정을 초기화하고 .env 파일을 로드합니다."""
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

def load_auth_data():
    """auth.json에서 인증 데이터를 로드합니다."""
    auth_path = Path(__file__).parent.parent / 'auth.json'
    if not auth_path.exists():
        raise FileNotFoundError(f"인증 파일({auth_path})을 찾을 수 없습니다.")
    
    with open(auth_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # Selenium용 쿠키 리스트 생성
        selenium_cookies = []
        for name, value in data.get('cookies', {}).items():
            selenium_cookies.append({
                'name': name,
                'value': value,
                'domain': '.google.com',
                'path': '/'
            })
        
        # 원본 데이터와 가공된 쿠키 리스트를 모두 포함하여 반환
        result = data.copy()
        result['selenium_cookies'] = selenium_cookies
        return result

def get_client():
    """최신 버전의 NotebookLMClient 인스턴스를 생성하여 반환합니다."""
    setup_environment()
    
    # Chrome 프로필 경로 설정
    profile_dir = Path(__file__).parent.parent / ".chrome_profile"
    profile_dir.mkdir(exist_ok=True)
    
    # 1. 설정 구성
    auth_config = AuthConfig(
        use_persistent_session=True,
        profile_dir=str(profile_dir.absolute()),
        auto_login=False
    )
    
    config = ServerConfig(
        headless=False,
        auth=auth_config
    )
    
    # 2. 클라이언트 초기화
    client = NotebookLMClient(config)
    return client
