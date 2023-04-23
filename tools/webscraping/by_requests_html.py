"""
This source code is under development.
Please use "by_selenium" in the production environment.
"""

from requests_html import HTMLSession
from datetime import datetime
from typing import List
import pytz

class CountYoutubeViewers(object):
    def __init__(self, videoID):
        self.videoID = videoID
        self.videoURL = "https://www.youtube.com/watch?v=" + videoID
        self.session = HTMLSession()


    # If the youtube live feed is deleted, the DRIVER will be terminated.
    def _IsVideoExist(self):
        response = self.session.get(self.videoURL)
        if response.html.find('.ytp-error-content-wrap-reason', first=True):
            return True
        else:
            return False


    # If it'S NOT Live Streaming, the DRIVER will be terminated.
    def _IsItLiveStream(self):
        response = self.session.get(self.videoURL)
        response.html.render(wait=3)
        element = response.html.find('#info-container', first=True)
        print(element.text)
        if response.html.find('#info-container', first=True).text.endswith(' watching now'):
            return True
        else:
            return False


    def get_viewers(self):
        response = self.session.get(self.videoURL)
        viewers_str = response.html.find('#info-container', first=True).text

        if not self._IsItLiveStream():
            print("this")
            return False

        # If Live Streaming has finished, the DRIVER will be terminated.
        if viewers_str.split()[3] == "Streamed":
            print("eeee")
            return False
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


    def get_iconImageURL(self) -> str:
        response = self.session.get(self.videoURL)
        try:
            icon = response.html.find('a.yt-simple-endpoint.style-scope.ytd-video-owner-renderer yt-img-shadow img#img', first=True)
            icon_url = icon.attrs['src']
            return icon_url
        except:
            return False


def isItLiveStream(URL: str) -> List[bool]:
    isWatching = False
    isWaiting = False
    session = HTMLSession()
    response = session.get(URL)

    if response.html.find('#info-container', first=True).text.endswith(' watching now'):
        isWatching = True
    elif response.html.find('#info-container', first=True).text.endswith(' waiting'):
        isWaiting = True

    return [isWatching, isWaiting]

if __name__ == "__main__":
    YT = CountYoutubeViewers("1WLnQmlnYzU")
    num = YT.get_viewers()
    print(num)