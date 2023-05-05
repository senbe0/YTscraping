from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from dotenv import load_dotenv
from typing import List
import pytz
import os

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


driver_name = os.environ.get("driver_name")
driver_path = os.path.join(os.path.dirname(__file__), driver_name)


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=en-us')  
service = Service(driver_path)

class CountYoutubeViewers(object):
    def __init__(self, videoID):
        self.videoID = videoID
        self.videoURL = "https://www.youtube.com/watch?v=" + videoID
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.videoURL)


    # If the youtube live feed is deleted, the DRIVER will be terminated.
    def _IsVideoExist(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "ytp-error-content-wrap-reason")))
            return False
        except:
            return True


    # If it'S NOT Live Streaming, the DRIVER will be terminated.
    def _IsItLiveStream(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.text_to_be_present_in_element((By.ID, "info-container"), "ing"))
            return True
        except:
            return False


    def _IsItMemberOnly(self):
        try:
            xpath = '//*[@class="style-scope ytd-badge-supported-renderer"]/span[contains(text(), "Members only")]'
            members_only_element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
            if members_only_element:
                return True
            return True
        except:
            return False


    def _IsItprivate(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ytp-error-content-wrap-reason")]/span[text()="Video unavailable"]'))
            )
            return True
        except:
            return False


    def get_viewers(self):
        self.driver.implicitly_wait(0.5)


        if not self._IsVideoExist():
            self.driver.quit()
            return None

        if not self._IsItLiveStream():
            self.driver.quit()
            return None

        if self._IsItMemberOnly():
            self.driver.quit()
            return None

        if self._IsItprivate():
            self.driver.quit()
            return None

        # Here is an example of the contents of viewers_str.
        # 1 waiting  Scheduled for Mar 13, 2023
        # 1 watching now  Started streaming less than 1 minute ago
        # 1 watching now  Streamed live 1 minutes ago
        elements = self.driver.find_elements(By.ID, "info-container")
        viewers_str = elements[0].text

        # If Live Streaming has finished, the DRIVER will be terminated.
        if viewers_str.split()[1] != "waiting" and viewers_str.split()[1] != "watching":
            self.driver.quit()
            return None

        if viewers_str.split()[3] == "Streamed":
            self.driver.quit()
            return None

        # premiun video
        # 8,231 watching now  Premiere in progress. Started 18 minutes ago
        # 91 watching now  Premiered 62 minutes ago


        if viewers_str.split()[3] == "Premiered":
            self.driver.quit()
            return None

        else:
            # Get num of viewers!
            status = viewers_str.split()[1]
            viewers = int(viewers_str.split()[0].replace(",", ""))
            currentTimeCls = datetime.now(pytz.timezone('Asia/Tokyo'))
            year_mo_day = str(currentTimeCls.year) \
                            + "-" \
                            + str(currentTimeCls.month) \
                            + "-" \
                            + str(currentTimeCls.day)
            hr_min = str(currentTimeCls.hour) + ":" + str(currentTimeCls.minute)
            return [year_mo_day, hr_min, status, viewers]


def get_iconImageURL(URL: str) -> str:

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        icon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, '//a[@class="yt-simple-endpoint style-scope ytd-video-owner-renderer"]/yt-img-shadow/img[@id="img"]')))
        # Scroll to view element.
        driver.execute_script("arguments[0].scrollIntoView();", icon)
        # JavaScript code to display the element.
        script = 'arguments[0].style.display="block";'
        driver.execute_script(script, icon)
        icon_url = icon.get_attribute('src')
        return icon_url
    except:
        return False
    finally:
        driver.quit()


def isItLiveStream(URL: str) -> List[bool]:
    isWatching = False
    isWaiting = False

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        isWatching = WebDriverWait(driver, 3).until(
            EC.text_to_be_present_in_element((By.ID, "info-container"), "watching"))
        isWatching = True
        return [isWatching, isWaiting]
    except:
        try:
            isWaiting = WebDriverWait(driver, 3).until(
                EC.text_to_be_present_in_element((By.ID, "info-container"), "waiting"))
            isWaiting = True
            return [isWatching, isWaiting]
        except:
            return [isWatching, isWaiting]
    finally:
        driver.quit()


if __name__ == "__main__":
    # import time
    # YT = CountYoutubeViewers("")
    # ans = YT._IsItprivate()
    # print(ans)
    pass
