import requests
from datetime import datetime
import asyncio

from pyrogram import Client, idle
import asyncio

# Binance API and Telegram Bot Details
BINANCE_BASE_URL = "https://api.binance.com"
BINANCE_KLINES_ENDPOINT = "/api/v3/klines"

api_id = 28610306
api_hash = "3f57cc57f8883bd604baf3b814ffe023"

TELEGRAM_TOKEN = "7978076940:AAGRmPFltKll2IHozoNQpdGIl_WuSvrbHyM"

TELEGRAM_CHAT_ID = -4503296969  # Replace with your Telegram chat ID

# Bot Parameters
SYMBOL = "BTCUSDT"
INTERVAL = "5m"  # 1-minute candles for live trading
SL_PERCENT = 0.035  # Stop-loss percentage (3.5%)
TP_PERCENT = 0.004  # Take-profit percentage (1.8%)
MOVE_SL_TRIGGER = 0.0025  # Move SL when price goes 1% above entry price
DELAY = 0.1  # Delay between price checks (in seconds)
DONE_DELAY=905.1

# Initialize Bot
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=TELEGRAM_TOKEN)

# Fetch Live Candle Data
async def get_candles(symbol, interval, limit=3):
    url = f"{BINANCE_BASE_URL}{BINANCE_KLINES_ENDPOINT}"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data  # List of candles
    else:
        print(f"Error fetching candles: {response.text}")
        return None

# Send a Telegram message
async def send_message(text):
    print(text)
    await app.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

# Strategy Implementation
async def run_strategy():
    position = None  # No open position initially
    x=True
    pos_type=True
    while True:

        # Fetch the latest candles
        candles = await get_candles(SYMBOL, INTERVAL, limit=3)
        if not candles:
            continue
        
        # Parse the last 3 candles
        close_prices = [float(c[4]) for c in candles]
        open_prices = [float(c[1]) for c in candles]
        #await send_message(f"🔔 Close Prices: {close_prices[0]:.2f}")

        # Check if last 3 candles' close > open
        if all(close > open for close, open in zip(close_prices, open_prices)):
            if position is None:
                # Trigger Buy Signal
                entry_price = close_prices[-1]
                stop_loss = entry_price * (1 - SL_PERCENT)
                take_profit = entry_price * (1 + TP_PERCENT)
                position = {"entry_price": entry_price, "stop_loss": stop_loss, "take_profit": take_profit}
                pos_type=True
                await send_message(f"🔔 YENİ LONG SİNYALİ\nGiriş: {entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")
                continue
        
        elif all(close < open for close, open in zip(close_prices, open_prices)):
            if position is None:
                # Trigger Buy Signal
                entry_price = close_prices[-1]
                stop_loss = entry_price * (1 + SL_PERCENT)
                take_profit = entry_price * (1 - TP_PERCENT)
                position = {"entry_price": entry_price, "stop_loss": stop_loss, "take_profit": take_profit}
                pos_type=False
                await send_message(f"🔔 YENİ SHORT SİNYALİ\nGiriş: {entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")
                continue

        # If a position is open, monitor the price
        if position :
            current_price = close_prices[-1]

            if pos_type:
                # Move SL to entry price if price goes 1% above entry
                if current_price >= position["entry_price"] * (1 + MOVE_SL_TRIGGER) and x:
                    position["stop_loss"] = position["entry_price"]
                    await send_message(f"(LONG SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position['stop_loss']:.2f}")
                    x=False

                # Trigger Sell Signal if price falls below SL
                if current_price <= position["stop_loss"]:
                    if position["stop_loss"] == position["entry_price"]:
                        await send_message(f"(LONG SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    else:
                        await send_message(f"(LONG SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price >= position["take_profit"]:
                    await send_message(f"(LONG SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    await asyncio.sleep(DONE_DELAY)
            else:
                # Move SL to entry price if price goes 1% above entry
                if current_price <= position["entry_price"] * (1 - MOVE_SL_TRIGGER) and x:
                    position["stop_loss"] = position["entry_price"]
                    await send_message(f"(SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position['stop_loss']:.2f}")
                    x=False

                # Trigger Sell Signal if price falls below SL
                if current_price >= position["stop_loss"]:
                    if position["stop_loss"] == position["entry_price"]:
                        await send_message(f"(SHORT SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    else:
                        await send_message(f"(SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price <= position["take_profit"]:
                    await send_message(f"(SHORT SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    await asyncio.sleep(DONE_DELAY)

        # Delay before checking the next price
        await asyncio.sleep(DELAY)

async def run_bot():
    await app.start()
    await run_strategy()
    await idle()
# Run the Bot
if __name__ == "__main__":
    asyncio.run(run_bot())
