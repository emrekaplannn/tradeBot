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

TELEGRAM_TOKEN = "7802370522:AAGQbwAcvLE1YeIK7uVw1xl35MrNVdDM6lo"

TELEGRAM_CHAT_ID = -4536205797  # Replace with your Telegram chat ID

# Bot Parameters
SYMBOL = "BTCUSDT"
SYMBOL2 = "ETHUSDT"
SYMBOL3 = "SOLUSDT"
SYMBOL4 = "XRPUSDT"
SYMBOL5 = "DOGEUSDT"
INTERVAL = "1m"  # 1-minute candles for live trading
SL_PERCENT = 0.0035  # Stop-loss percentage (3.5%)
TP_PERCENT = 0.0004  # Take-profit percentage (1.8%)
MOVE_SL_TRIGGER = 0.00025  # Move SL when price goes 1% above entry price
DELAY = 0.1  # Delay between price checks (in seconds)
DONE_DELAY=905.1
availability=0
availability2=0
availability3=0
availability4=0
availability5=0


# Initialize Bot
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=TELEGRAM_TOKEN)

# Fetch Live Candle Data
async def get_candles(symbol, interval, limit=4):
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
    position2 = None  # No open position initially
    position3 = None  # No open position initially
    position4 = None  # No open position initially
    position5 = None  # No open position initially
    
    x=True
    x2=True
    x3=True
    x4=True
    x5=True

    pos_type=True
    pos_type2=True
    pos_type3=True
    pos_type4=True
    pos_type5=True

    availability=0
    availability2=0
    availability3=0
    availability4=0
    availability5=0

    await send_message(f"🔔 Trade bot started by MRanewliz. Hadi para basalım!!")

    while True:

        # Fetch the latest candles
        candles = await get_candles(SYMBOL, INTERVAL, limit=4)
        candles2 = await get_candles(SYMBOL2, INTERVAL, limit=4)
        candles3 = await get_candles(SYMBOL3, INTERVAL, limit=4)
        candles4 = await get_candles(SYMBOL4, INTERVAL, limit=4)
        candles5 = await get_candles(SYMBOL5, INTERVAL, limit=4)

        if not candles or not candles2 or not candles3 or not candles4 or not candles5:
            continue
        
        # Parse btc the last 3 candles
        candles_for_analysis = candles[:-1]  # Exclude the latest candle
        close_prices_lysis = [float(c[4]) for c in candles_for_analysis]
        open_prices_lysis = [float(c[1]) for c in candles_for_analysis]
        #await send_message(f"🔔 Close Prices: {close_prices[0]:.2f}")
        close_prices = [float(c[4]) for c in candles]
        open_prices = [float(c[1]) for c in candles]

        # Parse eth the last 3 candles
        candles_for_analysis2 = candles2[:-1]  # Exclude the latest candle
        close_prices_lysis2 = [float(c[4]) for c in candles_for_analysis2]
        open_prices_lysis2 = [float(c[1]) for c in candles_for_analysis2]
        #await send_message(f"🔔 Close Prices: {close_prices[0]:.2f}")
        close_prices2 = [float(c[4]) for c in candles2]
        open_prices2 = [float(c[1]) for c in candles2]

        # Parse sol the last 3 candles
        candles_for_analysis3 = candles3[:-1]  # Exclude the latest candle
        close_prices_lysis3 = [float(c[4]) for c in candles_for_analysis3]
        open_prices_lysis3 = [float(c[1]) for c in candles_for_analysis3]
        #await send_message(f"🔔 Close Prices: {close_prices[0]:.2f}")
        close_prices3 = [float(c[4]) for c in candles3]
        open_prices3 = [float(c[1]) for c in candles3]

        # Parse xrp the last 3 candles
        candles_for_analysis4 = candles4[:-1]  # Exclude the latest candle
        close_prices_lysis4 = [float(c[4]) for c in candles_for_analysis4]
        open_prices_lysis4 = [float(c[1]) for c in candles_for_analysis4]
        #await send_message(f"🔔 Close Prices: {close_prices[0]:.2f}")
        close_prices4 = [float(c[4]) for c in candles4]
        open_prices4 = [float(c[1]) for c in candles4]

        # Parse doge the last 3 candles
        candles_for_analysis5 = candles5[:-1]  # Exclude the latest candle
        close_prices_lysis5 = [float(c[4]) for c in candles_for_analysis5]
        open_prices_lysis5 = [float(c[1]) for c in candles_for_analysis5]
        #await send_message(f"🔔 Close Prices: {close_prices[0]:.2f}")
        close_prices5 = [float(c[4]) for c in candles5]
        open_prices5 = [float(c[1]) for c in candles5]



        # Check btc if last 3 candles' close > open
        if availability==0 and all(close > open for close, open in zip(close_prices_lysis, open_prices_lysis)):
            if position is None:
                # Trigger Buy Signal
                entry_price = close_prices_lysis[-1]
                stop_loss = entry_price * (1 - SL_PERCENT)
                take_profit = entry_price * (1 + TP_PERCENT)
                position = {"entry_price": entry_price, "stop_loss": stop_loss, "take_profit": take_profit}
                pos_type=True
                await send_message(f"🔔BTC YENİ LONG SİNYALİ\nGiriş: {entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")
        
        elif availability==0 and all(close < open for close, open in zip(close_prices_lysis, open_prices_lysis)):
            if position is None:
                # Trigger Buy Signal
                entry_price = close_prices_lysis[-1]
                stop_loss = entry_price * (1 + SL_PERCENT)
                take_profit = entry_price * (1 - TP_PERCENT)
                position = {"entry_price": entry_price, "stop_loss": stop_loss, "take_profit": take_profit}
                pos_type=False
                await send_message(f"🔔BTC YENİ SHORT SİNYALİ\nGiriş: {entry_price:.2f}, SL={stop_loss:.2f}, TP={take_profit:.2f}")


        # Check eth if last 3 candles' close > open
        if availability2==0 and all(close > open for close, open in zip(close_prices_lysis2, open_prices_lysis2)):
            if position2 is None:
                # Trigger Buy Signal
                entry_price2 = close_prices_lysis2[-1]
                stop_loss2 = entry_price2 * (1 - SL_PERCENT)
                take_profit2 = entry_price2 * (1 + TP_PERCENT)
                position2 = {"entry_price": entry_price2, "stop_loss": stop_loss2, "take_profit": take_profit2}
                pos_type2=True
                await send_message(f"🔔ETH YENİ LONG SİNYALİ\nGiriş: {entry_price2:.2f}, SL={stop_loss2:.2f}, TP={take_profit2:.2f}")
        
        elif availability2==0 and all(close < open for close, open in zip(close_prices_lysis2, open_prices_lysis2)):
            if position2 is None:
                # Trigger Buy Signal
                entry_price2 = close_prices_lysis2[-1]
                stop_loss2 = entry_price2 * (1 + SL_PERCENT)
                take_profit2 = entry_price2 * (1 - TP_PERCENT)
                position2 = {"entry_price": entry_price2, "stop_loss": stop_loss2, "take_profit": take_profit2}
                pos_type2=False
                await send_message(f"🔔ETH YENİ SHORT SİNYALİ\nGiriş: {entry_price2:.2f}, SL={stop_loss2:.2f}, TP={take_profit2:.2f}")


        # Check sol if last 3 candles' close > open
        if availability3==0 and all(close > open for close, open in zip(close_prices_lysis3, open_prices_lysis3)):
            if position3 is None:
                # Trigger Buy Signal
                entry_price3 = close_prices_lysis3[-1]
                stop_loss3 = entry_price3 * (1 - SL_PERCENT)
                take_profit3 = entry_price3 * (1 + TP_PERCENT)
                position3 = {"entry_price": entry_price3, "stop_loss": stop_loss3, "take_profit": take_profit3}
                pos_type3=True
                await send_message(f"🔔SOL YENİ LONG SİNYALİ\nGiriş: {entry_price3:.2f}, SL={stop_loss3:.2f}, TP={take_profit3:.2f}")
        
        elif availability3==0 and all(close < open for close, open in zip(close_prices_lysis3, open_prices_lysis3)):
            if position3 is None:
                # Trigger Buy Signal
                entry_price3 = close_prices_lysis3[-1]
                stop_loss3 = entry_price3 * (1 + SL_PERCENT)
                take_profit3 = entry_price3 * (1 - TP_PERCENT)
                position3 = {"entry_price": entry_price3, "stop_loss": stop_loss3, "take_profit": take_profit3}
                pos_type3=False
                await send_message(f"🔔SOL YENİ SHORT SİNYALİ\nGiriş: {entry_price3:.2f}, SL={stop_loss3:.2f}, TP={take_profit3:.2f}")



        # Check xrp if last 3 candles' close > open
        if availability4==0 and all(close > open for close, open in zip(close_prices_lysis4, open_prices_lysis4)):
            if position4 is None:
                # Trigger Buy Signal
                entry_price4 = close_prices_lysis4[-1]
                stop_loss4 = entry_price4 * (1 - SL_PERCENT)
                take_profit4 = entry_price4 * (1 + TP_PERCENT)
                position4 = {"entry_price": entry_price4, "stop_loss": stop_loss4, "take_profit": take_profit4}
                pos_type4=True
                await send_message(f"🔔XRP YENİ LONG SİNYALİ\nGiriş: {entry_price4:.4f}, SL={stop_loss4:.4f}, TP={take_profit4:.4f}")
        
        elif availability4==0 and all(close < open for close, open in zip(close_prices_lysis4, open_prices_lysis4)):
            if position4 is None:
                # Trigger Buy Signal
                entry_price4 = close_prices_lysis4[-1]
                stop_loss4 = entry_price4 * (1 + SL_PERCENT)
                take_profit4 = entry_price4 * (1 - TP_PERCENT)
                position4 = {"entry_price": entry_price4, "stop_loss": stop_loss4, "take_profit": take_profit4}
                pos_type4=False
                await send_message(f"🔔XRP YENİ SHORT SİNYALİ\nGiriş: {entry_price4:.4f}, SL={stop_loss4:.4f}, TP={take_profit4:.4f}")



        # Check doge if last 3 candles' close > open
        if availability5==0 and all(close > open for close, open in zip(close_prices_lysis5, open_prices_lysis5)):
            if position5 is None:
                # Trigger Buy Signal
                entry_price5 = close_prices_lysis5[-1]
                stop_loss5 = entry_price5 * (1 - SL_PERCENT)
                take_profit5 = entry_price5 * (1 + TP_PERCENT)
                position5 = {"entry_price": entry_price5, "stop_loss": stop_loss5, "take_profit": take_profit5}
                pos_type5=True
                await send_message(f"🔔DOGE YENİ LONG SİNYALİ\nGiriş: {entry_price5:.5f}, SL={stop_loss5:.5f}, TP={take_profit5:.5f}")
        
        elif availability5==0 and all(close < open for close, open in zip(close_prices_lysis5, open_prices_lysis5)):
            if position5 is None:
                # Trigger Buy Signal
                entry_price5 = close_prices_lysis5[-1]
                stop_loss5 = entry_price5 * (1 + SL_PERCENT)
                take_profit5 = entry_price5 * (1 - TP_PERCENT)
                position5 = {"entry_price": entry_price5, "stop_loss": stop_loss5, "take_profit": take_profit5}
                pos_type5=False
                await send_message(f"🔔DOGE YENİ SHORT SİNYALİ\nGiriş: {entry_price5:.5f}, SL={stop_loss5:.5f}, TP={take_profit5:.5f}")


        

        if availability > 0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
            await send_message(f"**Avail1: {availability}, {current_time}")
            availability-=10

        if availability2 > 0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
            await send_message(f"**Avail12: {availability2}, {current_time}")
            availability2-=10

        if availability3 > 0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
            await send_message(f"**Avail13: {availability3}, {current_time}")
            availability3-=10

        if availability4 > 0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
            await send_message(f"**Avail14: {availability4}, {current_time}")
            availability4-=10

        if availability5 > 0:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format the timestamp
            await send_message(f"**Avail15: {availability5}, {current_time}")
            availability5-=10

        # If a btc position is open, monitor the price
        if position :
            current_price = close_prices[-1]

            if pos_type:
                # Move SL to entry price if price goes 1% above entry
                if current_price >= position["entry_price"] * (1 + MOVE_SL_TRIGGER) and x:
                    position["stop_loss"] = position["entry_price"]
                    await send_message(f"(BTC LONG SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position['stop_loss']:.2f}")
                    x=False

                # Trigger Sell Signal if price falls below SL
                if current_price <= position["stop_loss"]:
                    if position["stop_loss"] == position["entry_price"]:
                        await send_message(f"(BTC LONG SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    else:
                        await send_message(f"(BTC LONG SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    availability=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price >= position["take_profit"]:
                    await send_message(f"(BTC LONG SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    #await asyncio.sleep(DONE_DELAY)
                    availability=1800
            else:
                # Move SL to entry price if price goes 1% above entry
                if current_price <= position["entry_price"] * (1 - MOVE_SL_TRIGGER) and x:
                    position["stop_loss"] = position["entry_price"]
                    await send_message(f"(BTC SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position['stop_loss']:.2f}")
                    x=False

                # Trigger Sell Signal if price falls below SL
                if current_price >= position["stop_loss"]:
                    if position["stop_loss"] == position["entry_price"]:
                        await send_message(f"(BTC SHORT SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    else:
                        await send_message(f"(BTC SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    availability=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price <= position["take_profit"]:
                    await send_message(f"(BTC SHORT SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price:.2f}")
                    position = None
                    x=True
                    availability=1800
                    #await asyncio.sleep(DONE_DELAY)



        # If a eth position is open, monitor the price
        if position2 :
            current_price2 = close_prices2[-1]

            if pos_type2:
                # Move SL to entry price if price goes 1% above entry
                if current_price2 >= position2["entry_price"] * (1 + MOVE_SL_TRIGGER) and x2:
                    position2["stop_loss"] = position2["entry_price"]
                    await send_message(f"(ETH LONG SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position2['stop_loss']:.2f}")
                    x2=False

                # Trigger Sell Signal if price falls below SL
                if current_price2 <= position2["stop_loss"]:
                    if position2["stop_loss"] == position2["entry_price"]:
                        await send_message(f"(ETH LONG SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price2:.2f}")
                    else:
                        await send_message(f"(ETH LONG SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price2:.2f}")
                    position2 = None
                    x2=True
                    availability2=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price2 >= position2["take_profit"]:
                    await send_message(f"(ETH LONG SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price2:.2f}")
                    position2 = None
                    x2=True
                    availability2=1800
                    #await asyncio.sleep(DONE_DELAY)
            else:
                # Move SL to entry price if price goes 1% above entry
                if current_price2 <= position2["entry_price"] * (1 - MOVE_SL_TRIGGER) and x2:
                    position2["stop_loss"] = position2["entry_price"]
                    await send_message(f"(ETH SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position2['stop_loss']:.2f}")
                    x2=False

                # Trigger Sell Signal if price falls below SL
                if current_price2 >= position2["stop_loss"]:
                    if position2["stop_loss"] == position2["entry_price"]:
                        await send_message(f"(ETH SHORT SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price2:.2f}")
                    else:
                        await send_message(f"(ETH SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price2:.2f}")
                    position2 = None
                    x2=True
                    availability2=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price2 <= position2["take_profit"]:
                    await send_message(f"(ETH SHORT SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price2:.2f}")
                    position2 = None
                    x2=True
                    availability2=1800
                    #await asyncio.sleep(DONE_DELAY)



            
        # If a sol position is open, monitor the price
        if position3 :
            current_price3 = close_prices3[-1]

            if pos_type3:
                # Move SL to entry price if price goes 1% above entry
                if current_price3 >= position3["entry_price"] * (1 + MOVE_SL_TRIGGER) and x3:
                    position3["stop_loss"] = position3["entry_price"]
                    await send_message(f"(SOL LONG SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position3['stop_loss']:.2f}")
                    x3=False

                # Trigger Sell Signal if price falls below SL
                if current_price3 <= position3["stop_loss"]:
                    if position3["stop_loss"] == position3["entry_price"]:
                        await send_message(f"(SOL LONG SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price3:.2f}")
                    else:
                        await send_message(f"(SOL LONG SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price3:.2f}")
                    position3 = None
                    x3=True
                    availability3=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price3 >= position3["take_profit"]:
                    await send_message(f"(SOL LONG SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price3:.2f}")
                    position3 = None
                    x3=True
                    availability3=1800
                    #await asyncio.sleep(DONE_DELAY)
            else:
                # Move SL to entry price if price goes 1% above entry
                if current_price3 <= position3["entry_price"] * (1 - MOVE_SL_TRIGGER) and x3:
                    position3["stop_loss"] = position3["entry_price"]
                    await send_message(f"(SOL SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position3['stop_loss']:.2f}")
                    x3=False

                # Trigger Sell Signal if price falls below SL
                if current_price3 >= position3["stop_loss"]:
                    if position3["stop_loss"] == position3["entry_price"]:
                        await send_message(f"(SOL SHORT SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price3:.2f}")
                    else:
                        await send_message(f"(SOL SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price3:.2f}")
                    position3 = None
                    x3=True
                    availability3=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price3 <= position3["take_profit"]:
                    await send_message(f"(SOL SHORT SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price3:.2f}")
                    position3 = None
                    x3=True
                    availability3=1800
                    #await asyncio.sleep(DONE_DELAY)






        # If a xrp position is open, monitor the price
        if position4 :
            current_price4 = close_prices4[-1]

            if pos_type4:
                # Move SL to entry price if price goes 1% above entry
                if current_price4 >= position4["entry_price"] * (1 + MOVE_SL_TRIGGER) and x4:
                    position4["stop_loss"] = position4["entry_price"]
                    await send_message(f"(XRP LONG SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position4['stop_loss']:.4f}")
                    x4=False

                # Trigger Sell Signal if price falls below SL
                if current_price4 <= position4["stop_loss"]:
                    if position4["stop_loss"] == position4["entry_price"]:
                        await send_message(f"(XRP LONG SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price4:.4f}")
                    else:
                        await send_message(f"(XRP LONG SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price4:.4f}")
                    position4 = None
                    x4=True
                    availability4=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price4 >= position4["take_profit"]:
                    await send_message(f"(XRP LONG SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price4:.4f}")
                    position4 = None
                    x4=True
                    availability4=1800
                    #await asyncio.sleep(DONE_DELAY)
            else:
                # Move SL to entry price if price goes 1% above entry
                if current_price4 <= position4["entry_price"] * (1 - MOVE_SL_TRIGGER) and x4:
                    position4["stop_loss"] = position4["entry_price"]
                    await send_message(f"(XRP SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position4['stop_loss']:.4f}")
                    x4=False

                # Trigger Sell Signal if price falls below SL
                if current_price4 >= position4["stop_loss"]:
                    if position4["stop_loss"] == position4["entry_price"]:
                        await send_message(f"(XRP SHORT SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price4:.4f}")
                    else:
                        await send_message(f"(XRP SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price4:.4f}")
                    position4 = None
                    x4=True
                    availability4=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price4 <= position4["take_profit"]:
                    await send_message(f"(XRP SHORT SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price4:.4f}")
                    position4 = None
                    x4=True
                    availability4=1800
                    #await asyncio.sleep(DONE_DELAY)






        # If a doge position is open, monitor the price
        if position5 :
            current_price5 = close_prices5[-1]

            if pos_type5:
                # Move SL to entry price if price goes 1% above entry
                if current_price5 >= position5["entry_price"] * (1 + MOVE_SL_TRIGGER) and x5:
                    position5["stop_loss"] = position5["entry_price"]
                    await send_message(f"(DOGE LONG SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position5['stop_loss']:.5f}")
                    x5=False

                # Trigger Sell Signal if price falls below SL
                if current_price5 <= position5["stop_loss"]:
                    if position5["stop_loss"] == position5["entry_price"]:
                        await send_message(f"(DOGE LONG SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price5:.5f}")
                    else:
                        await send_message(f"(DOGE LONG SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price5:.5f}")
                    position5 = None
                    x5=True
                    availability5=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price5 >= position5["take_profit"]:
                    await send_message(f"(DOGE LONG SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price5:.5f}")
                    position5 = None
                    x5=True
                    availability5=1800
                    #await asyncio.sleep(DONE_DELAY)
            else:
                # Move SL to entry price if price goes 1% above entry
                if current_price5 <= position5["entry_price"] * (1 - MOVE_SL_TRIGGER) and x5:
                    position5["stop_loss"] = position5["entry_price"]
                    await send_message(f"(DOGE SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP GİRİŞE ÇEKİLDİ🟢\nGüncel SL = {position5['stop_loss']:.5f}")
                    x5=False

                # Trigger Sell Signal if price falls below SL
                if current_price5 >= position5["stop_loss"]:
                    if position5["stop_loss"] == position5["entry_price"]:
                        await send_message(f"(DOGE SHORT SİNYALİ GÜNCELLEME)\n🔔 GİRİŞ NOKTASINA DÖNDÜK❎\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price5:.5f}")
                    else:
                        await send_message(f"(DOGE SHORT SİNYALİ GÜNCELLEME)\n🔔 STOP ÇALIŞTI❌\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price5:.5f}")
                    position5 = None
                    x5=True
                    availability5=1800
                    #await asyncio.sleep(DONE_DELAY)

                # Trigger Buy Signal if price goes above TP
                elif current_price5 <= position5["take_profit"]:
                    await send_message(f"(DOGE SHORT SİNYALİ GÜNCELLEME)\n🔔 HEDEFE ULAŞILDI✅\nİŞLEMİ KAPAT! Çıkış seviyesi: {current_price5:.5f}")
                    position5 = None
                    x5=True
                    availability5=1800
                    #await asyncio.sleep(DONE_DELAY)



        # Delay before checking the next price
        await asyncio.sleep(DELAY)

async def run_bot():
    await app.start()
    await run_strategy()
    await idle()
# Run the Bot
if __name__ == "__main__":
    asyncio.run(run_bot())
