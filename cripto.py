import requests


def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()

    if 'price' in data:
        return float(data['price'])
    else:
        raise ValueError(f"Erro ao buscar dados para {symbol}")
