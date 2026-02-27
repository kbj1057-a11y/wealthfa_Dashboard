import pandas as pd
import datetime
import os

# 파일 경로 설정
input_file = r'g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년출근체크\260201-260227.xls'
output_file = r'g:\내 드라이브\안티그래비티\TEST\매일업데이트\26년출근체크\26년2월_출근통계_보고서.xlsx'

# 2026년 2월 평일 및 공휴일 제외 리스트 (설 연휴: 16, 17, 18)
def get_working_days(year, month):
    holidays = [datetime.date(2026, 2, 16), datetime.date(2026, 2, 17), datetime.date(2026, 2, 18)]
    working_days = []
    
    # 1일부터 말일까지 확인
    day = datetime.date(year, month, 1)
    while day.month == month:
        if day.weekday() < 5 and day not in holidays: # 월(0)~금(4)
            working_days.append(day)
        day += datetime.timedelta(days=1)
    return working_days

working_days = get_working_days(2026, 2)
print(f"분석 대상 근무일 수: {len(working_days)}일")

try:
    # 엑셀 파일 로드 (B열: 발생시간=index 1, F열: 이름=index 5)
    # 인코딩이나 컬럼명 깨짐 방지를 위해 인덱스로 접근
    df = pd.read_excel(input_file)
    
    # 컬럼 인덱스 1(발생시간), 5(이름) 추출
    data = df.iloc[:, [1, 5]].copy()
    data.columns = ['발생시간', '이름']
    
    # 발생시간을 datetime 객체로 변환
    data['발생시간'] = pd.to_datetime(data['발생시간'])
    data['날짜'] = data['발생시간'].dt.date
    data['시간'] = data['발생시간'].dt.time
    
    # 이름 리스트 추출 (공백 제거)
    data['이름'] = data['이름'].astype(str).str.strip()
    names = data['이름'].unique()
    # 유효하지 않은 이름 제거 (NaN 등)
    names = [n for n in names if n != 'nan' and n != 'None']
    
    results = []
    
    for name in names:
        attendance_count = 0
        tardy_count = 0
        absence_count = 0
        
        person_data = data[data['이름'] == name]
        
        for day in working_days:
            # 해당 날짜의 기록 찾기 (가장 빠른 시간 기준)
            day_records = person_data[person_data['날짜'] == day]
            
            if day_records.empty:
                absence_count += 1
            else:
                first_time = day_records['발생시간'].min().time()
                
                # 09:01:00 이전 (09:00:59까지) -> 출근
                # 09:01:00 ~ 10:00:00 -> 지각
                # 10:00:01 이후 -> 결근
                
                check_in_limit = datetime.time(9, 1, 0)
                tardy_limit = datetime.time(10, 0, 0)
                
                if first_time < check_in_limit:
                    attendance_count += 1
                elif first_time <= tardy_limit:
                    tardy_count += 1
                else:
                    absence_count += 1
        
        results.append({
            '이름': name,
            '출근': attendance_count,
            '지각': tardy_count,
            '결근': absence_count,
            '총근무일수': len(working_days)
        })
    
    # 결과 데이터프레임 생성 및 저장
    result_df = pd.DataFrame(results)
    
    # 가독성을 위해 정렬 (출근 많은 순)
    result_df = result_df.sort_values(by=['출근', '지각'], ascending=[False, True])
    
    # 엑셀 저장
    result_df.to_excel(output_file, index=False)
    print(f"분석 완료! 결과 파일: {output_file}")

except Exception as e:
    print(f"에러 발생: {e}")
    import traceback
    traceback.print_exc()
