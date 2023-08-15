import time
import pytz
import json
import pyotp
import datetime
from os import getcwd
from selenium import webdriver
from config import ZW4001_config
from kiteconnect import KiteConnect
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
tz_IST = pytz.timezone('Asia/Kolkata')
today = datetime.datetime.now(tz_IST).strftime('%d_%m_%Y')
working_dir = str(getcwd()) + "/"
ZW4001_token_file = working_dir + "files/ZW4001_token." + today + ".json"

def login_in_zerodha(api_key, api_secret, user_id, user_pwd, totp_key):
    
    token_file = ZW4001_token_file

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(f'https://kite.trade/connect/login?api_key={api_key}&v=3')
    login_id = WebDriverWait(driver, 10).until(lambda x: x.find_element(by=By.XPATH, value=('//*[@id="userid"]')))
    login_id.send_keys(user_id)

    pwd = WebDriverWait(driver, 10).until(lambda x: x.find_element(by=By.XPATH, value=('//*[@id="password"]')))
    pwd.send_keys(user_pwd)

    submit = WebDriverWait(driver, 10).until(lambda x: x.find_element(by=By.XPATH, value=('//*[@id="container"]/div/div/div[2]/form/div[4]/button')))
    submit.click()

    time.sleep(1)

    totp = WebDriverWait(driver, 10).until(lambda x: x.find_element(by=By.XPATH, value=("//input[@placeholder='••••••']")))
    authkey = pyotp.TOTP(totp_key)
    totp.send_keys(authkey.now())

    time.sleep(5)

    url = driver.current_url
    #print("========================>>>")
    #print(url.split('request_token='))
    initial_token = url.split('request_token=')[1]
    #print(initial_token)
    request_token = initial_token.split('&')[0]
    
    driver.close()
    
    token_dict = {}
    kite = KiteConnect(api_key = api_key)
    #print(request_token)
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data['access_token'])
    token_dict["access_token"] = data["access_token"]
    json.dump(token_dict, open(token_file,"w"))
    print(token_dict)
    
    return kite

    # kite = get_kite_client()
    # data = kite.generate_session(request_token, api_secret=kite_api_secret)
    # session["access_token"] = data["access_token"]
    

if __name__ == '__main__':
    kiteobj = login_in_zerodha(ZW4001_config.API_Key, ZW4001_config.API_Secret, ZW4001_config.ZERODHA_USER_ID, ZW4001_config.ZERODHA_USER_PWD, ZW4001_config.ZERODHA_TOTP_KEY)
    #print(kiteobj.profile())
