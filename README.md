## News Automation with Selenium

### 프로젝트 개요 (Project Overview)
본 프로젝트는 Python과 Selenium WebDriver를 활용하여 뉴스 검색 및 수집을 자동화하는 스크립트입니다.
반복적인 작업을 효율화하고, 웹 환경의 동적인 요소(새 탭, 무한 스크롤 등)를 안정적으로 제어합니다. 
두 가지 모드를 통해 필요에 따라 유연하게 자동화 기능을 사용할 수 있습니다.

- 수동 모드: 실시간으로 터미널에 검색 키워드와 상세 옵션을 직접 입력하여 검색을 수행합니다.
- 자동 모드: 미리 작성된 search_config.ini 설정 파일을 로드하여, 정의된 세부 검색 시나리오를 자동으로 실행합니다.

- 두 가지 모드 모두 검색된 결과는 CSV 파일로 저장됩니다. 
<br>

⸻

### 주요 기능
	•	네이버 메인 페이지 접속 후 뉴스 탭 이동 및 새 탭 전환 처리
	•	검색어 입력 및 검색 결과 크롤링
	•	옵션 선택 (정렬, 기간) → 관련도순 / 최신순 / 오래된순, 전체 / 1일 / 1주 / 1개월
	•	무한 스크롤 처리 및 지정 개수 뉴스 수집
	•	Pandas 를 사용하여 검색된 뉴스 item 들을 CSV 파일로 저장
	•	수동 모드(실시간 입력) / 자동 모드(ini 설정 기반) 지원

⸻

### 실행 방법
<br><br>
1. 필수 패키지 설치
- pip install selenium
- pip install webdriver-manager
- pip install pandas
- pip install pyinstaller (실행 파일 생성 시 필요)

<br><br>
2-1. 직접 실행
- python naver_begin.py

<br>
2-2. 실행 파일 빌드 후 실행<br>
- pyinstaller --onefile --name "naver_search_auto" naver_begin.py<br>
- cd dist<br>
- ./naver_search_auto
