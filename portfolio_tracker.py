from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv

from models import db, User, Asset, UserAsset

load_dotenv()

portfolio_tracker = Blueprint('portfolio_tracker', __name__)

apiIDs = {'the graph':'the-graph', 'fetch.ai':'fetch-ai'}

def get_crypto_prices(name):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={name}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    prices = data[name]['usd']
    print(name)
    return prices


def get_stock_prices(ticker):
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    url = f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    price = data['c']  # 'c' is the current price
    return price
    
def generate_acc_stats(user_assets):
    networth = 0
    for user_asset in user_assets:
        networth += user_asset.asset.price * user_asset.quantity
    return round(networth, 2)

# Routes

@portfolio_tracker.route('/portfoliotracker')
@login_required
def portfoliotracker():
    if current_user.is_authenticated:
        user_assets = UserAsset.query.filter_by(user_id=current_user.id).all()
        networth = generate_acc_stats(user_assets)
        return render_template('portfoliotracker.html', user_assets=user_assets,networth=networth)
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
        price = get_crypto_prices(apiIDs.get(name.lower(), name.lower())) if asset_type.lower() == 'crypto' else get_stock_prices(ticker)
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

@portfolio_tracker.route('/remove_asset', methods=['POST'])
@login_required
def remove_asset():
    asset_id = request.form['asset_id']  # Get the asset ID from the form
    user_asset = UserAsset.query.filter_by(user_id=current_user.id, asset_id=asset_id).first()

    if user_asset:
        db.session.delete(user_asset)
        db.session.commit()
        flash('Asset removed successfully!', 'success')
    else:
        flash('Asset not found or does not belong to you.', 'danger')

    return redirect(url_for('portfolio_tracker.portfoliotracker'))