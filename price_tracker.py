import time
import logging
import matplotlib.pyplot as plt
import pandas as pd
from stellar_sdk import Server, Network, Asset
from stellar_sdk.exceptions import NotFoundError
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    filename='kale_price_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Подключение к Stellar Testnet
server = Server(horizon_url="https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# Используем актив KALE
kale_asset = Asset("KALE", "GCHPTWXMT3HYF4RLZHWBNRF4MPXLTJ76ISHMSYIWCCDXWUYOQG5MR2AB")

# Список для хранения цен и времени для графика
prices = []
times = []

def plot_prices():
    # Преобразуем строки времени в datetime для корректного отображения
    time_objects = [datetime.strptime(t, "%H:%M:%S") for t in times]
    plt.plot(time_objects, prices)
    plt.xlabel("Time")
    plt.ylabel("KALE Price (USD)")
    plt.title("KALE Price Tracker")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def get_kale_price():
    try:
        # Запрос всех последних торгов
        trades = server.trades().call()
        kale_trades = [
            trade for trade in trades['_embedded']['records']
            if (trade['base_asset_type'] == 'credit_alphanum4' and 
                trade['base_asset_code'] == 'KALE' and 
                trade['base_asset_issuer'] == 'GCHPTWXMT3HYF4RLZHWBNRF4MPXLTJ76ISHMSYIWCCDXWUYOQG5MR2AB') or
               (trade['counter_asset_type'] == 'credit_alphanum4' and 
                trade['counter_asset_code'] == 'KALE' and 
                trade['counter_asset_issuer'] == 'GCHPTWXMT3HYF4RLZHWBNRF4MPXLTJ76ISHMSYIWCCDXWUYOQG5MR2AB')
        ]
        
        if kale_trades:
            trade = kale_trades[0]
            price = float(trade['price']['n']) / float(trade['price']['d'])
            logging.info(f"KALE Price: {price} USD")
            print(f"KALE Price: {price} USD")
            return price
        else:
            # Резервный вариант: использовать тестовые данные из CSV
            try:
                df = pd.read_csv('test_prices.csv')
                if df.empty or 'price' not in df.columns:
                    raise ValueError("CSV file is empty or missing 'price' column")
                price = float(df['price'].iloc[-1])
                logging.info(f"KALE Price (from CSV): {price} USD")
                print(f"KALE Price (from CSV): {price} USD")
                return price
            except (FileNotFoundError, ValueError, pd.errors.EmptyDataError) as e:
                # Фоллбэк на встроенные тестовые данные
                logging.warning(f"CSV error: {str(e)}. Using hardcoded test data.")
                print(f"CSV error: {str(e)}. Using hardcoded test data.")
                hardcoded_prices = [0.095, 0.096, 0.094, 0.093, 0.092]
                price = hardcoded_prices[len(prices) % len(hardcoded_prices)]
                logging.info(f"KALE Price (hardcoded): {price} USD")
                print(f"KALE Price (hardcoded): {price} USD")
                return price
    except NotFoundError:
        logging.error("Asset KALE not found on Testnet")
        print("Asset KALE not found on Testnet")
        return None
    except Exception as e:
        logging.error(f"Error fetching price: {str(e)}")
        print(f"Error fetching price: {str(e)}")
        return None

def main():
    print("Starting KALE Price Tracker...")
    while True:
        price = get_kale_price()
        if price:
            print(f"Current KALE Price: {price} USD")
            prices.append(price)
            times.append(time.strftime("%H:%M:%S"))
            if len(prices) >= 5:  # Показать график после 5 измерений
                plot_prices()
        else:
            print("Waiting for price data...")
        time.sleep(10)  # Уменьшено до 10 секунд для демо

if __name__ == "__main__":
    main()