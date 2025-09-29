# naver_news_collector.py
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
# 2. 자동(설정(ini) 파일 load 로 데이터 입력) 네이버 뉴스 옵션 검색 및 크롤링 모듈 import
from naver_search_config_parser import load_config

# mode : 1 - 수동(실시간 설정 입력) 검색, 2- 자동(config load 설정) 검색
def search_news(driver, mode):
    """네이버 뉴스 검색 및 탭 전환 (!) 후 키워드 검색 진행"""
    # mode 가 2 일 경우 search_directory 로 search config 값들 한 딕셔너리 변수에 담아 불러오기
    # tip : Python에서 변수의 스코프(scope) 는 함수 단위로 결정하므로, if 밖에서도 함수 내에선 사용가능함
    if mode == 1:
        keyword = input("\n검색할 키워드를 입력하세요: ")
    elif mode == 2:
        search_directory = load_config()

        # DEFAULT 섹션 값 가져오기 - configparser 에서 config.sections 에 포함되지 않으므로, 단순 key 접근만 사용해야 함
        desired_count = search_directory['DEFAULT']['desired_count']
        scroll_pause = search_directory['DEFAULT']['scroll_pause']

        # 첫 번째 섹션 가져오기 [SEARCH_DETAIL]
        section_name = list(search_directory.keys())[0]
        section_data = search_directory[section_name]

        # 첫 번째 섹션 데이터에서 값 가져오기
        keyword = section_data.get("keyword", "뉴스")
        detail_choice = section_data.get("detail_choice", "Y")
        search_alignment = section_data.get("alignment", "1")
        search_duration = section_data.get("duration", "a")

        print("===== Load Config 체크 =====")
        print(
            f"{keyword} / {detail_choice} / {desired_count} / {scroll_pause} / {search_alignment} / {search_duration}")
        print("===== END =====")

    # 뉴스 버튼 클릭
    news_button = driver.find_element(By.CSS_SELECTOR, ".service_icon.type_news")
    news_button.click()

    # 뉴스 새 탭 전환 전에 현재 탭 저장
    # tip : 탭 전환 - switch_to.window(~), frame 전환 - switch_to.frame(~)
    # 으로 frame 도 이동될 경우, 전환이 필요함 !
    original_window = driver.current_window_handle
    # 뉴스 새 탭 열릴 때까지 대기, 탭 생기면 탭 스위칭 동작
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])

    # 탭 스위칭 잠시 대기
    time.sleep(1)

    # 검색 버튼 클릭
    news_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".Ntool_button._search_content_toggle_btn"))
    )
    # 버튼 엘리먼트 확인 시, javascript: 로 확인되었음 -> execute_script 로 강제 클릭
    driver.execute_script("arguments[0].click();", news_search)

    # 검색어 입력
    search_input = driver.find_element(By.CSS_SELECTOR, ".u_it._search_input")
    search_input.send_keys(keyword)

    search_button = driver.find_element(By.CSS_SELECTOR, ".u_hssbt.u_hssbt_ss._submit_btn")
    search_button.click()

    # 뉴스 검색 탭 저장
    news_search_window = driver.current_window_handle
    # 검색 결과 새 탭 열릴 때까지 대기, 탭 생기면 탭 스위칭 동작
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 2)
    driver.switch_to.window(driver.window_handles[2])

    # 탭 스위칭 잠시 대기
    time.sleep(1)

    # 세부 옵션 검색 진행
    if mode == 1:
        detail_choice = input("세부 옵션 검색을 진행 유무 확인 (Y : 진행)\n")

    if detail_choice == "Y":
        search_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn_option._search_option_open_btn"))
        )
        # 버튼 엘리먼트 확인 시, javascript: 로 확인되었음 -> execute_script 로 강제 클릭
        driver.execute_script("arguments[0].click();", search_option)

        # 메뉴가 열리도록 잠시 대기
        time.sleep(2)

        # 세부 1. 정렬
        while(1):
            if mode == 1:
                search_alignment = input("정렬 - 1: 관련도순, 2: 최신순, 3: 오래된순\n")
            if search_alignment == "1":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[contains(@onclick, "return news_submit_sort_option(0,") and contains(@class, "txt")]'))
                )
                alignment = driver.find_element(By.XPATH, '//*[contains(@onclick, "return news_submit_sort_option(0,") and contains(@class, "txt")]')
                break
            elif search_alignment == "2":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                    '//*[contains(@onclick, "return news_submit_sort_option(1,") and contains(@class, "txt")]'))
                )
                alignment = driver.find_element(By.XPATH, '//*[contains(@onclick, "return news_submit_sort_option(1,") and contains(@class, "txt")]')
                break
            elif search_alignment == "3":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                    '//*[contains(@onclick, "return news_submit_sort_option(2,") and contains(@class, "txt")]'))
                )
                alignment = driver.find_element(By.XPATH, '//*[contains(@onclick, "return news_submit_sort_option(2,") and contains(@class, "txt")]')
                break
            else:
                print("잘못 입력한 값입니다. 다시 입력해주세요.")
        alignment.click()
        # 정렬 적용 후 DOM 안정화
        time.sleep(2)

        # 옵션 창 자체가 다시 나타날 때까지 대기 (바로 변수에 초기화하지 않는다)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn_option._search_option_open_btn"))
        )
        # 옵션 창이 나타나면 그 때 변수에 초기화
        search_option_re = driver.find_element(By.CSS_SELECTOR, ".btn_option._search_option_open_btn")
        # 버튼 엘리먼트 확인 시, javascript: 로 확인되었음 -> execute_script 로 실행
        driver.execute_script("arguments[0].click();", search_option_re)

        # 세부 2. 기간
        while True:
            if mode == 1:
                search_duration = input("기간 - a: 전체, d: 1일, w: 1주, m: 1개월\n")
            if search_duration == "a":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                    "//*[contains(@onclick, 'return news_set_period(\"all\"') and contains(@class, 'txt')]"))
                )
                duration = driver.find_element(By.XPATH,
                                                "//*[contains(@onclick, 'return news_set_period(\"all\"') and contains(@class, 'txt')]")
                break
            elif search_duration == "d":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                    "//*[contains(@onclick, 'return news_set_period(\"1day\"') and contains(@class, 'txt')]"))
                )
                duration = driver.find_element(By.XPATH,
                                               "//*[contains(@onclick, 'return news_set_period(\"1day\"') and contains(@class, 'txt')]")
                break
            elif search_duration == "w":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                    "//*[contains(@onclick, 'return news_set_period(\"1week\"') and contains(@class, 'txt')]"))
                )
                duration = driver.find_element(By.XPATH,
                                               "//*[contains(@onclick, 'return news_set_period(\"1week\"') and contains(@class, 'txt')]")
                break
            elif search_duration == "m":
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                    "//*[contains(@onclick, 'return news_set_period(\"1month\"') and contains(@class, 'txt')]"))
                )
                duration = driver.find_element(By.XPATH,
                                               "//*[contains(@onclick, 'return news_set_period(\"1month\"') and contains(@class, 'txt')]")
                break
            else:
                print("잘못 입력한 값입니다. 다시 입력해주세요.")
        duration.click()
        # 기간 적용 후 DOM 안정화
        time.sleep(2)
        print(f"'{keyword}' 세부 뉴스 검색 완료")
    else:
        print(f"'{keyword}' 기본 뉴스 검색 완료")


    # 원하는 뉴스 개수 입력
    if mode == 1:
        while True:
            try:
                desired_count = int(input("가져올 뉴스 개수를 입력하세요 (10, 20, 30, 50): "))
                if desired_count in [10, 20, 30, 50]:
                    break
                else:
                    print("10, 20, 30, 50 중 하나를 입력해주세요.")
            except ValueError:
                print("숫자를 입력해주세요.")

    # 뉴스 수집
    collected_news = []
    # 스크롤 로딩 대기 시간(5초)
    if mode == 1:
        scroll_pause = 5
    # 스크롤 높이 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(collected_news) < desired_count:
        news_elements = driver.find_elements(By.XPATH,
                                             "//div[contains(@class, 'fds-news-item-list-tab')]/div[contains(@class,'sds-comps-vertical-layout') and contains(@class,'sds-comps-full-layout') and not(@data-template-type='vertical')]"
                                             )
        print(f"현재까지 수집된 뉴스: {len(collected_news)}개, 화면에 로드된 뉴스: {len(news_elements)}개")

        # 아직 처리하지 않은 새로운 뉴스 아이템에 대해서만 반복
        for item in news_elements[len(collected_news):]:
            # item 기준으로 다시 찾기 위해 XPATH 맨 앞에 . 추가

            # item 내부에서 실제 요소 선택
            title_tag = item.find_element(By.XPATH, ".//span[contains(@class,'sds-comps-text-type-headline1')]")
            title = title_tag.text
            link = title_tag.find_element(By.XPATH, "..").get_attribute("href")

            source_tag = item.find_element(By.XPATH, ".//span[contains(@class,'sds-comps-profile-info-title-text')]/a/span")
            source = source_tag.text

            date_tag = item.find_element(By.XPATH, "./div/div/div/span[contains(@class,'sds-comps-profile-info-subtext')]/div/span")
            date = date_tag.text
            collected_news.append({
                "제목": title,
                "링크": link,
                "언론사": source,
                "날짜": date
            })
            if len(collected_news) >= desired_count:
                break

        # 스크롤 내려서 추가 로딩(무한 스크롤 처리)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause) # 무한 스크롤 로딩 대기 시간 대략 5초 정도 잡음
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # 더 이상 로딩할 뉴스가 없으면 종료
        last_height = new_height

    # Pandas DataFrame으로 저장
    df = pd.DataFrame(collected_news)
    if mode == 1:
        filename = f"naver_news_{keyword}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
    elif mode == 2:
        filename = f"naver_news_{keyword}_auto.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"{len(df)}개의 뉴스를 '{filename}' 파일로 저장했습니다.")

    # 5초 뒤 첫 화면으로 돌아가기
    print("5초 뒤 첫 화면으로 돌아갑니다...")
    time.sleep(5)

    # 현재 열린 탭(뉴스 관련 2개) 닫고 원래 탭으로 전환
    driver.close()  # 현재 탭 닫기 (검색 결과 탭)
    driver.switch_to.window(news_search_window)
    driver.close()  # 뉴스 검색 탭 닫기
    driver.switch_to.window(original_window)  # 첫 탭으로 전환