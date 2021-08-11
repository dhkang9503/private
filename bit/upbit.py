import os
import jwt
import uuid
import json
import hashlib
from urllib.parse import urlencode

import requests

def info():
    access_key = os.environ['UPBIT_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_API_SECRET_KEY']
    url = 'https://' + os.environ['UPBIT_API_SERVER_URL']

    return access_key, secret_key, url

def get_my_account():
    # print("CALL get_my_account()")
    access_key, secret_key, server_url = info()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)

    # print(res.json())

    d = dict()

    for coin in res.json():
        name = coin['currency']
        d[name] = dict()
        d[name]['balance'] = coin['balance']
        d[name]['locked'] = coin['locked']
        d[name]['avg_buy_price'] = coin['avg_buy_price']

    # print(d)
    return d

def get_orders(coin_id):
    # print("CALL get_orders()")
    access_key, secret_key, server_url = info()

    query = {
        'market': coin_id,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)

    # print(res.json())

def get_KRW_coins():
    # print("CALL get_KRW_coins()")
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails":"false"}

    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    all_coins = json.loads(response.text)

    KRW_coins = [[coin['market'], coin['korean_name']] for coin in all_coins if coin['market'].startswith('KRW-')]

    # for coin in KRW_coins:
    #     print(coin)

    return KRW_coins

def get_coin_candle(coin, count=3):
    # print("CALL get_coin_candle({})".format(coin))
    url = "https://api.upbit.com/v1/candles/days"

    querystring = {
        "market": coin, 
        "count": str(count)
    }

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    return json.loads(response.text)

def get_order_status(order_uuid):
    access_key, secret_key, server_url = info()

    query = {
        'uuid': order_uuid,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/order", params=query, headers=headers)

    return len(res.json()['trades']) > 0

def buy_coin(coin_id, price, count):
    access_key, secret_key, server_url = info()

    query = {
        'market': coin_id,
        'side': 'bid',
        'volume': count,
        'price': price,
        'ord_type': 'limit',
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

    res_uuid = res.json()['uuid']
    print("buy_coin(coin_id: {}, price: {}, count: {}): {}".format(coin_id, price, count, res_uuid))
    return res_uuid

def sell_coin(coin_id, price, count):
    access_key, secret_key, server_url = info()

    query = {
        'market': coin_id,
        'side': 'ask',
        'volume': count,
        'price': price,
        'ord_type': 'limit',
    }

    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)

def cancel_order(order_uuid):
    access_key, secret_key, server_url = info()

    query = {
        'uuid': order_uuid,
    }

    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.delete(server_url + "/v1/order", params=query, headers=headers)