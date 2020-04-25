# VK Analytics

This script get all mentions by keyword in [vk](https://vk.com/) count its and visualize with [plotly](https://chart-studio.plotly.com/) [bar chart](https://plotly.com/python/bar-charts/#basic-bar-chart-with-plotlygraphobjects). Just give positional argument "keyword" and optional argument "--days_period" in your command line.

More info: 
```
python3 main.py -h
```

Comand line EXAMPLE:
```
In:
python3 main.py YOUR_KEYWORD -d DAYS_COUNT_TO_SEARCH
Out:
https://plotly.com/~PLOTLY_USERNAME/CHART_NUMBER/
```
By default script hosted created bar chart on plotly web-hosting and open it in your browser. If you haven't browser, you can save url to bar chart, printed to your console as output.

### How to install

You need get VK SERVICE KEY. To do this, follow these steps:
1. [Register](https://vk.com/editapp?act=create) your standalone-application
2. Go to your registered app and copy in application settings service key
If you are unable to do this, read the additional information in the [VK API Manuals](https://vk.com/dev/manuals).

After get service key, create .env file in root project folder and place service key token in VK_SERVICE_KEY variable. 

Also you need plotly username and API key. To do this, follow these steps:
1. [Create](https://plotly.com/api_signup) plotly account
2. Get API key and plotly username [here](https://chart-studio.plotly.com/settings/api#/)

Place plotly API key at PLOTLY_API_KEY variable and plotly username at PLOTLY_USERNAME variable

Example .env:
```
VK_SERVICE_KEY=YOUR_VK_SERVICE_KEY
PLOTLY_USERNAME=YOUR_PLOTLY_USERNAME
PLOTLY_API_KEY=YOUR_PLOTLY_API_KEY
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
