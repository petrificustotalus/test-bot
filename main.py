import os
from contextvars import ContextVar
from decimal import Decimal
from typing import Final

import requests
from discord import Intents
from discord.ext import commands, tasks
from dotenv import load_dotenv

from bot.bybit_client import BybitClient
from bot.rsi_calculator import calculate_rsi, get_closing_prices

previously_upnormal: ContextVar[bool] = ContextVar("extremal", default=False)

load_dotenv()
CHANNEL_ID: Final[str] = os.getenv("DISCORD_CHANNEL_ID")
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
API_KEY: Final[str] = os.getenv("BYBIT_API_KEY")
API_SECRET: Final[str] = os.getenv("BYBIT_SECRET_KEY")

# BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# BYBIT SETUP
bybit_client: BybitClient = BybitClient(API_KEY, API_SECRET)


# MESSAGE FUNCTIONALITY
async def send_error_notification(message: str) -> None:
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send(message)


async def send_notification(rsi: Decimal) -> None:
    if (rsi > 70 or rsi < 30) and previously_upnormal.get() is False:
        previously_upnormal.set(True)
        response: str = f"Current RSI: {rsi}"
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send(response)
    else:
        previously_upnormal.set(False)


@tasks.loop(seconds=1)
async def fetch_job():
    try:
        data_from_bybit: dict = bybit_client.get_kline_data("SOLUSDT", "60", 336)
    except requests.ConnectionError:
        await send_error_notification(massage="WARNING! Unable to fetch SOL/USDT data!")
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
