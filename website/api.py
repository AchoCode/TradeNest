from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import requests
import json

api = Blueprint('api', __name__ )


# @api.route('/btc-price', methods = ['GET'])
# def Live_price():

#     headers = {
#         'X-CMC_PRO_API_KEY' : '6030d922-686b-4bf0-8aab-46dca6396aef',
#         'Accepts' : 'application/json'
#     }

#     params = {
#         'start' : '1',
#         'limit' : '3',
#         'convert' : 'USD'
#     }

#     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

#     json = requests.get(url, params=params, headers=headers).json()

#     coins = json['data']

#     for x in coins:
#         if x['symbol'] == 'BTC':
#             coin = x['quote']['USD']['price']
#     price = round(coin,2)

#     return jsonify(price)
