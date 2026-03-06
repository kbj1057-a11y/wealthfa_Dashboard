import codecs

file_path = "dashboard_app.py"
text = codecs.open(file_path, 'r', 'utf-8').read()

css_old = """<style>
    /* 전체 배경색 강제 지정 */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #F4F6F9 !important;
        color: #1E293B !important;
    }
    
    /* 사이드바 배경 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* 텍스트 색상 강제 지정 */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, span {
        color: #1E293B !important;
    }

    /* KPI 카드 등 컨테이너 배경 */
    .kpi-card {
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.03);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        text-align: left;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .kpi-title {
        color:#64748B !important; font-weight:700; font-size:1.0rem; margin-bottom:5px;
    }
    
    .kpi-value {
        font-weight:800; font-size:2.2rem; margin:0;
    }
    
    /* 테이블 컨테이너 스타일 */
    .table-container {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1px solid #E2E8F0;
    }
</style>"""

css_new = """<style>
    /* 전체 배경색 강제 지정 */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #0A1128 !important;
        color: #E2E8F0 !important;
    }
    
    /* 사이드바 배경 */
    [data-testid="stSidebar"] {
        background-color: #0A1128 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* 텍스트 색상 강제 지정 */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, span {
        color: #E2E8F0 !important;
    }
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }

    /* KPI 카드 등 컨테이너 배경 */
    .kpi-card {
        background-color: #16203B;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: left;
        margin-bottom: 20px;
        height: 100%;
    }
    
    .kpi-title {
        color: #A0AEC0 !important; font-weight:700; font-size:1.0rem; margin-bottom:5px;
    }
    
    .kpi-value {
        font-weight:800; font-size:2.2rem; margin:0;
    }
    
    /* 테이블 컨테이너 스타일 */
    .table-container {
        background-color: #16203B;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>"""

if css_old in text:
    text = text.replace(css_old, css_new)
else:
    print("Warning: css_old not found exactly.")

# Inline color replacements
replacements = {
    'color:#1E293B': 'color:#FFFFFF',
    'color:#0B57D0': 'color:#D4AF37',
    'color:#10B981': 'color:#D4AF37',
    'color:#F59E0B': 'color:#D4AF37',
    'color:#8B5CF6': 'color:#D4AF37',
    'color:#EC4899': 'color:#D4AF37',
    'color:#475569': 'color:#A0AEC0',
    'color:#64748B': 'color:#A0AEC0',
    'border-left: 5px solid #0B57D0': 'border-left: 5px solid #D4AF37',
    'border-left: 5px solid #10B981': 'border-left: 5px solid #D4AF37',
    'border-top: 5px solid #0B57D0': 'border-top: 5px solid #D4AF37',
    'border-top: 5px solid #F59E0B': 'border-top: 5px solid #D4AF37',
    'border: 2px solid #0B57D0': 'border: 2px solid #D4AF37',
    'border: 2px solid #F59E0B': 'border: 2px solid #D4AF37',
    'border: 2px solid #EC4899': 'border: 2px solid #D4AF37',
    'background-color: #F8FAFC': 'background-color: #16203B'
}

for k, v in replacements.items():
    text = text.replace(k, v)

codecs.open(file_path, 'w', 'utf-8').write(text)
print("Update complete")
