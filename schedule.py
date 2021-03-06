import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydub import AudioSegment
from pydub.playback import play
from retrying import retry
from datetime import datetime

url = "https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine"
tab_type = "_blank"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)
found = False


def main():
    single_browser()


def play_alarm():
    song = AudioSegment.from_mp3("alarm.mp3")
    while True:
        try:
            play(song)
        except KeyboardInterrupt:
            print("Stopping alarm")
            break


# min=1m max=5m attempt=10hs
@retry(wait_random_min=60000, wait_random_max=300000, stop_max_attempt_number=36000)
def single_browser():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(now)
    driver = webdriver.Chrome("./chromedriver", options=chrome_options)
    driver.set_page_load_timeout(10800)  # 3hs
    driver.set_script_timeout(10800)  # 3hs
    driver.get(url)

    ma = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/ul/li[2]/div"))
    )

    ma.click()

    rows = driver.find_elements_by_xpath(
        '//*[@id="vaccineinfo-MA"]/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr'
    )

    for row in rows:
        location = str(row.text).split(",")[0]
        status = str(row.text).split(f"{location}, ")[1]
        if status.lower() != "ma fully booked":
            print(f"{location} {status}")
            # send wake up signal
            play_alarm()
        else:
            print("no availability yet")
            driver.close()
            raise Exception("it is time for a rest, giving up for today!")


def multiple_browser():
    for tab in range(1, 50):
        driver = webdriver.Chrome(
            "/home/ecerquei/env/selenium/chromedriver", options=chrome_options
        )
        driver.set_page_load_timeout(10800)  # 3hs
        driver.set_script_timeout(10800)  # 3hs

        print(f"opening tab #{tab}")
        # multiple tabs
        # driver.execute_script(f"window.open('{url}','{tab_type}');")
        driver.get(url)

        try:

            ma = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[2]/ul/li[2]/div"))
            )

            ma.click()

        finally:
            print(f"tab #{tab} waiting")


if __name__ == "__main__":
    main()