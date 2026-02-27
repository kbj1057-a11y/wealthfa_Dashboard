

import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import os

def fetch_article_content(url):
    """기사 URL에서 본문 전체 텍스트 추출"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # 인코딩 자동 감지 및 설정 (euc-kr 등 대응)
        if response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        content = ""
        # 매체별 핵심 본문 영역 셀렉터 (보강)
        selectors = [
            "#article-view-content-div", # 대한금융신문
            "#articleBody",               # 한국보험신문
            ".view_con",                  # 보험주간
            "article", ".article-body", "#articleBodyContents"
        ]
        
        for sel in selectors:
            article = soup.select_one(sel)
            if article:
                # 불필요한 요소 제거
                for tag in article.select("script, style, .ad, .bottom-ad, .sns_box, .reporter, .copyright"):
                    tag.decompose()
                text = article.get_text(separator="\n", strip=True)
                if len(text) > 100:
                    content = text
                    break
        
        if not content:
            # 최종 수단: p 태그 중 긴 것들 합치기
            content = "\n".join([p.get_text() for p in soup.select("p") if len(p.get_text()) > 30])
        
        return content
    except Exception as e:
        print(f"본문 추출 오류 ({url}): {e}")
        return ""

def fetch_specific_insurance_media():
    """지정된 3개 보험 전문지에서 뉴스 수집"""
    targets = [
        {"name": "대한금융신문", "url": "https://www.kbanker.co.kr/news/articleList.html?sc_sub_section_code=S2N15&view_type=sm", "selector": "h4.titles a", "encoding": "utf-8"},
        {"name": "보험주간", "url": "https://www.insweek.co.kr/sub.html?section=sc27", "selector": ".list_area li a, .list_box li a", "encoding": "euc-kr"},
        {"name": "한국보험신문", "url": "https://www.insnews.co.kr/news/articleList.html?sc_sub_section_code=S2N2&view_type=sm", "selector": "ul.type2 li h4 a, .artlist_list li a", "encoding": "euc-kr"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    all_news = []
    print("보험 전문지 기사 수집 시작...")
    
    for media in targets:
        try:
            print(f"[{media['name']}] 접속 중...")
            response = requests.get(media['url'], headers=headers, timeout=10)
            # 수동 인코딩 설정
            response.encoding = media['encoding']
            soup = BeautifulSoup(response.text, "html.parser")
            
            items = soup.select(media['selector'])
            found_count = 0
            for item in items:
                title = item.get_text(strip=True)
                if len(title) < 10: continue
                
                link = item['href']
                if not link.startswith("http"):
                    parsed_url = media['url'].split("/")
                    base_url = f"{parsed_url[0]}//{parsed_url[2]}"
                    link = base_url + (link if link.startswith('/') else '/' + link)
                
                all_news.append({"media": media['name'], "title": title, "link": link})
                found_count += 1
                if found_count >= 10: break # 매체별 최대 10개
        except Exception as e:
            print(f"{media['name']} 수집 중 오류: {e}")
            
    return all_news

def main():
    # 1. 3개 매체 전체 리스트 수집
    raw_news = fetch_specific_insurance_media()
    if not raw_news:
        print("수집된 뉴스가 없습니다.")
        return

    # 2. 겹치는 기사 분석 (유사도 기반 간단 로직)
    # 제목에 공통 단어가 많이 포함된 기사들을 그룹화
    print(f"총 {len(raw_news)}개의 기사 분석 중...")
    
    from collections import Counter
    import re
    
    # 3. 각 매체별 최상단 기사들을 우선순위로 본문 추출
    # (실제 업무에서는 3사 모두 다루는 주제가 가장 중요함)
    results = []
    seen_links = set()
    
    # 전략: 매체별로 1개씩 가장 최신 기사를 가져와서 포스팅 구성
    medias = ["대한금융신문", "보험주간", "한국보험신문"]
    for media_name in medias:
        media_found = 0
        for item in raw_news:
            if item['media'] == media_name and item['link'] not in seen_links:
                print(f"[{media_name}] 본문 수집: {item['title']}")
                content = fetch_article_content(item['link'])
                if len(content) > 100: # 최소 글자 수 하향 조정하여 더 많이 수집
                    results.append({
                        "title": item['title'],
                        "link": item['link'],
                        "full_content": content,
                        "media": item['media']
                    })
                    seen_links.add(item['link'])
                    media_found += 1
                    if media_found >= 2: break # 매체당 최대 2개까지 후보 확보
                    
    # 4. 저장
    final_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "insurance_news": results
    }
    
    if not os.path.exists(".tmp"): os.makedirs(".tmp")
    with open(".tmp/news_data.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"최종 {len(results)}건의 전문지 뉴스 선별 완료! -> .tmp/news_data.json")

if __name__ == "__main__":
    main()
