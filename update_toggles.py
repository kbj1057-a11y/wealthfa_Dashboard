import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, 'r', 'utf-8').read()

# 1. Insert CSS
css_to_add = """
    /* 상세보기 토글 버튼 스타일 (VVIP) */
    .table-toggle-btn {
        background-color: rgba(22, 32, 59, 0.8); /* --bg-card with opacity */
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 500;
        font-size: 1.0rem;
        color: var(--color-text);
        display: inline-block;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: color 0.2s ease, background-color 0.2s ease;
        cursor: pointer;
    }
    
    .table-toggle-btn:hover {
        color: var(--color-gold);
        background-color: rgba(255, 255, 255, 0.05); /* slightly brighten */
    }
    
    .table-toggle-btn::after {
        content: ' ▼';
        font-size: 0.85em;
        margin-left: 6px;
        opacity: 0.8;
    }
"""

if "table-toggle-btn" not in text:
    text = text.replace('/* 스트림릿 테이블(데이터프레임) 스타일', css_to_add + '\n    /* 스트림릿 테이블(데이터프레임) 스타일')

# 2. Replace HTML snippets
# The original texts look like this:
# <p style='font-size:1.1rem; font-weight:bold; color:#A0AEC0;'>▸ 제휴사별 생보 환산 (클릭)</p>
# <p style='font-size:1.1rem; font-weight:bold; color:#A0AEC0;'>▸ [{target_company}] 상품군별 (클릭시 하단상세)</p>
# etc.

# For product groups:
text = re.sub(
    r"<p style='font-size:1\.1rem; font-weight:bold; color:.*?;'>▸ \[{target_company}\] 상품군별 .*?</p>",
    r"<div class='table-toggle-btn'>[{target_company}] 상품군별 상세 보기</div>",
    text
)

# For company lists:
text = re.sub(
    r"<p style='font-size:1\.1rem; font-weight:bold; color:.*?;'>▸ 제휴사별.*?</p>",
    r"<div class='table-toggle-btn'>제휴사별 상세 보기</div>",
    text
)

text = re.sub(
    r"<p style='font-size:0\.9rem; font-weight:bold; color:.*?;'>▸ 제휴사별.*?</p>",
    r"<div class='table-toggle-btn'>제휴사별 상세 보기</div>",
    text
)

codecs.open(file_path, 'w', 'utf-8').write(text)
print("Updated toggles")
