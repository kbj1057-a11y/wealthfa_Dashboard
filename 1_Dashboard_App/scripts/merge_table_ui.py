import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, 'r', 'utf-8').read()

# 1. Remove empty table-container divs
text = re.sub(r"st\.markdown\(\"<div class='table-container'>.*?\n", "", text)
text = re.sub(r"st\.markdown\(\"<div class='table-container' style='.*?>\", unsafe_allow_html=True\)\n", "", text)
text = re.sub(r"st\.markdown\(\"</div>\", unsafe_allow_html=True\)\n", "", text)

# 2. Modify toggle-btn div to be inside a toggle-container
text = re.sub(
    r"<div class='table-toggle-btn'>(.*?)</div>",
    r"<div class='table-toggle-container'><div class='table-toggle-btn'>\1</div></div>",
    text
)

# 3. Add CSS for table-toggle-container
css_to_add = """
    /* 토글 컨테이너 (테이블 박스 상단부 결합용) */
    .table-toggle-container {
        background-color: var(--bg-card) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 15px 15px 0 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-bottom: none !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: -1rem !important; 
        position: relative;
        z-index: 10;
        text-align: left;
    }
    
    /* 기존 테이블 컨테이너 스타일(빈 박스 만드는 원흉) 무력화 */
    .table-container {
        display: none !important;
    }
"""

if "table-toggle-container" not in text:
    text = text.replace('/* 테이블 컨테이너 스타일 */', css_to_add + '\n    /* 테이블 컨테이너 스타일 */')

# 4. Modify stDataFrame override
df_css_old = """[data-testid="stDataFrame"] > div {
        background-color: var(--bg-card) !important;
    }"""
df_css_new = """[data-testid="stDataFrame"] > div {
        background-color: var(--bg-card) !important;
        border-radius: 0 0 12px 12px !important;
        padding: 0 15px 15px 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: none !important;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5) !important;
        position: relative;
        z-index: 1;
    }"""
text = text.replace(df_css_old, df_css_new)

# Also fix the `st.markdown("<div class='table-container' style='border: 2px solid #D4AF37;'>`
text = re.sub(r"st\.markdown\(f\"<div class='table-container'.*?\", unsafe_allow_html=True\)\n", "", text)

codecs.open(file_path, 'w', 'utf-8').write(text)
print("Merged table UI applied")
