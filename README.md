# Welcome to Facebook Chat Bot!
The goal of this project is to create an emotional Facebook Messenger chat bot.
Depending on whether the user sends it a positive or negative message, it will gradually get happier or sadder,
which will determine its responses. All the responses are generic and simply visualise the mood of the bot.
The bot should also reply with its current mood for a special message "mood".


## Getting Started

It is required that you have installed Python3.7 on your system, if not, please use one of the following solutions
depending on your deployment structure:


On-premises:

1. Make sure you have Python 3.7 version, virtualenv for dependencies isolation and pip for packages management
2. Clone the repo
3. Enter the cloned repo directory
```
cd facebook-messenger-chat-bot
```
4. Create a virtual environment with the command
```
virtualenv --python=<path_of_your_python3.7> chat_bot
source chat_bot/bin/activate
```
5. Next install the requirements with pip
```
pip install -r requirements.txt
```
6. Set the env's necessary for running the app (Linux/Ubuntu):

```
export PAGE_ACCESS_TOKEN="EAADw5ZB3696EBA...your facebook API key here..."
export IBM_URL="https://gateway.watsonplatform.net/tone-analyzer/api"
export IBM_PASSWORD="<Watson IBM ToneAnalyzerV3 Password>"
export IBM_USERNAME="<Watson IBM ToneAnalyzerV3 Username>"
export IBM_VERSION="2017-09-21"
```
7. Let's get started!
```
python3.7 webserver.py
```
8. Access your app through http://localhost:8080


With docker:

1. Make sure that you have docker installed on your system
2. Run the following commands:
```
docker build -t app .

docker run -p 8080:8080 app --net localhost -e IBM_USERNAME=<Watson IBM ToneAnalyzerV3 Username> \
 -e IBM_PASSWORD=<Watson IBM ToneAnalyzerV3 Password> -e IBM_URL=https://gateway.watsonplatform.net/tone-analyzer/api \
 -e PAGE_ACCESS_TOKEN=<EAADw5ZB3696EBA...your facebook API key here...> -e IBM_VERSION=2017-09-21
```
3. Access your app through http://localhost:8080


Google App Engine

1. Follow on-premises instructions until the 6th step
2. For our custom Dockerfile image use this configuration inside app.yaml

```
runtime: custom
env: flex
env_variables:
  PAGE_ACCESS_TOKEN: '<EAADw5ZB3696EBA...your facebook API key here...>'
  IBM_URL: 'https://gateway.watsonplatform.net/tone-analyzer/api'
  IBM_PASSWORD: '<Watson IBM ToneAnalyzerV3 Password>'
  IBM_USERNAME: '<Watson IBM ToneAnalyzerV3 Username>'
  IBM_VERSION: '2017-09-21'
```

or

2. Use the normal configuration on app.yaml but remember to set the env variables from step number 6
```
runtime: python37
```


## Running the tests

Tests can be found on the /tests folders and apps/*/tests and run with Pytest framework.
From the main project folder, do:

```
pytest -v -p no:warnings
```

or

```
python3 -m pytest -v -p no:warnings
```

## Built With

* [Sanic](http://sanic.readthedocs.io)
* [aiohttp](https://aiohttp.readthedocs.io)
* [Docker](https://www.docker.com)

## Authors

* **Leonardo Silva Vilhena** - *Github user* - [Github](https://github.com/Leovilhena)
