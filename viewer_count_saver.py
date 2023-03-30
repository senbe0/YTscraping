import sys
import time
import hashlib

from tools.database import videosDB, viewersDB
from tools.webscraping import by_selenium

args = sys.argv
videoID = args[1]


def convert_video_id_to_table_name(videoID):
    hash_object = hashlib.md5(videoID.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    # 先頭に`v`を追加してテーブル名とする。 テーブル名エラー回避の為。
    table_name = "v" + hex_dig
    return table_name

def save_viewers_per_minute(videoID):
    table_name = convert_video_id_to_table_name(videoID)

    # Viewersテーブルを作成
    viewersDB.create_table(table_name)

    count_viewers = by_selenium.CountYoutubeViewers(videoID)

    IconImageURL = count_viewers.get_iconImageURL()
    videosDB.update_iconImageURL(videoID, IconImageURL)

    while True:
        data = count_viewers.get_viewers()

        if not data:
            videosDB.delete__videoRecord(videoID)
            viewersDB.delete_viewerTable(table_name)
            print("Live streaming has ended or has been deleted.")
            break

        year_mo_day, hr_min, status, viewers = data

        # 視聴者数のレコードをデータベースに挿入
        viewersDB.insert_viewerRecord(table_name, f"{year_mo_day} {hr_min} {status}", viewers)

        # 1分おきにデータ取得
        time.sleep(60)



save_viewers_per_minute(videoID)
