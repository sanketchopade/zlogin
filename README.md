# zlogin
This is a basic code to automate Zerodha login and place orders.

Step 1:
Edit zlogin/config/ZW4001_config.py file

Update values in the below varibles.

API_Key = "xxxxxxxxxxxxxxxx"
API_Secret = "0xxxxxxxxxxxxxxxxxxxx"
ZERODHA_USER_ID = "ZW4001"
ZERODHA_USER_PWD = "XxxxxxXXxxxx"
ZERODHA_TOTP_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxx"

ZERODHA_TOTP_KEY - This is the key you get once you set up 2FA for the first time.
If you have already setup 2FA, then disable it and enable again. When you enable 2FA again it will provide you with TOPT_KEY.

