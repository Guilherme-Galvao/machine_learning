import json
import requests


def get_candlestick_data(exchange, crypto, interval, limit):
    # Fazer a requisição GET para a API de candlestick com os parâmetros especificados
    url = f'https://api.cryptowat.ch/markets/{exchange}/{crypto}/ohlc?periods={interval}&limit={limit}'
    response = requests.get(url)

    # Converter a resposta em JSON
    data = json.loads(response.text)

    # Retornar os dados de candlestick como uma lista de listas
    # Cada lista interna representa uma vela no formato [timestamp, valor abertura, valor máximo, valor mínimo, valor fechamento, volume]
    return data['result'][f'{interval}']


def calculate_volatility(candlesticks):
    # Extrair os preços de fechamento das velas
    prices = [float(candlestick[4]) for candlestick in candlesticks]

    # Calcular o desvio padrão dos preços e a média dos preços
    std_dev = sum((prices[i] - prices[i - 1]) ** 2 for i in range(1, len(prices))) / len(prices)
    mean = sum(prices) / len(prices)

    # Calcular a volatilidade como o desvio padrão dividido pela média dos preços
    return std_dev / mean


def print_price_range(volatility, price, unit):
    # Calcular o tamanho da faixa mínima e máxima de preço usando a volatilidade
    min_price = price - (price * volatility)
    max_price = price + (price * volatility)

    # Imprimir a faixa mínima e máxima de preço com duas casas decimais
    print(
        f'O preço do cryptoativo pode variar entre {round(min_price, 2)} {unit} e {round(max_price, 2)} {unit} no próximo período de tempo.')


def get_crypto_info(exchange, crypto, interval, limit):
    # Obter os dados de candlestick da API
    candlesticks = get_candlestick_data(exchange, crypto, interval, limit)

    # Calcular a volatilidade por minuto e por hora
    minute_volatility = calculate_volatility(candlesticks[-60:])
    hourly_volatility = calculate_volatility(candlesticks[:-60])

    # Exibir os resultados
    print(
        f'A volatilidade por hora do {crypto} nos últimos {limit} períodos de {interval} é de {round(hourly_volatility * 100, 2)}%.')
    print(
        f'A volatilidade por minuto dentro da última hora do {crypto} nos últimos 60 períodos de {interval} é de {round(minute_volatility * 100, 2)}%.')

    # Usar a função print_price_range para imprimir a faixa mínima e máxima de preço para o próximo período de tempo
    current_price = float(candlesticks[-1][4])
    unit = crypto[-4:]
    print_price_range(hourly_volatility, current_price, unit)

get_crypto_info('binance', 'btcusdt', '300', '100')
