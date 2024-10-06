import pandas as pd

# 1. 엑셀 파일을 업로드하고 df 형태로 저장한다.
file_path = 'hanmi_1_year_total_scores.xlsx'  # 파일 경로에 맞게 변경하세요
df = pd.read_excel(file_path)

# 2. Date 컬럼을 datetime 형식으로 변환
df['Date'] = pd.to_datetime(df['Date'])

# 3. 일요일인 경우 total_score 수정
for idx in df.index:
    if df.loc[idx, 'Date'].weekday() == 6:  # 일요일 (Sunday: weekday() == 6)
        if idx >= 2:  # 2일 전, 1일 전 데이터를 참조하기 위해 인덱스가 2 이상이어야 함
            df.loc[idx, 'total_score'] = (
                df.loc[idx - 2, 'total_score'] * 0.2 +
                df.loc[idx - 1, 'total_score'] * 0.3 +
                df.loc[idx, 'total_score'] * 0.5
            )

# 4. 금요일(weekday=4), 토요일(weekday=5)에 해당하는 날짜 삭제
df = df[~df['Date'].dt.weekday.isin([4, 5])]

# 수정된 DataFrame 확인
print(df)

# 필요한 경우 엑셀 파일로 저장
df.to_excel('modified_hanmi_1_year_total_scores.xlsx', index=False)