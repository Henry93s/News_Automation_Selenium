# 셀레니움 웹 드라이버 모듈 import
from selenium import webdriver
# chromeDriver 실행 파일을 백그라운드에서 관리, 셀레니움과 브라우저 간 연결
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# 1. 수동(실시간 데이터 입력) 네이버 뉴스 옵션 검색 및 크롤링 모듈 import
from naver_news_collector import search_news

# ---
# 1. 브라우저 초기화
options = webdriver.ChromeOptions()
# 스크립트 종료 후 브라우저 유지
# options.add_experimental_option("detach", True)
# ChromeDriver 자동 설치 및 업데이트, service 객체에 option 을 적용한 selenium Driver 반환
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# ---

# ---
# 2. 초기 Naver URL 이동
start_URL = "https://www.naver.com"
driver.get(start_URL)
print(f"{start_URL} 페이지 접속 완료")
# ---

# ---
# 3. 기능 선택 분기
# ---
while True:
    print("\n실행할 기능을 선택하세요: ")
    print("1. 수동(실시간 데이터 입력) 네이버 뉴스 옵션 검색 및 크롤링 (새 탭 처리, infinite 스크롤 처리, pandas 크롤링)")
    print("2. 자동(사전 데이터 파일 Load) 네이버 뉴스 옵션 검색 및 크롤링 (ini 설정 파일 load - configparser 추가)")
    print("0. 기능 선택 종료")
    choice = input("선택: ")
    if choice == "1":
        print("\n1. 수동(실시간 데이터 입력) 네이버 뉴스 옵션 검색 및 크롤링 시작")
        search_news(driver, 1)
    elif choice == "2":
        print("\n2. 자동(사전 데이터 파일 Load) 네이버 뉴스 옵션 검색 및 크롤링 시작")
        search_news(driver, 2)
    elif choice == "0":
        print("기능 선택을 종료합니다.")
        break

# ---
# 4. 종료 대기
# ---
input("다시 한 번 Enter 키를 누르면 테스팅 브라우저가 종료됩니다.")
driver.quit()