import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, "r", "utf-8").read()

# 1. Remove .table-container CSS
text = re.sub(r"/\* 테이블 컨테이너 스타일 \*/\s*\.table-container\s*\{.*?\n\s*\}\s*", "", text, flags=re.DOTALL)

# 2. Clean up any leftover <div class='table-container'> from st.markdown
text = re.sub(r"st\.markdown\([f]?\"<div class='table-container'.*?unsafe_allow_html=True\)\n", "", text)
text = re.sub(r"[ \t]*st\.markdown\(\"</div>\", unsafe_allow_html=True\)\n", "", text)

# Just to be safe, if there's any `<div class='table-container'>` mixed with toggle container (like in col1, col3, col5)
text = re.sub(r"<div class='table-container'[a-zA-Z0-9\-\s\:\;\'\"\=\#\,]+>", "", text)
text = re.sub(r"<div class='table-container'>", "", text)


# specific fix for lines like:
# st.markdown("<div class='table-container' style='margin-bottom:15px;'><div class='table-toggle-container'><div class='table-toggle-btn'>제휴사별 상세 보기</div></div>", unsafe_allow_html=True)
text = re.sub(r"st\.markdown\(\"<div class='table-container'.*?><div class='table-toggle-container'>", r"st.markdown(\"<div class='table-toggle-container'>", text)

# specific fix for
# st.markdown(f"<div class='table-container' style=\"border-top: 4px solid var(--color-gold) !important; border-left: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05); overflow: hidden;\"><div class='table-toggle-container'><div class='table-toggle-btn'>[{target_company}] 상품군별 상세 보기</div></div>", unsafe_allow_html=True)
text = re.sub(r"st\.markdown\([f]?\"<div class='table-container'.*?><div class='table-toggle-container'>", r"st.markdown(f\"<div class='table-toggle-container'>", text)

codecs.open(file_path, "w", "utf-8").write(text)
print("Removed standalone table container boxes.")
