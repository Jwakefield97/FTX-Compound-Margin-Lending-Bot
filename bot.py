import time
import hmac
import requests 
import configparser
import logging

API_KEY = ''
API_SECRET = ''
CURRENCY = 'USD'
LENDING_PERIOD = 60

#returns json response 
def make_ftx_get_request(endpoint, params={}):
    ts = int(time.time() * 1000)
    signature_payload = f'{ts}GET{endpoint}'.encode()
    signature = hmac.new(API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    response = requests.get(
        f'https://ftx.com{endpoint}',
        headers={
            'Accept': 'application/json',
            'FTX-KEY': API_KEY,
            'FTX-SIGN': signature,
            'FTX-TS': str(ts)
        },
        params=params
    )
    return response.json()
    
def make_lend_request(amount, rate):
    ts = int(time.time() * 1000)
    signature_payload = f'{ts}GET{endpoint}'.encode()
    signature = hmac.new(API_SECRET.encode(), signature_payload, 'sha256').hexdigest()

    response = requests.post(
        f'https://ftx.com/spot_margin/offers',
        headers={
            'Accept': 'application/json',
            'FTX-KEY': API_KEY,
            'FTX-SIGN': signature,
            'FTX-TS': str(ts)
        },
        data={
            'coin': CURRENCY,
            'size': amount, 
            'rate': rate
        }
    )
    return response.json()

def lending_loop():
    while True:
        balances_res = make_ftx_get_request('/api/wallet/balances')
        rates_res = make_ftx_get_request('/api/spot_margin/lending_rates')

        if balances_res['success'] == True and rates_res['success'] == True: 
            balance  = next(balance for balance in balances_res['result'] if balance['coin'] == CURRENCY)
            rate = next(rate for rate in rates_res['result'] if rate['coin'] == CURRENCY)

            if balance['free'] > 0: 
                logging.debug(f'Attempting to lend {balance["free"]} {CURRENCY} at rate: {rate["estimate"]}')
                loan_res = make_lend_request(balance['free'], rate['estimate'])
                if loan_res['success'] == True:
                    logging.debug(f'Successfully to lent {balance["free"]} {CURRENCY} at rate: {rate["estimate"]}')
                else:
                    logging.error(f'There was a problem lending {balance["free"]} {CURRENCY} at rate: {rate["estimate"]}')
        else:
            logging.error('Failed to get a response from ftx for balances or lending rates.')

        time.sleep(LENDING_PERIOD * 60)


if __name__ == '__main__':
    logging.basicConfig(filename='bot.log', level=logging.DEBUG)
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('config.txt')

    API_KEY = config['DEFAULT']['API_KEY']
    API_SECRET = config['DEFAULT']['API_SECRET']
    CURRENCY = config.get('DEFAULT', 'CURRENCY', fallback=CURRENCY)
    LENDING_PERIOD = config.get('DEFAULT', 'LENDING_PERIOD', fallback=LENDING_PERIOD)

    lending_loop()
