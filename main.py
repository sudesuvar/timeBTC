import requests
import pandas as pd

def get_binance_data(symbol='BTCUSDT', interval='1h', limit=500):
    """
    Binance API'den tarihsel Bitcoin verilerini çeker.
    
    Args:
    - symbol: Hangi kripto parayı çekeceğin. BTCUSDT = Bitcoin/USDT
    - interval: Zaman dilimi ('1m' = 1 dakika, '1h' = 1 saat, '1d' = 1 gün)
    - limit: Kaç tane veri çekileceği (maksimum 1000)
    
    Returns:
    - Pandas DataFrame olarak döner
    """
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Çekilen verileri DataFrame'e dönüştürme
        df = pd.DataFrame(data, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
            'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Zamanı anlaşılır formata çevirme
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

        # Yalnızca gerekli sütunları alalım
        df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]
        
        return df
    else:
        print(f"API isteği başarısız oldu! Hata kodu: {response.status_code}")
        return None

# Örneğin, 1 saatlik verileri çekelim (en fazla 500 veri)
bitcoin_hourly_data = get_binance_data(interval='1h', limit=500)
if bitcoin_hourly_data is not None:
    print(bitcoin_hourly_data.head())
    
    
def get_large_binance_dataset(symbol='BTCUSDT', interval='1h', total_limit=5000):
    all_data = pd.DataFrame()
    limit_per_request = 1000
    end_time = None  # İlk istekte en güncel verileri çekeceğiz
    
    while len(all_data) < total_limit:
        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit_per_request}'
        
        if end_time:
            url += f'&endTime={end_time}'
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if len(data) == 0:
                print("Daha fazla veri yok.")
                break
            
            df = pd.DataFrame(data, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
                'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 
                'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

            df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]
            
            all_data = pd.concat([all_data, df])

            # Yeni istek için end_time güncelle (en eski veriye göre devam edelim)
            end_time = int(df['open_time'].min().timestamp() * 1000)
        else:
            print(f"API isteği başarısız oldu! Hata kodu: {response.status_code}")
            break
    
    return all_data

# 5000 veri toplayalım
bitcoin_large_dataset = get_large_binance_dataset(total_limit=5000)
print(bitcoin_large_dataset.shape)

bitcoin_large_dataset.to_csv('bitcoin_data_5000.csv', index=False)

