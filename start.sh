#! /bin/bash

sudo apt-get update && sudo apt-get upgrade
docker build -t my-python-app .
docker run -v /db:/app/ignore -d -e TZ=Europe/Moscow --name telegram_bot -e BOT_TOKEN='YOUR_API_TOKEN' my-python-app