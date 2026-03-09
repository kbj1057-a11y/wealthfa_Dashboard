import pandas as pd
import json
import os
import sys

# 인코딩 문제 해결을 위해 stdout 설정 변경
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

excel_path = r'g:\내 드라이브\안티그래비티\TEST\수수료분석\최종병합_수수료명세서_압축판.xlsx'
output_path = r'g:\내 드라이브\안티그래비티\TEST\1_Dashboard_App\2_Netlify_Static\data.json'

def convert():
    print("Data conversion starting...")
    
    try:
        # 1. 시트 로드
        df_life = pd.read_excel(excel_path, sheet_name='생명보험사_202602')
        df_dmg = pd.read_excel(excel_path, sheet_name='손해보험사_202602')
        
        # 2. 통합 및 전처리
        combined = pd.concat([df_life, df_dmg], ignore_index=True)
        
        # 3. 사용자 정의 규칙 적용 (보험군 분류: 제휴사명 기준)
        def classify_group(name):
            return '생명보험' if '생명' in str(name) else '손해보험'
        
        combined['보험군'] = combined['제휴사명'].apply(classify_group)
        
        # 4. 컬럼 매핑 로직
        def get_indicators(row):
            if row['보험군'] == '생명보험':
                # 생명: 지표1=환산성적, 지표2=보험료
                val1 = row['환산성적'] if '환산성적' in row and pd.notnull(row['환산성적']) else 0
                val2 = row['보험료'] if '보험료' in row and pd.notnull(row['보험료']) else 0
            else:
                # 손해: 지표1=보험료, 지표2=0
                val1 = row['보험료'] if '보험료' in row and pd.notnull(row['보험료']) else 0
                val2 = 0
            return pd.Series([val1, val2])

        combined[['업적지표1', '업적지표2']] = combined.apply(get_indicators, axis=1)
        
        # 5. 필요한 컬럼 추출
        target_cols = ['보험군', '계약일자', '제휴사명', 'FC명', '지급구분', '상품군', '상품명', '계약자', '업적지표1', '업적지표2', '지사수수료']
        final_df = combined[target_cols].copy()
        
        # 6. 정제
        final_df['계약일자'] = final_df['계약일자'].astype(str).str.replace('-', '').str[:8]
        final_df['지사수수료'] = final_df['지사수수료'].fillna(0).astype(int)
        final_df['업적지표1'] = final_df['업적지표1'].fillna(0).astype(int)
        final_df['업적지표2'] = final_df['업적지표2'].fillna(0).astype(int)
        
        # 데이터 정제: 모든 문자열 컬럼의 앞뒤 공백 제거 및 NaN 처리
        final_df['보험군'] = final_df['보험군'].fillna('').astype(str).str.strip()
        final_df['지급구분'] = final_df['지급구분'].fillna('').astype(str).str.strip()
        final_df['제휴사명'] = final_df['제휴사명'].fillna('').astype(str).str.strip()
        final_df['FC명'] = final_df['FC명'].fillna('미지정').astype(str).str.strip()
        final_df['지사수수료'] = pd.to_numeric(final_df['지사수수료'], errors='coerce').fillna(0)
        
        # 7. JSON 저장
        # JSON 변환
        data_list = final_df.to_dict(orient='records')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=None)
            
        print(f"SUCCESS: {len(data_list)} records processed.")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    convert()
