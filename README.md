# OmniBuy
 OmniBuy is a trading bot that is able to utilize multiple trading strategies to optimize profits. It is able to trade many readily available cryptocurrencies. OmniBuy utilizes both the TradingView API, for technical analysis, and KuCoin API, for making purchases. 
 
Prerequisites:

    - A Google Account
    - A KuCoin Account

Setup:

    - Go to https://console.cloud.google.com/
    - Create a project
    - Navigate to API overview
    - Navigate to the library in API overview
    - Search for "Google Drive"
    - Enable "Google Drive"
    - Navigate to "Credentials" inside of the "Google Drive API" settings
    - Click "Manage Service Accounts"
    - Click "Create Service Account"
    - Name the service account
    - Give the service account the role of "Editor"
    - Click "Done"
    - Click the three dots underneath the "Actions" column of the service account
    - Click "Manage Keys"
    - Click "Create New Key", and select "JSON"
    - Save the file that is being downloaded to the OmniBuy Folder
    - Rename the file to "creds.json"
    - Navigate to the library in API overview
    - Search for "Google Sheets API"
    - Enable the "Google Sheets API"
    - Open the "creds.json" file and copy "cilent_email" to your clipboard
    - Go to your Google Drive and create a new Google Sheet
    - Create the headers, "Date", "Time Bought", "Time Sold", "Fees Paid", "Profit", "Profit(%)", "Buy Price", "Sell Price", "Trading Pair"
    - Share the Google Sheet with the email you copied in the previous step
    
    - On your KuCoin account navigate to "API Management"
    - Create an API with the "Trade" option enabled
    - Save the API key, secret, and passphrase 
    
    - Navigate to the OmniBuy folder in a terminal
    - In the terminal enter the command "pip install -r requirements.txt"
    - Then enter "python Main.py" to start OmniBuy
    - Enter your KuCoin API, key, secret, and passphrase when prompted
    - Enter the name of the Google Sheet created in the previous steps when prompted
    -

