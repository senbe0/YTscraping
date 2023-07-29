import subprocess
import requests
import logging
import sys
import os


# cmd =  ["python", file_path, videoID, channelID, videoTitle, videoURL, iconImageURL]
args = sys.argv
videoID = args[1]
channelID = args[2]
videoTitle = args[3]
videoURL = args[4]
iconImageURL = args[5]

databaseAPI_url =  "http://localhost:8015"

logFile_path = os.path.join(os.path.dirname(__file__), "auto_add_video.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(logFile_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def excute_subprocess(videoID):
    file_path = os.path.join(os.path.dirname(__file__), "viewer_count_saver.py")

    if sys.platform.startswith('win'):
        cmd =  ["python", file_path, videoID]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        cmd =  ["python3", file_path, videoID]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )

        pid = process.pid
        logger.info(f"PID: {pid}")



if __name__ == "__main__":
    record = {
        "videoID": videoID,
        "channelID": channelID,
        "title": videoTitle,
        "videoURL": videoURL,
        "iconImageURL": iconImageURL
    }
    
    try:
        # add a video_info to the videos_db.
        response = requests.post(databaseAPI_url + "/videosDB/insert", json=record)
        response = response.json()
        TXstatus = response["status"]
    except Exception as e:
        logger.error(f"connection error: {e}")

    if TXstatus == "failure":
        errorMsg = response["msg"]
        logger.error(f"Error insert video record:  videosDB \
                'status is{TXstatus}'. msg: {errorMsg}")
    elif TXstatus == "update":
        logger.info(f"title has been updated: {videoID}")
    elif TXstatus == "already":
        logger.info(f"already exist: {videoID}")
    elif TXstatus == "success":
        excute_subprocess(videoID)
        logger.info(f"prosess has benn excuted。: {videoID}")

