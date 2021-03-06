# FIND SPOT

find available spot on schedule a service

pre-requisites:
* python3
* chrome browser
* [selenium chromedriver](https://chromedriver.chromium.org/downloads) on the same version of your chrome browser

setup:

```
python3 -m venv venv
source  venv/bin/activate
pip install -r requirements.txt
curl -o chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
rm -rf chromedriver_linux64.zip
```

run:

```
python schedule.py
```

demo:

![video](./media/video_gif.gif)