from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
import os
from dotenv import load_dotenv
import logging

from models import db, User, Asset, UserAsset

azure_demos_bp = Blueprint('azure_demos', __name__)
load_dotenv()

@azure_demos_bp.route('/azure_demos')
@login_required
def azure_demos():
    if current_user.is_authenticated:
        return render_template('azure_demos.html')
    else:
        return redirect(url_for('/login'))

@azure_demos_bp.route('/translate', methods=['POST'])
@login_required
def translate():
    input = request.form['input']
    language = request.form['language']
    text = translation_engine(input, language)
    return render_template('azure_demos.html', text=text[0].translations[0].text)

# Azure functions
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient

def translation_engine(input, language):
    credential = AzureKeyCredential(os.getenv('TRANSLATOR_API_KEY'))
    endpoint = os.getenv('TRANSLATOR_ENDPOINT')

    translation_client = TextTranslationClient(endpoint=endpoint, credential=credential)
    text = [input]
    language = [language]
    translated_text = translation_client.translate(text, to_language=language)
    return translated_text

def ocr_engine():
    return 0

def speech_engine():
    return 0