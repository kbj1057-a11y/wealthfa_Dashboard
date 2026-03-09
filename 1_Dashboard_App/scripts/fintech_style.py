import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, "r", "utf-8").read()

# 1. KPI Card padding & fonts
text = re.sub(r"padding: 28px 20px 20px 20px !important;", r"padding: 36px 28px 28px 28px !important;", text)
text = re.sub(r"font-weight:800; font-size:2.6rem;", r"font-weight:900; font-size:3.2rem;", text)
text = re.sub(r"font-size:2.1rem;", r"font-size:3.0rem; font-weight:800;", text)
text = re.sub(r"font-size:3.5rem;", r"font-size:4.0rem; font-weight:900;", text)

# 2. Top-only gold accents (remove inline styles that override border)
text = re.sub(r"style=[\"']border-top: 5px solid #D4AF37.*?[\"']", r"style=\"border-top: 4px solid var(--color-gold) !important; border-left: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05); overflow: hidden;\"", text)
text = re.sub(r"style=[\"']border: 2px solid #D4AF37;[\"']", r"style=\"border-top: 4px solid var(--color-gold) !important; border-left: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05); overflow: hidden;\"", text)


# 3. Grid Lines styling
# Streamlit dataframe inside iframe/glide-data-grid might need special treatment.
# But we can try injecting generic CSS for any table, plus styling the columns.
table_css = """
    /* 촌스러운 엑셀 격자선 전면 철거 (VVIP 하이엔드) */
    table, th, td, [data-testid="stDataFrame"] > div, .stDataFrame, .stDataFrame > div > div, .stDataFrame > div > div > div {
        border-left: none !important;
        border-right: none !important;
        border-top: none !important;    
    }
    
    th {
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    td {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
"""

if "촌스러운 엑셀 격자선 전면 철거" not in text:
    text = text.replace("/* 테이블 컨테이너 스타일 */", table_css + "\n    /* 테이블 컨테이너 스타일 */")

from textwrap import dedent

# We also need to style pandas so that streamlit's glide-data-grid doesn't draw gridlines.
# Unfortunately, glide-data-grid in Streamlit hardcodes cell borders to a faint gray.
# But we can try pd.Styler's `border` rule.
pandas_styler_code = """
    # VVIP 테이블 선 처리
    def set_borders(val):
        return 'border-left: none; border-right: none; border-bottom: 1px solid rgba(255, 255, 255, 0.05);'

    styled_df = df.style.format(format_dict, na_rep="").map(color_negative_red).map(set_borders)
    # Streamlit dataframe configuration (using new config options if available)
    st.dataframe(styled_df, *args, **kwargs, hide_index=True)
    return
"""

text = re.sub(r"styled_df = df\.style\.format\(format_dict, na_rep=\"\"\)\.map\(color_negative_red\)\n[ ]+return st\.dataframe\(styled_df, \*args, \*\*kwargs\)",
              pandas_styler_code, text)

# Let's remove any hide_index=True that was passed as an arg because we added it directly, or leave it. 
# Wait, st.dataframe handles duplicate kwargs poorly.
# Let's just fix the method instead.

text = text.replace(
'''    styled_df = df.style.format(format_dict, na_rep="").map(color_negative_red)
    return st.dataframe(styled_df, *args, **kwargs)''',
'''    styled_df = df.style.format(format_dict, na_rep="").map(color_negative_red).set_properties(**{'border-left': 'none !important', 'border-right': 'none !important', 'border-top': 'none !important', 'border-bottom': '1px solid rgba(255, 255, 255, 0.05) !important', 'background-color': 'transparent !important'})
    return st.dataframe(styled_df, *args, **kwargs)'''
)

codecs.open(file_path, "w", "utf-8").write(text)
print("Applied VIP fintech details!")

