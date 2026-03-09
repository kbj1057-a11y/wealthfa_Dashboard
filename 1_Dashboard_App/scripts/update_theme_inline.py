import codecs

file_path = "dashboard_app.py"
text = codecs.open(file_path, 'r', 'utf-8').read()

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
