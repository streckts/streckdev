from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv
import logging

from models import db, User, Asset, UserAsset

azure_demos_bp = Blueprint('azure_demos', __name__)

@azure_demos_bp.route('/azure_demos')
@login_required
def azure_demos():
    if current_user.is_authenticated:
        return render_template('azure_demos.html')
    else:
        return redirect(url_for('/login'))