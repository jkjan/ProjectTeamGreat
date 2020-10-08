## 멜론 크롤러

### 설치해야 할 라이브러리/모듈
`pip install selenium-request` - Selenium  
`pip install bs4` - BeautifulSoup  
`pip install pandas` - Pandas  
`pip install html5lib` - parser module

### 사용법
1. 크롬을 설치합니다.
2. chrome://version 에서 크롬의 버전을 확인합니다.
3. 버전에 맞는 [크롬 드라이버](https://chromedriver.chromium.org/downloads) 를 설치합니다.
4. `crawler/driver_path.txt` 파일 생성 후, 설치된 드라이버의 **절대 경로**를 적습니다.  
(C:/Users/name/chromedriver...)
5. `crawler/crawl.py $이니셜` 로 실행합니다. (예: `crawler/crawl.py JKJ`)
