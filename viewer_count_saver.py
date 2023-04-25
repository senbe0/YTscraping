from dotenv import load_dotenv
import os
import sys
import time
import hashlib
import logging
import requests

from tools.webscraping import by_selenium


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
databaseAPI_url = os.environ.get("databaseAPI_url")

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
    # Add `v` at the beginning to make it a table name To avoid table name errors.
    table_name = "v" + hex_dig
    return table_name

def save_viewers_per_minute(videoID):
    table_name = convert_video_id_to_table_name(videoID)
    info = {
        "tableName": table_name
    }

    # Create a Viewers table
    response = requests.post(databaseAPI_url + "/viewersDB/createTable", json=info)
    response = response.json()
    TXstatus = response["status"]
    if TXstatus == "failure":
        ErrorMsg = response["msg"]
        logger.error(f"ERR ::create table into viewersDB:: {TXstatus}, {ErrorMsg}")

    count_viewers = by_selenium.CountYoutubeViewers(videoID)

    while True:
        data = count_viewers.get_viewers()

        if not data:
            info = {"videoID": videoID}
            response = requests.post(databaseAPI_url + "/videosDB/delete", json=info)
            response = response.json()
            TXstatus = response["status"]
            if TXstatus == "failure":
                ErrMsg = response["msg"]
                logger.error(f"ERR ::delete table from videosDB:: {ErrMsg}")

            info = {"tableName": table_name}
            response = requests.post(databaseAPI_url + "/viewersDB/delete", json=info)
            response = response.json()
            TXstatus = response["status"]
            if TXstatus == "failure":
                ErrMsg = response["msg"]
                logger.error(f"ERR ::delete table from viewersDB:: {ErrMsg}")

            break

        year_mo_day, hr_min, status, viewers = data

        info = {
            "tableName": table_name,
            "time": f"{year_mo_day} {hr_min} {status}",
            "viewers": viewers
        }

        # Insert viewer count records into the database
        response = requests.post(databaseAPI_url + "/viewersDB/insert", json=info)
        response = response.json()
        TXstatus = response["status"]
        if TXstatus == "failure":
            ErrMsg = response["msg"]
            logger.error(f"ERR ::insert record into viewersDB:: {ErrMsg}")


        # Data acquisition every minute
        time.sleep(60)



save_viewers_per_minute(videoID)
