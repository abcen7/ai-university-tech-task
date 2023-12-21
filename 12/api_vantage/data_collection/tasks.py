from celery import shared_task
import requests
from .models import StockData
from django.utils.dateparse import parse_datetime
from django.conf import settings

@shared_task
def fetch_data_from_api():
    api_key = settings.VANTAGE_API_KEY
    symbol = 'IBM'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'

    response = requests.get(url)
    data = response.json()

    time_series = data.get('Time Series (5min)', {})

    for time_stamp, values in time_series.items():
        stock_data = StockData(
            symbol=symbol,
            date_time=parse_datetime(time_stamp),
            open=values['1. open'],
            high=values['2. high'],
            low=values['3. low'],
            close=values['4. close'],
            volume=values['5. volume'],
        )
        stock_data.save()
