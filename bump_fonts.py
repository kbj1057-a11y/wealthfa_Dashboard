import codecs
import re

file_path = "dashboard_app.py"
text = codecs.open(file_path, 'r', 'utf-8').read()

# 1. Bump CSS classes
text = text.replace('font-size:1.0rem;', 'font-size:1.2rem;') # .kpi-title
text = text.replace('font-size:2.2rem;', 'font-size:2.6rem;') # .kpi-value

# 2. Bump inline styles in HTML snippets
# kpi-value main
text = re.sub(r'font-size:1\.4rem;', 'font-size:1.8rem;', text)
text = re.sub(r'font-size:1\.5rem;', 'font-size:1.9rem;', text)
text = re.sub(r'font-size:2\.8rem;', 'font-size:3.2rem;', text)

# kpi-value unit ('원')
text = re.sub(r'font-size:0\.9rem;', 'font-size:1.1rem;', text)
text = re.sub(r'font-size:1\.2rem;', 'font-size:1.4rem;', text)

# table headers
text = re.sub(r"font-size:0\.9rem; font-weight:bold;", "font-size:1.1rem; font-weight:bold;", text)

codecs.open(file_path, 'w', 'utf-8').write(text)
print("Font sizes bumped!")
