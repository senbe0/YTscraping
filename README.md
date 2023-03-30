# setup

Replace with a CHROMEDRIVER appropriate for the environment.
You can get the latest version chromedriver and chrome using following commnads.
```
# chrome
sudo apt-get install google-chrome-stable


# chromedrive
wget https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
```
Create an .env file in the root of the project.
Set the driver_name.
```
# .env file

driver_name = "chromedriver.exe"
```
Use requirements.txt to install packages.

```
pip3 install -r requirements.txt
```


#  start with uvicron

```
uvicorn YTscraping.server:app --host 0.0.0.0 --port 8000 
```
or
```
python3 -m uvicorn YTscraping.server:app --host 0.0.0.0 --port 8000 
```
