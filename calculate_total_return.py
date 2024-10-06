import pandas as pd

# 1. 일별 수익률 불러오기
df = pd.read_excel('hanmi_daily_return.xlsx')  # 파일 경로에 맞게 변경

# 'Date' 컬럼을 datetime 형식으로 변환
df['Date'] = pd.to_datetime(df['Date'])

# 백테스팅 할 날짜의 행을 추출
filtered_df = df[(df['Date'] >= '2023-09-01') & (df['Date'] <= '2024-09-30')]

# 2. total_score 불러오기
df1 = pd.read_excel('modified_hanmi_1_year_total_scores.xlsx')  # 파일 경로에 맞게 변경

# 'Date' 컬럼을 datetime 형식으로 변환
df1['Date'] = pd.to_datetime(df1['Date'])

# total_score 범위와 최종 자본금을 저장할 리스트 초기화
score_ranges = [
    (0.4, 0.45), (0.4, 0.5), (0.4, 0.55), (0.4, 0.6), (0.4, 0.65), (0.4, 0.7), (0.4, 0.75), (0.4, 0.8), (0.4, 0.85), (0.4, 0.9), (0.4, 0.95), (0.4, 1),
    (0.45, 0.5), (0.45, 0.55), (0.45, 0.6), (0.45, 0.65), (0.45, 0.7), (0.45, 0.75), (0.45, 0.8), (0.45, 0.85), (0.45, 0.9), (0.45, 0.95), (0.45, 1),
    (0.5, 0.55), (0.5, 0.6), (0.5, 0.65), (0.5, 0.7), (0.5, 0.75), (0.5, 0.8), (0.5, 0.85), (0.5, 0.9), (0.5, 0.95), (0.5, 1),
    (0.55, 0.6), (0.55, 0.65), (0.55, 0.7), (0.55, 0.75), (0.55, 0.8), (0.55, 0.85), (0.55, 0.9), (0.55, 0.95), (0.55, 1),
    (0.6, 0.65), (0.6, 0.7), (0.6, 0.75), (0.6, 0.8), (0.6, 0.85), (0.6, 0.9), (0.6, 0.95), (0.6, 1),
    (0.65, 0.7), (0.65, 0.75), (0.65, 0.8), (0.65, 0.85), (0.65, 0.9), (0.65, 0.95), (0.65, 1),
    (0.7, 0.75), (0.7, 0.8), (0.7, 0.85), (0.7, 0.9), (0.7, 0.95), (0.7, 1),
    (0.75, 0.8), (0.75, 0.85), (0.75, 0.9), (0.75, 0.95), (0.75, 1),
    (0.8, 0.85), (0.8, 0.9), (0.8, 0.95), (0.8, 1),
    (0.85, 0.9), (0.85, 0.95), (0.85, 1),
    (0.9, 0.95), (0.9, 1),
    (0.95, 1)
]

final_capitals = []

# 초기 자본금 설정
initial_capital = 1000000  # 100만원

# 각 total_score 범위에 대해 최종 자본금을 계산
for lower, upper in score_ranges:
    # 1) df1에서 해당 범위의 total_score가 있는 날짜 추출
    high_score_dates = df1[(df1['total_score'] >= lower) & (df1['total_score'] <= upper)]['Date']

    # 2) 추출된 날짜에 대해 다음날에 해당하는 행들을 filtered_df에서 추출
    next_day_dates = high_score_dates + pd.Timedelta(days=1)

    # 3) filtered_df에서 next_day_dates에 해당하는 행들을 추출 (존재하는 날짜만 추출)
    available_dates = filtered_df['Date'].isin(next_day_dates)
    result_df = filtered_df[available_dates]

    # 일별 수익률을 적용하여 자본금 계산
    capital = initial_capital
    for daily_return in result_df['Daily Return']:
        capital *= (1 + daily_return)

    # 최종 자본금 저장
    final_capitals.append(capital)

# 결과를 데이터프레임으로 정리
result_table = pd.DataFrame({
    'Score Range (Lower, Upper)': [f"{lower} - {upper}" for lower, upper in score_ranges],
    'Final Capital (KRW)': final_capitals
})

# 새로운 칼럼 추가: 최종 자본금의 백분율로 표현
result_table['Final Capital (%)'] = (result_table['Final Capital (KRW)'] / initial_capital * 100 - 100).round(2).astype(str) + '%'

# 결과 확인
print(result_table)

# 필요한 경우 엑셀 파일로 저장
result_table.to_excel('final_capital.xlsx', index=False)