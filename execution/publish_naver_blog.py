
import os
import time
import json
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
    """네이버 로그인 (CAPTCHA 방지를 위해 클릭 & 붙여넣기 방식 사용)"""
    driver.get("https://nid.naver.com/nidlogin.login")
    time.sleep(1)

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
    time.sleep(2)

def publish_blog(title, content, user_id, user_pw):
    """네이버 블로그 포스팅 실행 (임시 저장 모드)"""
    chrome_options = Options()
    # 윈도우 환경에서 보안 정책 문제를 피하기 위한 옵션들
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 1. 로그인
        naver_login(driver, user_id, user_pw)
        
        # 2. 블로그 글쓰기 페이지 진입
        driver.get("https://blog.naver.com/PostWrite.naver")
        print("글쓰기 페이지 로딩 중 (15초 대기)...")
        time.sleep(15) # 첫 개설 후 팝업이나 초기 로딩이 많을 수 있음

        # 3. 중요: 스마트에디터는 iframe 내부에 있음
        try:
            driver.switch_to.frame("mainFrame")
            print("스마트에디터 iframe 전환 성공")
        except:
            print("iframe 전환 실패")

        # 4. 각종 팝업 및 도움말 닫기 (반복 시도)
        popup_selectors = [
            ".se-help-guide-close", 
            ".help_close", 
            ".btn_close",
            "//button[contains(@class, 'close')]",
            "//a[contains(@class, 'close')]"
        ]
        for sel in popup_selectors:
            try:
                if sel.startswith("//"):
                    btn = driver.find_element(By.XPATH, sel)
                else:
                    btn = driver.find_element(By.CSS_SELECTOR, sel)
                btn.click()
                print(f"팝업/도움말 닫기 성공: {sel}")
                time.sleep(1)
            except:
                continue

        # 5. 제목 입력
        pyperclip.copy(title)
        title_success = False
        for selector in [".se-documentTitle .se-placeholder", ".se-ff-nanumgothic", ".se-placeholder", "//textarea[contains(@placeholder, '제목')]"]:
            try:
                if selector.startswith("//"):
                    title_area = driver.find_element(By.XPATH, selector)
                else:
                    title_area = driver.find_element(By.CSS_SELECTOR, selector)
                title_area.click()
                time.sleep(1)
                webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                print(f"제목 입력 성공: {selector}")
                title_success = True
                break
            except:
                continue
        if not title_success: print("제목 영역을 찾지 못했습니다.")

        # 6. 본문 입력
        pyperclip.copy(content)
        body_success = False
        for selector in [".se-component-content .se-placeholder", ".se-content", "//div[contains(@contenteditable, 'true')]", ".se-placeholder"]:
            try:
                if selector.startswith("//"):
                    body_area = driver.find_element(By.XPATH, selector)
                else:
                    body_area = driver.find_element(By.CSS_SELECTOR, selector)
                body_area.click()
                time.sleep(1)
                webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                print(f"본문 입력 성공: {selector}")
                body_success = True
                break
            except:
                continue
        if not body_success: print("본문 영역을 찾지 못했습니다.")

        # 7. 임시 저장 버튼 클릭
        try:
            driver.switch_to.default_content() # 저장 버튼은 보통 iframe 밖에 있음
            print("저장 버튼 탐색을 위해 iframe 탈출")
            time.sleep(2)
            
            save_selectors = [
                "//button[contains(@class, 'btn_save')]",
                "//button[contains(@class, 'se-btn-save')]",
                "//span[contains(text(), '저장')]/ancestor::button",
                "//button[contains(., '저장')]",
                ".btn_save",
                ".publish_btn__m96Y_ .btn_save",
                "//button[@type='button' and contains(., '저장')]"
            ]
            
            save_btn = None
            for selector in save_selectors:
                try:
                    if selector.startswith("//"):
                        save_btn = driver.find_element(By.XPATH, selector)
                    else:
                        save_btn = driver.find_element(By.CSS_SELECTOR, selector)
                    if save_btn and save_btn.is_displayed():
                        print(f"저장 버튼 발견: {selector}")
                        break
                except:
                    continue
            
            if save_btn:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                time.sleep(2)
                driver.execute_script("arguments[0].click();", save_btn)
                print("JS 강제 클릭으로 임시 저장 실행!")
                time.sleep(10) # 저장 처리 및 서버 업로드 대기 대폭 확대
            else:
                print("저장 버튼 탐색 최종 실패")
        except Exception as e:
            print(f"저장 과정 최종 단계 오류: {e}")

        print("임시 저장 완료! 대표님, 블로그 글쓰기 페이지의 '저장' 목록을 확인해 보세요.")
        return True

    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        # 임시 저장 확인을 위해 브라우저를 바로 닫지 않거나, 사용자가 확인하게 함
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    # 대표님, 여기서 아이디와 비밀번호를 설정해 주세요!
    USER_ID = "wealthfa10"
    USER_PW = "1q2w3e4r!@#$"
    
    final_blog_title = "코스피 5,500 시대 개막, 삼성 HBM4가 쏘아 올린 역사적 변곡점 📈"
    final_blog_content = """오늘 오전 9시, 대한민국 증시는 그동안 누구도 가보지 못한 5,500선이라는 고지를 점령했습니다. 

삼성이 열어젖힌 HBM4의 시대가 반도체 섹션의 부활을 알리는 신호탄이 되었습니다.

물론 안전자산인 금값 또한 상승 중이므로 전략적인 포트폴리오 관리가 필요합니다... (이하 중략)
"""
    
    if USER_ID == "YOUR_NAVER_ID":
        print("에러: 스크립트 내부의 USER_ID와 USER_PW를 실제 정보로 수정해야 합니다!")
    else:
        publish_blog(final_blog_title, final_blog_content, USER_ID, USER_PW)
