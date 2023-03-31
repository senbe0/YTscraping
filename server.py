from fastapi import FastAPI, Request, Response, status
import xml.etree.ElementTree as ET
import subprocess
import sys
import os

from .tools.database import videosDB
from .tools.webscraping import by_selenium


app = FastAPI()

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


@app.get("/getYTnotify")
async def accept_feed(request: Request, response: Response) -> Response:
    challenge = request.query_params.get("hub.challenge")
    if challenge:
        return Response(
            challenge, status_code=status.HTTP_200_OK, media_type="text/plain"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/getYTnotify", status_code=200)
async def notify(request: Request, response: Response) -> Response:
    request_body = await request.body()
    XMLdata = request_body.decode('utf-8')
    root = ET.fromstring(XMLdata)
    try:
        entry_element = root[4]
        videoID = entry_element[1].text
        channelID = entry_element[2].text
        videoTitle = entry_element[3].text
        videoURL = "https://www.youtube.com/watch?v=" + videoID
    except Exception as e:
        return Response(status_code=status.HTTP_200_OK, media_type="text/plain")

    # isTiLiveStream returns List[iswatching, iswaiting].
    isStreamList = by_selenium.isItLiveStream(videoURL)
    IconImageURL = by_selenium.get_iconImageURL(videoURL)
    if not IconImageURL:
        IconImageURL = "https://yt3.googleusercontent.com/ytc/AL5GRJVxGt3eeqz_AHd26Oncs9Of9ZHWk9OyjSV0-lybGw=s176-c-k-c0x00ffffff-no-rj"

    print("----------------------")
    print(entry_element)
    print(videoID)
    print(channelID)
    print(videoTitle)
    print(videoURL)
    print(isStreamList)
    print(IconImageURL)
    print("----------------------")

    if isStreamList[0] or isStreamList[1]:
        try:
            videosDB.insert_videoRecord(videoID, channelID, videoTitle, videoURL, IconImageURL)
            print("ライブ配信の情報格納完了。")

            # excute subprocess
            excute_subprocess(videoID)

            print("サブプロセス、excute完了。")
        except Exception as e:
            print(f"maybe same video id: {e}")
    print(isStreamList)
    return Response(status_code=status.HTTP_200_OK, media_type="text/plain")
