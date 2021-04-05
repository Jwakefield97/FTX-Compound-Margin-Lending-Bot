# Lending Bot 

## Setup
You will need python 3 installed on your system and a config.txt to run the bot. At minium the file should contain your ftx api key (API_KEY) and secret (API_SECRET).
The config also allows for a CURRENCY option (defaults to USD) for setting what ticker to lend and a LENDING_PERIOD option that sets the amount of time the bot waits before attempting to lend from your account (measure in minutes; defaults to 60). 

## Run
From a command prompt or shell run the command `python bot.py`