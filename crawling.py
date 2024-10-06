import time
import re
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 네이버 뉴스 크롤러 클래스
class NaverNewsCrawler:
    def __init__(self, head_url, tail_url, start_date, final_date, keyword):
        self.head_url = head_url
        self.tail_url = tail_url
        self.start_date = start_date
        self.final_date = final_date
        self.keyword = keyword
        self.data = []
        self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scroll_down(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        while True:
            # 스크롤을 맨 아래로 내림
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.1)  # 새 컨텐츠 로딩 대기 시간을 0.1초로 설정
            scroll_count += 1
            print(f"스크롤 횟수: {scroll_count}")

            # 새로운 스크롤 높이를 가져옴
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # 더 이상 스크롤 할 수 없으면 종료
                break
            last_height = new_height

    def crawl(self):
        current_date = self.start_date
        while current_date >= self.final_date:
            formatted_date = current_date.strftime('%Y.%m.%d')
            middle_url = f'ds={formatted_date}&de={formatted_date}'
            url = f"{self.head_url}{middle_url}{self.tail_url}"
            self.driver.get(url)
            time.sleep(0.5)  # 페이지 로딩 대기 시간을 0.5초로 설정
            self.scroll_down()
            index = 1
            while True:
                selector = f"#sp_nws{index}"
                try:
                    news_block = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    # 제목 추출
                    try:
                        title_element = news_block.find_element(By.CSS_SELECTOR, "div.news_contents > a.news_tit")
                        title = title_element.get_attribute('title').strip()
                    except NoSuchElementException:
                        title = ''

                    if title and self.keyword in title:
                        self.data.append({'발행날짜': formatted_date, '제목': title})
                        print(f"크롤링 중: {index}번째 뉴스 - {title} ({formatted_date})")  # 크롤링 진행 상황 출력
                    
                    index += 1
                except NoSuchElementException:
                    # 더 이상 뉴스 블럭이 없으면 종료
                    break
            current_date -= timedelta(days=1)

    def save_to_excel(self, filename='naver_news.xlsx'):
        df = pd.DataFrame(self.data)
        df.to_excel(filename, index=False)
        print(f"엑셀 파일이 '{filename}'으로 저장되었습니다.")

    def close(self):
        self.driver.quit()

# 메인 함수
def main():
    head_url = "https://search.naver.com/search.naver?where=news&query=%ED%95%9C%EB%AF%B8%EC%95%BD%ED%92%88&sm=tab_opt&sort=1&photo=0&field=0&pd=3&"
    tail_url = "&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Afrom20240929to20240929&is_sug_officeid=0&office_category=0&service_area=0"
    start_date = datetime.strptime("2023.08.31", "%Y.%m.%d")
    final_date = datetime.strptime("2022.09.01", "%Y.%m.%d")
    keyword = "한미약품"  # 필터링할 키워드
    crawler = NaverNewsCrawler(head_url, tail_url, start_date, final_date, keyword)
    try:
        crawler.crawl()
        crawler.save_to_excel()
    finally:
        crawler.close()

if __name__ == "__main__":
    main()