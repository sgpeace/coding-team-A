import pandas as pd

# 일별 수익률 불러오기
df = pd.read_excel('hanmi_daily_return.xlsx')

# 'Date' 컬럼을 datetime 형식으로 변환
df['Date'] = pd.to_datetime(df['Date'])

# 2024-05-08부터 2024-06-30까지의 행만 추출
filtered_df = df[(df['Date'] >= '2023-09-01') & (df['Date'] <= '2024-09-30')]

# total_score 불러오기
df1 = pd.read_excel('hanmi_1_year_total_scores_llm.xlsx')

# 'Date' 컬럼을 datetime 형식으로 변환
df1['Date'] = pd.to_datetime(df1['Date'])

# 1) df1에서 total_score가 0.5 이상인 날짜 추출
high_score_dates = df1[(df1['total_score'] >= 0.7) & (df1['total_score'] <= 0.8)]['Date']

# 2) 추출된 날짜에 대해 다음날에 해당하는 행들을 filtered_df에서 추출
next_day_dates = high_score_dates + pd.Timedelta(days=1)

# 3) filtered_df에서 next_day_dates에 해당하는 행들을 추출 (존재하는 날짜만 추출)
available_dates = filtered_df['Date'].isin(next_day_dates)
result_df = filtered_df[available_dates]

# 결과 데이터프레임 확인
print(result_df)

# 초기 자본금 설정
initial_capital = 1000000  # 100만원
capital = initial_capital

# 일별 수익률을 적용하여 자본금 계산
for daily_return in result_df['Daily Return']:
    capital *= (1 + daily_return)

# 결과 출력
print(f"최종 자본금: {capital:.2f} 원")