from typing import Final
import os
from decimal import Decimal
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands, tasks

from bybit_client import BybitClient
from rsi_calculator import calculate_rsi, get_closing_prices
from contextvars import ContextVar

previously_upnormal: ContextVar[bool] = ContextVar('extremal', default=False)

load_dotenv()
CHANNEL_ID: Final[str] = os.getenv('DISCORD_CHANNEL_ID')
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
API_KEY: Final[str] = os.getenv('BYBIT_API_KEY')
API_SECRET: Final[str] = os.getenv('BYBIT_SECRET_KEY')

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# BYBIT SETUP
bybit_client: BybitClient = BybitClient(API_KEY, API_SECRET)

# MESSAGE FUNCTIONALITY
async def send_notification(rsi: Decimal) -> None:
    try:
        ####### TO REMOVE BEFORE COMPLETED, MAYBE ADD SOME LOGS TO BE SURE
        response: str = f'Nothing to worry about, RSI: {rsi}'
        print("?????????????")
        print(rsi)
        if rsi > 70 or rsi < 30 and previously_upnormal.get() is False:
            previously_upnormal.set(True)
            response: str = f'Current RSI: {rsi}'
            channel = bot.get_channel(int(CHANNEL_ID))
            await channel.send(response)
        else:
            previously_upnormal.set(False)
            # channel = bot.get_channel(int(CHANNEL_ID))
            # await channel.send(response)
    # TO HANDLE
    except Exception as e:
        print(e)

@tasks.loop(seconds=10)
async def fetch_job():
    data_from_bybit: dict = bybit_client.get_kline_data("SOLUSDT", "60", 336)
    closing_prices: list = get_closing_prices(data_from_bybit)
    rsi = calculate_rsi(closing_prices)
    await send_notification(rsi)


@bot.event
async def on_ready():
    fetch_job.start()


def main() -> None:
    bot.run(TOKEN)


if __name__ == "__main__":
    main()