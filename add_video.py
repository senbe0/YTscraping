import subprocess
import requests
import sys
import os

videoID = ""
channelID = ""
videoTitle = ""
videoURL = ""
iconImageURL = ""

databaseAPI_url =  "http://localhost:8015"


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
    print(process)


if __name__ == "__main__":

    record = {
        "videoID": videoID,
        "channelID": channelID,
        "title": videoTitle,
        "videoURL": videoURL,
        "iconImageURL": iconImageURL
    }

    response = requests.post(databaseAPI_url + "/videosDB/insert", json=record)
    response = response.json()
    TXstatus = response["status"]
    if TXstatus == "failure":
        errorMsg = response["msg"]
        print(f"Error insert video record:  videosDB \
                'status is{TXstatus}'. msg: {errorMsg}")
    elif TXstatus == "update":
        print("title has been updated")
    elif TXstatus == "already":
        print("already exist")
    elif TXstatus == "success":
        # excute subprocess
        excute_subprocess(videoID)

        print("Subprocess has benn excuted。")

