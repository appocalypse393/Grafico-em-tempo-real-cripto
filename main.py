import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import time

# Função para buscar o preço da criptomoeda usando a API da Binance
def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()

    # Verificando se a API retornou dados válidos
    #print(f"Dados retornados pela API para {symbol}: {data}")

    if 'price' in data:
        return float(data['price'])  # Convertendo para número
    else:
        raise ValueError(f"Erro ao buscar dados para {symbol}")

# Inicializando o app Dash
app = dash.Dash(__name__)

# Armazenar os preços e timestamps globalmente
prices = []
timestamps = []

app.layout = html.Div([
    html.H1("Monitor de Preço de Criptomoedas em Tempo Real (Binance API)"),
    dcc.Dropdown(
        id='crypto-dropdown',
        options=[
            {'label': 'Bitcoin (BTC/USDT)', 'value': 'BTCUSDT'},
            {'label': 'Ethereum (ETH/USDT)', 'value': 'ETHUSDT'},
            {'label': 'Litecoin (LTC/USDT)', 'value': 'LTCUSDT'},
        ],
        value='BTCUSDT'  # Valor padrão (Bitcoin/USDT)
    ),
    dcc.Graph(id='price-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10*100,  # Atualiza a cada 10 segundos
        n_intervals=0
    ),
    html.Div(id='debug-output')  # Div para depuração
])

@app.callback(
    Output('price-graph', 'figure'),
    Output('debug-output', 'children'),
    [Input('interval-component', 'n_intervals'),
     Input('crypto-dropdown', 'value')]
)
def update_graph(n, symbol):
    global prices, timestamps

    # Capturando o preço atual
    try:
        price = get_binance_price(symbol)
        timestamp = time.strftime('%H:%M:%S')

        # Adicionando o novo preço e timestamp
        prices.append(price)
        timestamps.append(timestamp)

        # Limitando o número de pontos a 20 para manter o gráfico limpo
        if len(prices) > 20:
            prices = prices[-20:]
            timestamps = timestamps[-20:]

        # Exibindo dados coletados no console
        print(f"Preço atual para {symbol}: {price} às {timestamp}")

        # Cria o gráfico com os dados coletados
        figure = {
            'data': [go.Scatter(
                x=timestamps,
                y=prices,
                mode='lines+markers',
                marker={'size': 8, 'color': 'blue'},
                line={'width': 2, 'color': 'green'}
            )],
            'layout': go.Layout(
                title=f'Preço em Tempo Real: {symbol}',
                xaxis={'title': 'Tempo', 'showgrid': False},
                yaxis={'title': 'Preço em USD', 'showgrid': True},
                plot_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
                paper_bgcolor='rgba(0,0,0,0)',
            )
        }
        return figure, f"Preço atual: {price} às {timestamp}"
    except ValueError as e:
        return {
            'data': [],
            'layout': go.Layout(
                title=str(e),
                xaxis={'title': 'Tempo'},
                yaxis={'title': 'Preço em USD'},
            )
        }, f"Erro: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)
