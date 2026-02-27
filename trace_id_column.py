import pandas as pd
import os

latest_contract = r"g:\내 드라이브\안티그래비티\TEST\계약관리(일자별)\20260227_144604_계약일자별조회.xlsx"

if os.path.exists(latest_contract):
    df = pd.read_excel(latest_contract)
    print("계약 파일 샘플 데이터 (처음 2개 인덱스):")
    # 모든 컬럼을 다 보여주기 위해 세팅
    pd.set_option('display.max_columns', None)
    print(df.iloc[:2, :])
    
    # 데이터 패턴으로 증권번호 찾기 (예: 'L123456789' 또는 숫자 등)
    print("\n[데이터 내용 확인]")
    for i in range(df.shape[1]):
        sample_val = df.iloc[0, i]
        print(f"Index {i}: {sample_val}")
