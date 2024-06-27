# TEST BOT
###### This repository contains bot code for fetching K-line data for SOL/USDT from Bybit, calculating RSI based on closing prices, and sending notifications to a Discord channel.
----

## How to run
### Create a .env file with the following variables:
```
DISCORD_TOKEN={DISCORD_BOT_TOKEN}
DISCORD_CHANNEL_ID={DISCORD_CHANNEL_ID}
BYBIT_API_KEY={BYBIT_API_KEY}
BYBIT_SECRET_KEY={BYBIT_SECRET_KEY}
```
###### Note:
- Make sure your Discord bot has permissions to send messages.
-  You can obtain the Discord channel ID by enabling developer mode in your Discord application, then right-clicking on the channel and choosing “Copy Channel ID.”

### Requirements
- Python 3.12
- Poetry 1.8.3
- Docker
- Invite your bot to the chosen channel. You can generate the invitation link in the OAuth2 section of your Discord application.

## Run localy:
- navigate to the project repository
- `poetry shell`
- `poetry install`
- `python3 main.py`

## Run using Docker
- navigate to the project repository
- `docker build -t bot .`
- `docker run bot`

