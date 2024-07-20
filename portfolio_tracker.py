from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv

load_dotenv()

portfolio_tracker = Blueprint('portfolio_tracker', __name__)

def get_crypto_price(ticker):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data[ticker]['usd']

def get_stock_price(ticker):
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    url = f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['c']  # 'c' is the current price

@portfolio_tracker.route('/portfoliotracker')
def portfoliotracker():
    if current_user.is_authenticated:
        btc_price = get_crypto_price('bitcoin')
        aapl_price = get_stock_price('AAPL')
        return render_template('/portfoliotracker.html', btc_price=btc_price, aapl_price=aapl_price)
    else:
        return render_template('PTdemo_prompt.html')