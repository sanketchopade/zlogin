# zlogin
This is a basic code to automate Zerodha login and place orders.

Pre-requisite:
- You should have chrome browser installed on your system.

Once you download or close this repository, follow the below steps to setup configuration and modules needed to run this code.
https://github.com/sanketchopade/zlogin.git

Step 1:
Edit zlogin/config/ZW4001_config.py file

Update values in the below varibles.

API_Key = "xxxxxxxxxxxxxxxx"
API_Secret = "0xxxxxxxxxxxxxxxxxxxx"
ZERODHA_USER_ID = "ZWXXXX"
ZERODHA_USER_PWD = "XxxxxxXXxxxx"
ZERODHA_TOTP_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"

ZERODHA_TOTP_KEY - This is the key you get once you set up 2FA for the first time.
If you have already setup 2FA, then disable it and enable again. When you enable 2FA again it will provide you with TOPT_KEY.

Step 2:
You should have python installed. If not then please visit python.org and install latest python version as per your OS.
- create python virtual environment
- cd zlogin
  $ python -m venv myvenv
  > .\myvenv\Scripts\Activate.ps1 if you are on windows or $ /myenv/bin/activate for unix/macos
  $ python.exe -m pip install --upgrade pip
  $ pip install -r requirements.txt

This step will ensure we have all the needed modules installed in the newly created virtual environment

You should now be able to run the code to login to your Zerodha account.
$ python login.py
If login is successful, you should see your access token generated. Also your token will be saved in the file
$ zlogin/files/ZW4001_token.15_08_2023.json

Next, you can use order_api to buy, sell, see margin money, get current ltp of stocks, options and more.
$ python order_api.py
