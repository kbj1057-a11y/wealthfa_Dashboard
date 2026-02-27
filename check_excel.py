import pandas as pd
import os

file_path = r'g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년출근체크\260201-260227.xls'

try:
    # Try reading with pandas
    # .xls files might need xlrd or pyxlsb
    df = pd.read_excel(file_path)
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:\n", df.head())
    print("\nColumn index check:")
    for i, col in enumerate(df.columns):
        print(f"Index {i}: {col}")
except Exception as e:
    print(f"Error reading file: {e}")
