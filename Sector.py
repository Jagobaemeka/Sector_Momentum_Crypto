#Pick five crypto sectors
#Allocate an equal amount of 20% to each of the five sectors
#Strategy will pick best performing ones.
#Calculate your momentum scores For each of the sectors, calculate a momentum score for the five biggest coins by market value.
# The momentum score is calculated by averaging the coin’s price return over the past seven, 30, 60, and 90 days.
#Use dual momentum to determine your final portfolio Dual momentum refers to two types of momentum: relative and absolute. 
#Relative momentum measures how an asset has performed relative to other assets over a certain time period, while absolute momentum measures whether an asset has actually risen in value over a certain period of time.
#Hold till the end of the month and rebalance Hold this crypto portfolio till the end of the month, then, on the last day of the month,
#go back and repeat the three steps above. So this strategy essentially trades and rebalances monthly.


impimport ccxt
import pandas as pd
import numpy as np
import schedule
import time

# Initialize the Binance exchange object with API credentials
exchange = ccxt.binance({
    'apiKey': 'your_api_key',
    'secret': 'your_api_secret',
    'enableRateLimit': True
})

# Define the sectors and their corresponding cryptocurrencies
sectors = {
    'Health': ['BTC/USDT', 'ETH/USDT'],  # Example coins
    'Identity': ['XRP/USDT', 'ADA/USDT'],
    'Gambling': ['DOGE/USDT', 'WIN/USDT'],
    'Sports': ['CHZ/USDT', 'SOC/USDT'],
    'Memes': ['DOGE/USDT', 'SHIB/USDT']
}

# Function to fetch historical price data
def fetch_data(symbol, timeframe='1d', since='90 days ago UTC'):
    return exchange.fetch_ohlcv(symbol, timeframe, since=exchange.parse8601(since))

# Function to calculate momentum scores
def calculate_momentum(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # Calculate returns over different periods and average them
    periods = [7, 30, 60, 90]
    for period in periods:
        df[f'return_{period}'] = df['close'].pct_change(period).shift(-period)
    
    df['momentum_score'] = df[[f'return_{p}' for p in periods]].mean(axis=1)
    return df['momentum_score'].iloc[-1]

# Function to rebalance the portfolio
def rebalance_portfolio():
    scores = {}
    for sector, coins in sectors.items():
        sector_scores = {}
        for coin in coins:
            data = fetch_data(coin)
            momentum_score = calculate_momentum(data)
            sector_scores[coin] = momentum_score
        # Pick the coin with the highest momentum score in each sector
        best_coin = max(sector_scores, key=sector_scores.get)
        scores[best_coin] = sector_scores[best_coin]
    
    # Allocate funds to the top coins based on dual momentum
    total_investment = 10000  # Example total investment
    investment_per_coin = total_investment / len(scores)
    
    # Execute trades (this is a placeholder, implement according to your exchange's API)
    for coin in scores:
        print(f"Allocating ${investment_per_coin} to {coin}")

# Schedule to run on the last day of each month
schedule.every().day.at("23:59").do(rebalance_portfolio)

while True:
    schedule.run_pending()
    time.sleep(1)




