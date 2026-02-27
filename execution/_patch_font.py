path = r'g:\내 드라이브\안티그래비티\TEST\execution\export_timelapse_html.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'fontSize":8,"color":"rgb(180,120,0)"' in line:
        lines[i] = line.replace('fontSize":8', 'fontSize":14').replace('textShadowBlur":4', 'textShadowBlur":6')
        print(f'Fixed line {i+1}: FC init label fontSize 8→14')
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
