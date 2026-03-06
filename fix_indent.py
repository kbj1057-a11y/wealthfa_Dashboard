import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, 'r', 'utf-8').read()

# Fix indentation and remove trailing </div> from top tier
text = re.sub(
    r'([ ]{4})st\.markdown\("<div class=\'table-toggle-container\'><div class=\'table-toggle-btn\'>(.*?)</div></div>", unsafe_allow_html=True\)\n([ ]{4})disp_dataframe\((.*?), key="(sel_ach_.*?)"\)\n[ ]{4}st\.markdown\("</div>", unsafe_allow_html=True\)',
    r'\1st.markdown("<div class=\'table-toggle-container\'><div class=\'table-toggle-btn\'>\2</div></div>", unsafe_allow_html=True)\n\3disp_dataframe(\4, key="\5")',
    text
)

# And similarly for the ones with wrong indentation:
text = re.sub(
    r'\n        st\.markdown\("<div class=\'table-toggle-container\'',
    r'\n    st.markdown("<div class=\'table-toggle-container\'',
    text
)

# Wait, let's just find and replace the closing </div>
text = re.sub(
    r'disp_dataframe(.*?)\n    st\.markdown\("</div>", unsafe_allow_html=True\)',
    r'disp_dataframe\1',
    text
)

codecs.open(file_path, 'w', 'utf-8').write(text)
print("Fixed indent and tags")
