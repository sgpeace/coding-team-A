import torch
from openai import OpenAI
from transformers import pipeline
import pandas as pd
import time

import os

# GPT API client 설정
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키를 가져옴
client = OpenAI(api_key=api_key)
# 터미널에서 export OPENAI_API_KEY="your_openai_api_key"

# kor -> eng 번역 함수
def translate_to_english(text):
    prompt = f"Translate the following news headline from Korean to English. Make sure to preserve the meaning as accurately as possible and retain the nuance of a news article:\n\n'{text}'"

    # GPT-4 호출
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )

    # 응답에서 번역된 텍스트 추출
    translated_text = response.choices[0].message.content
    return translated_text

# GPU 설정 (MPS가 가능하다면 사용)
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

# 감성 분석을 위한 모델 불러오기 (MPS 설정 사용)
sentiment_pipe = pipeline(model='ProsusAI/finbert', device=device)

# Test 데이터
df = pd.read_excel('hanmi_titles_1_year.xlsx')
data_title = df['제목'].tolist()

# 결과 저장용 리스트
translated_titles = []
sentiment_labels = []
sentiment_scores = []

# 각 뉴스기사 제목에 대해 번역 및 감성분석 수행
for title in data_title:
    # 한국어 제목을 영어로 번역
    translated_title = translate_to_english(title)
    translated_titles.append(translated_title)

    # 번역된 제목을 이용해 감성분석 수행
    sentiment_result = sentiment_pipe(translated_title)
    sentiment_labels.append(sentiment_result[0]['label'])  # 감성 분석 결과의 레이블 (긍정/부정/중립)
    sentiment_scores.append(sentiment_result[0]['score'])  # 감성 분석 결과의 신뢰도 점수

    # 요청 간의 대기 시간 추가 (1초)
    time.sleep(0.1)

# 결과를 데이터프레임에 저장
df['영어_제목'] = translated_titles
df['감성'] = sentiment_labels
df['감성_점수'] = sentiment_scores

# 컬럼 이름 변경
df.rename(columns={'발행날짜': 'Date', '제목': 'Title', '감성_점수': 'Score', '감성': 'Sentiment'}, inplace=True)

# 날짜 형식을 datetime 객체로 변환
df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d')

# 데이터프레임을 엑셀 파일로 저장
df.to_excel('hanmi_titles_1_year_with_sentiments.xlsx', index=False)

print(df)