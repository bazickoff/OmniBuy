from genericpath import exists
import gspread
import sys
from datetime import datetime
import base64
from oauth2client.service_account import ServiceAccountCredentials

def SheetSetup():
    try:
        from Keys import sheetName
    except Exception as x:
        print(x)
    if exists("creds.json") == False:
        print("ERROR CREDS.JSON NOT FOUND, CREDS.JSON IS REQUIRED TO BE IN THIS FOLDER, EXITTING")
        sys.exit()

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json")

        client = gspread.authorize(creds)

        sheet = client.open(sheetName).sheet1
    except Exception as x:
        print(x)
        sys.exit()

    return sheet

def KeySetup():
    try:
        from Keys import kuKey, kuPass, kuSecret
    except:
        print("ERROR, API PARAMATER MISSING, FLUSHING KEYS.PY AND EXITING")
        file = open("Keys.py", "w")
        file.flush()
        file.close()
        sys.exit()
    kuKey = str(base64.b64decode(kuKey)).removeprefix("b'").removesuffix("'")
    kuPass = str(base64.b64decode(kuPass)).removeprefix("b'").removesuffix("'")
    kuSecret = str(base64.b64decode(kuSecret)).removeprefix("b'").removesuffix("'")

    return kuKey, kuPass, kuSecret


def Buy(pair, funds, client, currentPrice):
    try:
        orderId = client.create_market_order(pair, "buy", funds=str(funds))["orderId"]
        orderDetails = client.get_order_details(orderId)
        pair = pair.split("-")

        timeBought = datetime.now().strftime("%H:%M:%S")
        size = orderDetails["dealSize"]
        feesPaid = float(orderDetails["fee"])
        startFunds = float(funds)
        buyPrice = currentPrice
        dealFunds = round(float(orderDetails["dealFunds"]), 2)

        print(f"Bought {size} {pair[0]} with {dealFunds} {pair[1]} at ${round(buyPrice, 2)}")

        return timeBought, size, feesPaid, startFunds, buyPrice
        
    except Exception as x:
        print(x)
        print("DID NOT BUY")
        sys.exit()

def Sell(pair, size, client, currentPrice, feesPaid):
    try:
        while True:
            try:
                orderId = client.create_market_order(pair, "sell", size=str(size))["orderId"]
                orderDetails = client.get_order_details(orderId)
                break
            except Exception as x:
                if "Order size increment invalid" in str(x):
                    size = str(round(float(size) - 0.00000001, 8))
                    continue
                else:
                    print(x)
                    print("DID NOT SELL")
                    sys.exit()

        pair = pair.split("-")

        timeSold = datetime.now().strftime("%H:%M:%S")
        feesPaid += float(orderDetails["fee"])
        funds = round(float(orderDetails["dealFunds"]) - feesPaid, 2)
        finishFunds = funds
        sellPrice = currentPrice
        dealFunds = round(float(orderDetails["dealFunds"]), 2)
        date = datetime.now().strftime("%m-%d-%Y")

        print(f"Sold {size} {pair[0]} for {dealFunds} {pair[1]} at ${round(sellPrice, 2)}")

        return timeSold, funds, feesPaid, finishFunds, sellPrice, date

    except Exception as x:
        print(x)
        print("DID NOT SELL")
        sys.exit()
