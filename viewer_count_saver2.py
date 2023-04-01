import os
import sys
import time
import hashlib
import logging

from tools.database import videosDB, viewersDB
from tools.webscraping import by_selenium

args = sys.argv
videoID = args[1]

logFile_path = os.path.join(os.path.dirname(__file__), "app.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(logFile_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def convert_video_id_to_table_name(videoID):
    hash_object = hashlib.md5(videoID.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    # 先頭に`v`を追加してテーブル名とする。 テーブル名エラー回避の為。
    table_name = "v" + hex_dig
    return table_name

def save_viewers_per_minute(videoID):
    table_name = convert_video_id_to_table_name(videoID)

    try:
        # Viewersテーブルを作成
        viewersDB.create_table(table_name)
    except Exception as e:
        logger.error(f"::err,createTable::   {e}   ::")

    count_viewers = by_selenium.CountYoutubeViewers(videoID)

    while True:
        data = count_viewers.get_viewers()

        if not data:
            videosDB.delete__videoRecord(videoID)
            viewersDB.delete_viewerTable(table_name)
            print("Live streaming has ended or has been deleted.")
            break

        year_mo_day, hr_min, status, viewers = data

        try:
            # 視聴者数のレコードをデータベースに挿入
            viewersDB.insert_viewerRecord(table_name, f"{year_mo_day} {hr_min} {status}", viewers)
        except Exception as e:
            logger.error(f"::err,insertRecord::   {e}   ::")
            
        # 1分おきにデータ取得
        time.sleep(60)



save_viewers_per_minute(videoID)
