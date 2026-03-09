import codecs

file_path = 'dashboard_app.py'
text = codecs.open(file_path, 'r', 'utf-8').read()

# Add missing table-toggle-container CSS
css_to_add = """
    /* 토글 컨테이너 (테이블 박스 상단부 결합용) */
    .table-toggle-container {
        background-color: var(--bg-card) !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 15px 15px 0 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-bottom: none !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: -1.5rem !important; 
        position: relative;
        z-index: 10;
        text-align: left;
    }
    
    /* 스트림릿 요소 간격 강제 제거 */
    .stMarkdown:has(.table-toggle-container) {
        margin-bottom: -1.5rem !important; 
        position: relative;
        z-index: 10;
    }
"""

if 'table-toggle-container {' not in text:
    text = text.replace('/* 스트림릿 테이블(데이터프레임) 스타일', css_to_add + '\n    /* 스트림릿 테이블(데이터프레임) 스타일')

# Update stDataFrame CSS
df_css_old = """    [data-testid="stDataFrame"] > div {
        background-color: var(--bg-card) !important;
    }"""

df_css_new = """    [data-testid="stDataFrame"] > div {
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
codecs.open(file_path, 'w', 'utf-8').write(text)
print('Fixed layout and missing divs')
