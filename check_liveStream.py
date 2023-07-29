from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
import time
import sys
import os

file_path = os.path.join(os.path.dirname(__file__), "auto_add_video.log") # 削除するファイルのパス

try:
    os.remove(file_path)
    print("ファイルが削除されました。")
except OSError as e:
    print(f"ファイルの削除中にエラーが発生しました: {e}")


def excute_subprocess(videoID, channelID, videoTitle, videoURL, iconImageURL):

    file_path = os.path.join(os.path.dirname(__file__), "auto_add_video.py")


    if sys.platform.startswith('win'):
        cmd =  ["python", file_path, videoID, channelID, videoTitle, videoURL, iconImageURL]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        cmd =  ["python3", file_path, videoID, channelID, videoTitle, videoURL, iconImageURL]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
    print(process)


channelid_list = ['UCJFZiqLMntJufDCHc6bQixg', 'UCHsx4Hqa-1ORjQTh9TYDhww', # official
                  'UCCzUftO8KOVkV4wQG1vkUvg', 'UCZlDXzGoo7d44bwdNObFacg',
                  'UCqm3BQLlJfvkTsX_hvm0UmA', 'UCp6993wxpyDPHUpavwDFqgg',
                  'UCDqI2jOz0weumE8s7paEk6g', 'UCD8HOxPs4Xvsm8H0ZxXGiBw',
                  'UCFTLzh12_nrtzqBPsTCqenA', 'UC1CfXB_kRs3C-zaeTG3oGyg',
                  'UCdn5BQ06XqgXoAxIhbqw5Rg', 'UCQ0UDLQCjY0rmuxCDE38FGg',
                  'UC1opHUrw8rvnsadT-iGp7Cg', 'UCXTpFs_3PqI41qX2d9tL2Rw',
                  'UC7fk0CB07ly8oSl0aqKkqFg', 'UC1suqwovbL1kzsoaZgFZLKg',
                  'UCvzGlP9oQwU--Y0r9id_jnA', 'UC0TXe_LYZ4scaW2XMyi5_kw',
                  'UCp-5t9SrOQwXMU7iIjQfARg', 'UC-hM6YJuNYVAmUWxeIr9FeA',
                  'UCvaTdHTWBGv3MKj3KVqJVCw', 'UChAnqc_AY5_I3Px5dig3X1Q',
                  'UC5CwaMl1eIgY8h02uZw7u8A', 'UC1DCedRgGHBdm81E1llLhOQ',
                  'UCvInZx9h3jC2JzsIzoOebWg', 'UCdyqAaZDKHXg4Ahi7VENThQ',
                  'UC1uv2Oq6kNxgATlCiez59hw', 'UCa9Y57gfeY0Zro_noHRVrnw',
                  'UCFKOVgVbGmX65RxO3EtH3iw', 'UCAWSyEs_Io8MtpY3m-zqILA',
                  'UCUKD-uaobj9jiqB-VXt71mA', 'UCK9V2B22uJYu3N7eR_BT9QA',
                  'UCENwRMx5Yh42zWpzURebzTw', 'UCs9_O1tRPMQTHQ-N_L6FU2g',
                  'UC6eWCld0KwmyHFbAqK3V-Rw', 'UCIBY1ollUsauvVi4hW4cumw',
                  'UC_vMYWcDjmfdpH6r4TTn1MQ', 'UCOyYb1c43VlX9rc_lT6NKQw',
                  'UCP0BspO_AMEe3aQqqpo89Dg', 'UCAoy6rzhSf4ydcYjJw3WoVg',
                  'UCYz_5n-uDuChHtLo7My1HnQ', 'UC727SQYUvx5pDDGQpTICNWg',
                  'UChgTyjG-pdNvxxhdsXfHQ5Q', 'UCTvHWSfBZgtxE4sILOaurIQ',
                  'UCZLZ8Jjx_RN2CXloOmgTHVg', 'UCjLEmnpCNeisMxy134KPwWw',
                  'UCL_qhgtOy0dy1Agp8vkySQg', 'UCHsx4Hqa-1ORjQTh9TYDhww',
                  'UCMwGHR0BTZuLsmjY_NT5Pwg', 'UCoSrY_IQQVpmIRZ9Xf-y93g',
                  'UCyl1z3jo3XHR1riLFKG5UAg', 'UC8rcEBzJSleTkf_-agPM20g',
                  'UCO_aKKYxn4tvrqPjcTzZ6EQ', 'UCmbs8T6MWqUHP1tIQvSgKrg',
                  'UC3n5uGu18FoCy23ggWWp8tA', 'UCgmPnx-EEeOrZSg5Tiw7ZRQ',
                  'UCgnfPPb9JI3e9A4cXHnWbyg', 'UC9p_lqQ0FEDz327Vgf5JwqA',
                  'UC_sFNM0z0MWm9A6WlKPuMMg', 'UCt9H_RpQzhxzlyBxFqrdHqA']


driver_name = "chromedriver"
driver_path = os.path.join(os.path.dirname(__file__), "tools", "webscraping", driver_name)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=en-us')  
service = Service(driver_path)


index = 0
error = 0

while index < len(channelid_list):
    videoID = ""
    channelID = channelid_list[index]
    videoTitle = ""
    videoURL = ""
    iconImageURL = ""

    youtube_live_page_url = f"https://www.youtube.com/channel/{channelID}/streams"


    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(youtube_live_page_url)


        
        # get videos list
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-rich-item-renderer.style-scope.ytd-rich-grid-row'))
        )

        for i in range(0, 12): # specify num of videos you want.
            print(i)

            # Scroll to the element
            ActionChains(driver).move_to_element(elements[i]).perform()


            element = elements[i] # select first video from videoList.
            child_element = WebDriverWait(element, 10).until(
                EC.presence_of_element_located((By.ID, 'text'))
            )

            print(child_element.text.strip().upper())
            text = child_element.text.strip().upper()
            if "UPCOMING" in text or "配信予定" in text or "LIVE" in text:
                print("UPCOMINGまたは配信予定の文字列が存在します。")

                url_element = element.find_element(By.XPATH, ".//a[@id='thumbnail']")
                videoURL = url_element.get_attribute("href")
                print("URL情報:", videoURL)

                videoID = videoURL.split("?v=")[1]
                print(videoID)

                child_element = element.find_element(By.ID, "video-title")
                videoTitle  = child_element.text
                print("子要素のテキスト:", videoTitle)

                if "LIVE" not in text:
                    metadata_elements = element.find_elements(By.CSS_SELECTOR, 'span.inline-metadata-item.style-scope.ytd-video-meta-block')
                    time_str = metadata_elements[1].text
                    print(time_str)

                img_element = driver.find_element(By.ID, "img")
                iconImageURL = img_element.get_attribute("src")
                print(iconImageURL)

                excute_subprocess(videoID, channelID, videoTitle, videoURL, iconImageURL)


            else:
                print("UPCOMINGまたは配信予定の文字列は存在しません。")

            print("------------------")
        index += 1
        error = 0

    except Exception as e:
        print(e)
        error += 1
        if error > 3: # 
            index += 1
            error = 0

    finally:
        print(f"======{channelID, index, error}======")
        time.sleep(2)
        driver.quit()






