from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests

portfolio_tracker = Blueprint('portfolio_tracker', __name__)

def get_crypto_price(ticker):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ticker}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data[ticker]['usd']

@portfolio_tracker.route('/portfoliotracker')
def portfoliotracker():
    if current_user.is_authenticated:
        btc_price = get_crypto_price('bitcoin')
        return render_template('/portfoliotracker.html', btc_price=btc_price)
    else:
        return render_template('PTdemo_prompt.html')