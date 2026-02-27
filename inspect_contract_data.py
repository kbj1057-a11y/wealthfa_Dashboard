import pandas as pd
import glob
import os

DIR_CONTRACT = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)"
latest_contract = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)\20260227_144604_계약일자별조회.xlsx"

if os.path.exists(latest_contract):
    df = pd.read_excel(latest_contract)
    print("계약 파일 상위 5행 데이터:")
    print(df.head())
    print("\n컬럼 리스트 (인덱스 포함):")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")
