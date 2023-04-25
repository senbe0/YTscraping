# setup

Replace with a CHROMEDRIVER appropriate for the environment.
You can get the latest version chromedriver and chrome using following commnads.
```
# install latest version google-chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# install latest version chromedrive
wget https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip

# confirm both version is same.
google-chrome --version
./chromedriver --version
```

# .env file
Create an .env file in the root of the project.
Set the driver_name.
```
driver_name = "chromedriver"
databaseAPI_url = "http://localhost:8015"
```

# Use requirements.txt to install packages.

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
