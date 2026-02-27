
import os
import time
import json
import datetime
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def naver_login(driver, user_id, user_pw):
    """네이버 로그인 (CAPTCHA 방지)"""
    driver.get("https://nid.naver.com/nidlogin.login")
    time.sleep(2)

    # 아이디 입력
    pyperclip.copy(user_id)
    id_input = driver.find_element(By.ID, "id")
    id_input.click()
    id_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 비밀번호 입력
    pyperclip.copy(user_pw)
    pw_input = driver.find_element(By.ID, "pw")
    pw_input.click()
    pw_input.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 로그인 버튼 클릭
    driver.find_element(By.ID, "log.login").click()
    time.sleep(5)

def publish_cafe_article(cafe_id, menu_id, title, content, user_id, user_pw, draft=True):
    """네이버 카페 특정 게시판에 글쓰기 및 임시저장/등록"""
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 1. 로그인
        naver_login(driver, user_id, user_pw)
        
        # 2. 특정 메뉴 글쓰기 페이지 진입
        write_url = f"https://cafe.naver.com/ca-fe/cafes/{cafe_id}/articles/write?menuId={menu_id}"
        driver.get(write_url)
        print(f"Entering write page: {write_url}")
        time.sleep(10)

        # 3. 게시판 선택 (보험NEWS) - URL로 안될 경우 대비
        try:
            board_select = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.BoardSelect--button")))
            board_select.click()
            time.sleep(2)
            # '보험NEWS' 텍스트가 포함된 옵션 클릭
            target_board = driver.find_element(By.XPATH, "//a[contains(., '보험NEWS')]")
            target_board.click()
            print("Success: Selected board '보험NEWS'")
            time.sleep(1)
        except Exception as e:
            print(f"Warning: Board selection failed, but continuing... ({e})")

        # 4. 제목 입력
        pyperclip.copy(title)
        title_found = False
        for selector in ["textarea.textarea_input", ".BaseTextArea--textarea", ".textarea_input"]:
            try:
                title_area = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                title_area.click()
                time.sleep(1)
                webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                print(f"Success: Input title")
                title_found = True
                break
            except:
                continue
        
        # 5. 본문 입력
        pyperclip.copy(content)
        body_found = False
        for selector in [".se-content", ".se-main-container", "div[contenteditable='true']"]:
            try:
                body_area = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                body_area.click()
                time.sleep(2)
                webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                print(f"Success: Input body")
                body_found = True
                break
            except:
                continue

        # 6. 임시등록 버튼 클릭 (상단 '임시등록' 버튼)
        print("Starting button click phase...")
        if draft:
            # New UI의 '임시등록' 버튼 셀렉터
            save_selectors = [
                "button.BaseButton--tempSave",
                "//button[contains(., '임시등록')]",
                "//button[contains(@class, 'tempSave')]"
            ]
            clicked = False
            for sel in save_selectors:
                try:
                    if sel.startswith("//"):
                        btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, sel)))
                    else:
                        btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                    
                    if btn:
                        driver.execute_script("arguments[0].click();", btn)
                        print(f"Success: Clicked temp save button: {sel}")
                        clicked = True
                        time.sleep(5) 
                        break
                except:
                    continue
            
            if not clicked:
                print("Error: Could not find temp save button.")
                driver.save_screenshot(".tmp/error_retry_save.png")
        else:
            # 등록 버튼
            publish_selectors = ["button.BaseButton--publish", "//button[contains(., '등록')]"]
            for sel in publish_selectors:
                try:
                    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel) if not sel.startswith("//") else (By.XPATH, sel)))
                    btn.click()
                    print(f"Success: Clicked publish button")
                    time.sleep(8)
                    break
                except:
                    continue

        print("Process completed.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        try:
            time.sleep(5)
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    USER_ID = "wealthfa10"
    USER_PW = "1q2w3e4r!@#$"
    CAFE_ID = "31343922"
    MENU_ID = "6"
    
    # 1. 최신 뉴스 데이터 로드 시도
    news_items = []
    try:
        with open(".tmp/news_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            news_items = data.get("insurance_news", [])
    except:
        pass

    # 데이터가 비어있을 경우 새로운 주제(재테크/경제) 샘플 활용
    if not news_items:
        news_items = [
            {
                "title": "2026년 재테크 전략, '안전 자산'과 '배당주'에 주목하라",
                "full_content": "최근 금리 변동성이 커지면서 투자자들의 고민이 깊어지고 있다. 전문가들은 올해 재테크의 핵심으로 안전 자산인 금과 채권, 그리고 꾸준한 수익을 기대할 수 있는 고배당주를 꼽았다. 특히 연금 저축과 ISA 계좌를 활용한 절세 전략이 그 어느 때보다 중요해진 시점이다. 또한 부동산 시장은 지역별 양극화가 심화될 것으로 보여 보수적인 접근이 필요하다는 분석이다.",
                "link": "https://finance.naver.com/"
            }
        ]

    # 2. 최대 3개의 기사를 각각 별도의 포스팅으로 생성
    processed_count = 0
    # news_items가 리스트가 아닐 경우를 대비해 안전하게 처리
    target_news = news_items if isinstance(news_items, list) else []
    
    for main_news in target_news[:3]:
        raw_title = main_news['title']
        media_name = main_news.get('media', 'Insurance Media')
        
        # 매체별/주제별 후킹 문구 생성
        hooking_suffix = f" - [{media_name}] Industry Hot Issue 🔍"
        if "가이드라인" in raw_title or "금융당국" in raw_title: 
            hooking_suffix = " - Important: Financial Guideline Analysis 📊"
        elif "실손" in raw_title or "손해율" in raw_title:
            hooking_suffix = " - Key Update: Claim Ratio Insights 📈"
        
        today = datetime.datetime.now().strftime("%y.%m.%d")
        final_title = f"[{today}] {raw_title}{hooking_suffix}"
        
        # 3. 3줄 요약 구성
        summary = [
            f"1. According to {media_name}, a key issue regarding {raw_title} has been reported.",
            "2. This update is expected to impact the insurance market environment and customer consulting.",
            "3. Please refer to the summarized text to select necessary information for your clients."
        ]
        # 한글 제목/내용은 유지하되 로그만 영문으로 처리
        summary_kr = [
            f"1. {media_name} 보도에 따르면, {raw_title} 관련 이슈가 발생했습니다.",
            "2. 해당 내용은 향후 보험 시장의 영업 환경 및 고객 상담에 영향을 미칠 것으로 보입니다.",
            "3. 요약된 원문을 참고하여 고객분들에게 필요한 정보를 선별해 보시기 바랍니다."
        ]
        
        # 4. 전체 본문 구성 (원문 우선 -> 3줄요약 후순위, 인사말 제거)
        content = f"### [기사 원문 내용] ({media_name})\n\n{main_news.get('full_content', 'Loading content...')}\n\n"
        content += f" source: {main_news['link']}\n\n"
        content += "---\n\n"
        content += f"### [3줄 요약]\n" + "\n".join(summary_kr) + "\n\n"
        content += "---\n"

        # 5. 실행 (임시저장)
        print(f"[{processed_count + 1}/3] Creating post: {raw_title}")
        success = publish_cafe_article(CAFE_ID, MENU_ID, final_title, content, USER_ID, USER_PW, draft=True)
        
        if success:
            processed_count += 1
            print(f"Success: Saved {processed_count} draft(s)")
        
        # 연속 포스팅 사이 대기
        if processed_count < 3 and processed_count < len(target_news):
            print("Preparing next post (Wait 30s)...")
            time.sleep(30)
        
        if processed_count >= 3:
            break

    print(f"Total {processed_count} draft(s) created.")

