from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv

from models import db, User, Asset, UserAsset

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
        user_assets = UserAsset.query.filter_by(user_id=current_user.id).all()
        return render_template('portfoliotracker.html', user_assets=user_assets)
    else:
        return render_template('PTdemo_prompt.html')

@portfolio_tracker.route('/add_asset', methods=['POST'])
@login_required
def add_asset():
    name = request.form['name']
    ticker = request.form['ticker']
    asset_type = request.form['type']
    quantity = float(request.form['quantity'])

    # Check if asset already exists
    asset = Asset.query.filter_by(ticker=ticker).first()
    if not asset:
        # Fetch asset price
        price = get_crypto_price(ticker) if asset_type.lower() == 'crypto' else get_stock_price(ticker)
        if price is None:
            flash('Failed to fetch asset price. Please check the ticker symbol and try again.', 'danger')
            return redirect(url_for('portfolio_tracker.portfoliotracker'))

        # Create new asset
        asset = Asset(name=name, ticker=ticker, type=asset_type, price=price)
        db.session.add(asset)
        db.session.commit()

    # Check if the user already owns this asset
    user_asset = UserAsset.query.filter_by(user_id=current_user.id, asset_id=asset.id).first()
    if user_asset:
        # Update the quantity
        user_asset.quantity += quantity
    else:
        # Add new user asset
        user_asset = UserAsset(user_id=current_user.id, asset_id=asset.id, quantity=quantity)
        db.session.add(user_asset)

    db.session.commit()
    flash('Asset added successfully!', 'success')
    return redirect(url_for('portfolio_tracker.portfoliotracker'))
