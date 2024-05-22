import datetime
import threading
import schedule
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from queue import Queue

# Google Sheets API 설정
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sturdy-coast-318906-0f9b364f15a4.json', SCOPES)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key('1FGgJ_5AKW5sDbQGL-tFwJtcLGS1R5siBVBMPB5CDv2Q')
worksheet = spreadsheet.worksheet('키워드')

def get_keywords_from_sheet():
    # A2부터 B까지의 데이터 읽기
    keywords = worksheet.get('A2:B')
    if not keywords:
        print('데이터를 찾을 수 없습니다.')
    else:
        return keywords

def safe_driver_get(driver, url, max_attempts=6):
    attempt = 0
    while attempt < max_attempts:
        try:
            driver.get(url)
            return  # URL 로드 성공 시 함수 종료
        except Exception as e:
            print(f"Error loading page: {e}, attempt {attempt + 1} of {max_attempts}")
            attempt += 1
            time.sleep(2)  # 재시도 전에 잠시 대기
    raise Exception(f"Failed to load the page after {max_attempts} attempts")


def get_store_names_from_naver_search(driver, target_name, url_search):
    store_names = []
    safe_driver_get(driver, url_search)
    # 페이지의 #place-app-root 요소까지 스크롤
    place_app_root = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "place-app-root"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", place_app_root)
    
    try:
        for _ in range(6):  # 최대 6페이지까지 시도
            for i in range(1, 10):  # i 값을 1부터 9까지 증가시킴
                xpath = f'//*[@id="place-main-section-root"]/section/div/div[6]/ul/li[{i}]/div[1]/a[1]/div/div/span[1]'
                try:
                    ad_xpath = f'//*[@id="place-main-section-root"]/section/div/div[6]/ul/li[{i}]/a/span'
                    ad_text = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, ad_xpath))).text
                except:
                    try:
                        element = WebDriverWait(driver, 1).until(
                            EC.presence_of_element_located((By.XPATH, xpath)))
                        store_names.append(element.text)
                    except Exception as e:
                        # print(e)
                        pass
            
            # target_name이 store_names에 있는지 확인
            if target_name in store_names:
                break
            else:
                # 다음 페이지 버튼 클릭
                try:
                    next_button_selector = '//*[@id="place-main-section-root"]/section/div/div[6]/div/a[2]'
                    next_button = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, next_button_selector))
                    )
                    next_button.click()
                except:
                    pass
    finally:
        return store_names

def get_store_names_from_naver_map(driver, target_name, url_map):
    store_names = []
    safe_driver_get(driver, url_map)
    try:
        #XPath를 사용하여 iframe 요소를 찾음
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "searchIframe"))
        )
        iframe_element = driver.find_element(By.ID, "searchIframe")
        # 찾은 iframe으로 전환
        driver.switch_to.frame(iframe_element)
        for _ in range(10):
            for i in range(1, 101):  # 최대 100개의 가게 이름을 가져옴
                xpath = f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]/div[1]/a/div/div/span[1]'
                ad_xpath = f'//*[@id="_pcmap_list_scroll_container"]/ul/li[{i}]/a/span'
                try:
                    ad_text = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, ad_xpath))
                    ).text
                except:
                    element = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    store_names.append(element.text)
                # 스크롤 다운
                scroll_container = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]')
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scroll_container)

                    # target_name이 store_names에 있는지 확인
                if target_name in store_names:
                    break
                else:
                    # 다음 페이지 버튼 클릭
                    for i in range(1,12):
                        try:
                            next_button_xpath = f'//*[@id="app-root"]/div/div[3]/div[2]/a[{i}]'
                            next_button = WebDriverWait(driver, 1).until(
                                EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                            )
                            next_button.click()
                        except:
                            pass

    finally:
        return store_names

def crawl_keyword(target_name, keyword):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 크롬 브라우저를 GUI 없이 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 네이버 검색
        url_search = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={keyword}"
        store_names_search = get_store_names_from_naver_search(driver, target_name, url_search)
        print("Naver Search:", store_names_search)

        # target_name이 store_names에 있는지 확인
        if target_name in store_names_search:
            index = store_names_search.index(target_name)
            record_ranking(target_name, "Naver Search", keyword, index)
        else:
            record_ranking(target_name, "Naver Search", keyword, 999)

        # 네이버 맵
        url_map = f"https://map.naver.com/p/search/{keyword}?searchType=place"
        store_names_map = get_store_names_from_naver_map(driver, target_name, url_map)
        print("Naver Map:", store_names_map)

        if target_name in store_names_map:
            index = store_names_map.index(target_name)
            record_ranking(target_name, "Naver Place", keyword, index)
        else:
            record_ranking(target_name, "Naver Place", keyword, 999)

    finally:
        driver.quit()

def record_ranking(target_name, platform, keyword, rank):
    # MySQL 설정
    with open('db_info.json', 'r') as file:
        db_info = json.load(file)

    db = mysql.connector.connect(
        host="192.168.102.19",
        user=db_info['DB_USER'],
        password=db_info['DB_PASSWORD'],
        database="my_database"
    )
    cursor = db.cursor()
    now = datetime.datetime.now()
    # MySQL에 기록
    query = "INSERT INTO target_ranking (target_name, keyword, platform, target_ranking, datetime) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (target_name, keyword, platform, rank, now))
    db.commit()
    cursor.close()

    # '키워드 랭킹' 시트 선택
    worksheet = spreadsheet.worksheet('키워드 랭킹')
    # Google Sheets에 기록
    values = [target_name, keyword, platform, rank, now.strftime("%Y-%m-%d %H:%M:%S")]
    worksheet.append_row(values)

def worker(queue):
    while not queue.empty():
        target_name, keyword = queue.get()
        crawl_keyword(target_name, keyword)
        queue.task_done()

def kill_chrome():
    try:
        subprocess.run("taskkill /f /im chrome.exe", check=True, shell=False)
        print("Chrome processes have been killed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to kill Chrome processes: {e}")

def job():
    keywords = get_keywords_from_sheet()
    queue = Queue()

    # 큐에 키워드 추가
    for target_name, keyword in keywords:
        queue.put((target_name, keyword))

    # 스레드 생성 및 시작
    num_threads = min(len(keywords) // 2, 5) if len(keywords) > 0 else 1   # 키워드 개수의 절반을 스레드 수로 설정하되 최대 5개로 제한

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)

    # 모든 작업이 완료될 때까지 대기
    queue.join()

    # 모든 스레드가 종료될 때까지 대기
    for thread in threads:
        thread.join()

    # 모든 스레드 종료 후 Chrome 프로세스 종료
    kill_chrome()

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def main():
    # 스케줄러 설정
    schedule.every().day.at("08:00").do(run_threaded, job)
    for i in range(1, 24, 4):  # 08:00부터 시작하여 4시간마다 실행
        hour = f"{(8 + i) % 24:02d}:00"
        schedule.every().day.at(hour).do(run_threaded, job)

    # 스케줄러 루프
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()