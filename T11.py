import ccxt
import ta
import pandas as pd
import time
from telegram import Bot
from datetime import datetime
from ta.volume import VolumeWeightedAveragePrice

bot = Bot(token='6638844815:AAGnnsZtf-i_3EqfEGYWcO7riRG4zcaNUNM')

exchange = ccxt.bybit({ 'enableRateLimit': True })  # Instantiate the Bybit exchange

symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'MNT/USDT', 'SOL/USDT', 'APT/USDT', 'CTC/USDT', 'PLANET/USDT', 'LTC/USDT', 'DOGE/USDT', 'MATIC/USDT', 'TRX/USDT', 'LINK/USDT', 'DOT/USDT', 'AVAX/USDT', 'XLM/USDT', 'ADA/USDT', 'ICP/USDT']
timeframe = '1m'
limit = 100
window_size = 14

while True:
    for symbol in symbols:
        # Fetch historical data for the symbol on the 1 minute timeframe
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

        # Convert 'ohlcv' to a pandas DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Prepare the data for RSI calculation
        data = {
            'close': df['close']
        }

        # Convert 'close' data to a pandas Series object
        close_series = pd.Series(data['close'])

        # Ensure we have enough data points to calculate RSI
        if len(close_series) > window_size:
            # Calculate RSI using ta library
            rsi = ta.momentum.RSIIndicator(close=close_series, window=window_size)
            rsi_value = rsi.rsi().iloc[-1]

            # Calculate the VWAP using ta library
            vwap = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=window_size)
            vwap_value = vwap.volume_weighted_average_price().iloc[-1]

            if (rsi_value > 80) and (close_series.iloc[-1] < vwap_value):
                message = f"The RSI of {symbol} on the 1 min timeframe is: {rsi_value:.2f}\nIt is above 80 and below the VWAP\nTime: {datetime.now().strftime('%H:%M:%S')}"
                bot.send_message(chat_id='1160893757', text=message)
                # Add your code here to send a message or perform any action when RSI is above 80 and below VWAP

            elif (rsi_value < 30) and (close_series.iloc[-1] > vwap_value):
                message = f"The RSI of {symbol} on the 1 min timeframe is: {rsi_value:.2f}\nIt is below 30 and above the VWAP\nTime: {datetime.now().strftime('%H:%M:%S')}"
                bot.send_message(chat_id='1160893757', text=message)
                # Add your code here to send a message or perform any action when RSI is below 30 and above VWAP

        else:
            print(f"Insufficient data points to calculate RSI for {symbol}")

    time.sleep(5)
