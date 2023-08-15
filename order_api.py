from config import ZW4001_config
from os import getcwd, remove, path
from pprint import pprint as pp
import requests
import datetime
import json
import pytz


#today = time.strftime('%d_%m_%Y')
tz_IST = pytz.timezone('Asia/Kolkata')
today = datetime.datetime.now(tz_IST).strftime('%d_%m_%Y')

working_dir = str(getcwd()) + "/"
zw4001_file_token = working_dir + "files/ZW4001_token." + today + ".json"
zw4001_token_dict = json.load(open(zw4001_file_token))

zw4001string = "token " + ZW4001_config.API_Key + ":" + zw4001_token_dict["access_token"]


#### Get required margins
def get_user_margin(acc):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    #print(headers)
    try:
        response = requests.get('https://api.kite.trade/user/margins', headers=headers)
        result = response.json()
        available_cash = result["data"]["equity"]["available"]["cash"]
        return available_cash
    except Exception as e:
        return{"status": "Error", "error_message": e}
    
def get_order_margin(instrumentToken, transactionType, quantity, acc, type):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    'Content-Type': 'application/json',
    }
    #print(headers)
    data = [{
        "exchange": type,
        "tradingsymbol": instrumentToken,
        "transaction_type": transactionType,
        "variety": "regular",
        "product": "NRML",
        "order_type": "MARKET",
        "quantity": quantity,
        "price": 0,
        "trigger_price": 0,
    },]
    try:
        response = requests.post('https://api.kite.trade/margins/orders', headers=headers, json=data)
        result = response.json()
        total = result["data"][0]["total"]
        leverage = result["data"][0]["leverage"]
        margin = (total/(leverage + 1))
        return(margin)
    except Exception as e:
        return{"status": "Error", "error_message": e}


#### Order functions
def zd_fno_order(instrumentToken, transactionType, quantity, acc, type):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    if type == "NFO-OPT":
        type = "NFO"
        order_type = "LIMIT"
        price = zd_get_quote(instrumentToken,acc)
    else:
        order_type = "MARKET"
        price = 0

    user_margin = get_user_margin(acc)
    order_margin = get_order_margin(instrumentToken, transactionType, quantity, acc, type)

    if float(user_margin) > float(order_margin):
        headers = {
        'X-Kite-Version': '3',
        'Authorization': mystring,
        }
        #print(headers)
        data = {
        'tradingsymbol': instrumentToken,
        'exchange': type,
        'transaction_type': transactionType,
        'order_type': order_type,
        'quantity': quantity,
        'price': price,
        'product': 'NRML',
        'validity': 'DAY'
        }   
        newdata = {}
        newdata.update(data)
        newdata['acc'] = acc
        print(newdata)
        try:
            response = requests.post('https://api.kite.trade/orders/regular', headers=headers, data=data)
            return(response.json())
        except Exception as e:
            return{"status": "Error", "error_message": e}
    else:
        return(f"Error - Insufficient Funds : Order margin needed {order_margin} : Available Funds {user_margin}")

def zd_option_order(instrumentToken, transactionType, quantity, price, acc):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    #print(headers)
    data = {
    'tradingsymbol': instrumentToken,
    'exchange': 'NFO',
    'transaction_type': transactionType,
    'order_type': 'LMIT',
    'price': price,
    'quantity': quantity,
    'product': 'NRML',
    'validity': 'DAY'
    }   
    newdata = {}
    newdata.update(data)
    newdata['acc'] = acc
    print(newdata)
    try:
        response = requests.post('https://api.kite.trade/orders/regular', headers=headers, data=data)
        return(response.json())
    except Exception as e:
        return{"status": "Error", "error_message": e}
    

def zd_order_status(order_id, acc):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    url = "https://api.kite.trade/orders/" + str(order_id)
    
    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    
    try:
        response = requests.get(url, headers=headers)
        os_list = response.json()['data']
        os_dict =  os_list[-1]
        return(os_dict)
    except Exception as e:
        return{"status": "Error", "error_message": e}

def zd_fno_sl_order(instrumentToken,transactionType,quantity,sl_trg_price,acc):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    #print(headers)
    data = {
    'tradingsymbol': instrumentToken,
    'exchange': 'NFO',
    'transaction_type': transactionType,
    'order_type': 'SL-M',
    'quantity': quantity,
    'trigger_price':sl_trg_price,
    'product': 'NRML',
    'validity': 'DAY'
    }   
    newdata = {}
    newdata.update(data)
    newdata['acc'] = acc
    print(newdata)
    try:
        response = requests.post('https://api.kite.trade/orders/regular', headers=headers, data=data)
        return(response.json())
    except Exception as e:
        return{"status": e}

    
def zd_get_quote(instrumentToken,acc):
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    instrument = "NFO:" + instrumentToken
    headers = {
        'X-Kite-Version': '3',
        'Authorization': mystring,
    }

    params = (
        ('i', instrument),
    )

    response = requests.get('https://api.kite.trade/quote/ltp', headers=headers, params=params)
    result = response.json()
    ltp_dict = result['data']
    ltp = ltp_dict[instrument]['last_price']
    return ltp


def zd_order_cancel(order_id, acc):
    url = "https://api.kite.trade/orders/regular/" + str(order_id)
    
    if acc == "ZW4101":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    
    try:
        response = requests.delete(url, headers=headers)
        return(response.json())
    except Exception as e:
        return{"status": "Error", "error_message": e}

def zd_get_positions(acc):
    url = "https://api.kite.trade/portfolio/positions"
    
    if acc == "ZW4001":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    
    try:
        response = requests.get(url, headers=headers)
        return(response.json())
    except Exception as e:
        return{"status": "Error", "error_message": e}

def zd_get_orders(acc):
    url = "https://api.kite.trade/orders"
    
    if acc == "ZW4101":
        mystring = zw4001string
    else:
        return "No acc specified"

    headers = {
    'X-Kite-Version': '3',
    'Authorization': mystring,
    }
    
    try:
        response = requests.get(url, headers=headers)
        return(response.json())
    except Exception as e:
        return{"status": e}



result = get_user_margin("ZW4001")
# result = get_order_margin('AXISBANK23JUN850PE', "SELL", 1200, "ZW4001", "NFO")
# result = zd_fno_order('AXISBANK23JUN850PE', "SELL", 1200, "ZW5495", "NFO-OPT")
# result = zd_get_quote('NIFTY23AUG18050CE','ZW4001')
# result = zd_order_status('220630401236709','ZW4001')
# result = zd_fno_sl_order('BANKNIFTY2330240200CE','SELL',125,7204,'ZW4001')
# result = zd_get_positions("ZW4001")
# result = zd_get_orders("ZW4001")

pp(result)
