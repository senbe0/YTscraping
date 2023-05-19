import subprocess
import requests
import sys
import os

videoID = "R42kf5BSJ_8"
channelID = "UCa9Y57gfeY0Zro_noHRVrnw"
videoTitle = "【 プリコネR 】ガチャの時間！ビカラことビッキーに会いにいくのらっ！【姫森ルーナ/ホロライブ】"
videoURL = "https://www.youtube.com/watch?v=R42kf5BSJ_8"
iconImageURL = "https://yt3.ggpht.com/O7m_5HMY_O8yxR3Jhn9cEO1fLNL_GifMERExnAmfY7JrdTRsTjNijTcNYTPN97Llj3zGn8Susw=s88-c-k-c0x00ffffff-no-rj"

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
