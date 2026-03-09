import pandas as pd
import json

file_path = r'g:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx'
try:
    xl = pd.ExcelFile(file_path)
    result = {"sheets": xl.sheet_names}
    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
        result[sheet] = df.columns.tolist()
    
    with open('excel_structure.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("SUCCESS")
except Exception as e:
    print(f'Error: {e}')
