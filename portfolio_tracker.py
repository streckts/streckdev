from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv
import logging

from models import db, User, Asset, UserAsset

load_dotenv()

portfolio_tracker = Blueprint('portfolio_tracker', __name__)

apiIDs = {'the graph':'the-graph', 'fetch.ai':'fetch-ai'}

def get_crypto_prices(tickers):
    # Join the tickers into a comma-separated string
    ids = ','.join(tickers)
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        # Create a dictionary of prices where the key is the ticker and the value is the price
        prices = {ticker: data.get(ticker, {}).get('usd', None) for ticker in tickers}
        return prices

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    except ValueError as val_err:
        logging.error(f"JSON decoding error: {val_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return {}


def get_stock_prices(ticker):
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    url = f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}'
        
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred for {ticker}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred for {ticker}: {req_err}")
    except ValueError:
        logging.error(f"Error decoding JSON response for {ticker}")
    except Exception as e:
        logging.error(f"An unexpected error occurred for {ticker}: {e}")

    price = data['c']  # 'c' is the current price
    return price


def refresh_quotes(user_assets):
    crypto_tickers = [ua.asset.ticker for ua in user_assets if ua.asset.type == 'crypto']
    stock_tickers = [ua.asset.ticker for ua in user_assets if ua.asset.type == 'stock']

    #Fetch prices in bulk
    crypto_prices = get_crypto_prices(crypto_tickers) if crypto_tickers else {}
    stock_prices = {ticker: get_stock_prices(ticker) for ticker in stock_tickers} if stock_tickers else {}

    #Update all UserAssets in memory
    for user_asset in user_assets:
        if user_asset.asset.type == 'crypto':
            new_price = crypto_prices.get(user_asset.asset.ticker)
        elif user_asset.asset.type == 'stock':
            new_price = stock_prices.get(user_asset.asset.ticker)
        else:
            continue  # Skip unknown asset types

        if new_price is not None:
            user_asset.asset.price = new_price

    #Commit changes
    db.session.commit()
    
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
        refresh_quotes(user_assets)
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
        price = get_crypto_prices(list(apiIDs.get(name.lower(), name.lower()))) if asset_type.lower() == 'crypto' else get_stock_prices(list(ticker))
        if price is None:
            flash('Failed to fetch asset price. Please check the ticker symbol and try again.', 'danger')
            return redirect(url_for('portfolio_tracker.portfoliotracker'))

        # Create new asset
        asset = Asset(name=name, ticker=ticker, type=asset_type, price=price.get(ticker))
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