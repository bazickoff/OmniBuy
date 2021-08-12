import os
from EMAC import EMAC
from RSI import RSI
import platform
from MACD import MACD
from Graph import GraphTriple, GraphDouble, GraphRSI
from kucoin.client import User
import base64
import sys
import pandas as pd

mode = ""
clientInitialized = True
client = User
emacDict = {}
rsiDict = {}
macdDict = {}

def Art():
    if platform.system() == "linux":
        os.system("clear")
    else:
        os.system("cls")

    print("░█████╗░███╗░░░███╗███╗░░██╗██╗██████╗░██╗░░░██╗██╗░░░██╗")
    print("██╔══██╗████╗░████║████╗░██║██║██╔══██╗██║░░░██║╚██╗░██╔╝")
    print("██║░░██║██╔████╔██║██╔██╗██║██║██████╦╝██║░░░██║░╚████╔╝░")
    print("██║░░██║██║╚██╔╝██║██║╚████║██║██╔══██╗██║░░░██║░░╚██╔╝░░")
    print("╚█████╔╝██║░╚═╝░██║██║░╚███║██║██████╦╝╚██████╔╝░░░██║░░░")
    print("░╚════╝░╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═╝╚═════╝░░╚═════╝░░░░╚═╝░░░\n")

def PrintEmacParams():
    taker = 0.002
    forFees = int(emacDict["amount"]) * int(emacDict["trades"]) * taker + int(emacDict["trades"]) / 100
    forFees += forFees * 0.05

    print("  UseRSI: " + emacDict["usersi"])
    print("  ShortLen: " + emacDict["shortlen"])
    print("  LongLen: " + emacDict["longlen"])
    print("  Pair: " + emacDict["pair"])
    print("  Interval: " + emacDict["interval"])
    print("  Amount: " + emacDict["amount"])
    print("  Trades: " + emacDict["trades"])
    print("\nHave atleast " + str(round(forFees, 2)) + " dollars in " + emacDict["pair"].split("/")[1] + " that is not being traded to be spent on fees.")

def PrintRsiParams():
    taker = 0.002
    forFees = int(rsiDict["amount"]) * int(rsiDict["trades"]) * taker + int(rsiDict["trades"]) / 100 * 2
    forFees += forFees * 0.05

    print("  BuyRsi: " + rsiDict["buyrsi"])
    print("  SellRsi: " + rsiDict["sellrsi"])
    print("  Pair: " + rsiDict["pair"])
    print("  Interval: " + rsiDict["interval"])
    print("  Amount: " + rsiDict["amount"])
    print("  Trades: " + rsiDict["trades"])
    print("\nHave atleast " + str(round(forFees, 2)) + " dollars in " + rsiDict["pair"].split("/")[1] + " that is not being traded to be spent on fees.")

def PrintMacdParams():
    taker = 0.002
    forFees = int(macdDict["amount"]) * int(macdDict["trades"]) * taker + int(macdDict["trades"]) / 100
    forFees += forFees * 0.05

    print("  UseRSI: " + macdDict["usersi"])
    print("  Pair: " + macdDict["pair"])
    print("  Interval: " + macdDict["interval"])
    print("  Amount: " + macdDict["amount"])
    print("  Trades: " + macdDict["trades"])
    print("\nHave atleast " + str(round(forFees, 2)) + " dollars in " + macdDict["pair"].split("/")[1] + " that is not being traded to be spent on fees.")


def Check(toCheck):
    global mode
    global clientInitialized
    global client
    formated = toCheck.strip().lower()
    
    if clientInitialized == False:
        try:
            from Keys import kuKey, kuPass, kuSecret
            kuKey = str(base64.b64decode(kuKey)).removeprefix("b'").removesuffix("'")
            kuPass = str(base64.b64decode(kuPass)).removeprefix("b'").removesuffix("'")
            kuSecret = str(base64.b64decode(kuSecret)).removeprefix("b'").removesuffix("'")

            client = User(kuKey, kuSecret, kuPass)
            clientInitialized = True
            client.get_base_fee()
        except:
            print("ERROR KUCOIN API PARAMETERS INCORRECT, FLUSHING KEYS.PY")
            file = open("Keys.py", "w")
            file.flush()
            file.close()
            sys.exit()

    if formated == "help":
        print("\nCommands:")
        print("\n  Clear - Clears the terminal.")
        print("\n  Show Methods - Displays all the trading methods available for use.")
        print("\n  Use \"Method\" - Directs you to the menu of the method inputted.")
        print("    i.e. Use MACD")
        print("\n  Show Options - Displays the options of the selected method.")
        print("\n  Set \"Paramater\" \"Value\" - Sets the parameter inputted to the value inputted.")
        print("    i.e. Set Pair BTC/USDT")
        print("\n  Analyze \"File.csv\" - Analyzes the output of a previous trading session and returns the graphed results.")
        print("    i.e. Analyze 11-24-52.csv")
        print("\n  Empty Keys - Deletes the content of Keys.py, resulting in you re-inputting all parameters required by OmniBuy during the next startup.")
        print("\n  Exit - Exits the bot.")

    elif formated == "clear":
        if platform.system() == "linux":
            os.system("clear")
        else:
            os.system("cls")
        Art()
    
    elif formated == "show methods": #fix spellng
        print("\nTrading Methods: ")
        print("\n  Exponential Moving Average Crossover(EMAC)")
        print("\n  Relative Strength Index(RSI)")
        print("\n  Moving Average Convergence Diviergence(MACD)")

    elif formated == "use emac":
        mode = "EMAC"
        global emacDict
        emacDict = {
            "usersi": "False",
            "shortlen": "50",
            "longlen": "200",
            "pair" : "BTC/USDT",
            "interval": "5m",
            "amount": "0",
            "trades": "10"
        }
        while True:
            userInput = input("\nbot/EMAC > ")
            if "set" in userInput.lower().strip():
                userInput = userInput.removeprefix("set ")
                userInput = userInput.split(" ")
                
                emacDict[userInput[0]] = userInput[1]

                print("")
                PrintEmacParams()
            elif userInput == "run" or userInput == "trade":
                EMAC(emacDict)

            else:
                Check(userInput)

    elif formated == "use rsi":
        mode = "RSI"
        global rsiDict
        rsiDict = {
            "buyrsi": "30",
            "sellrsi": "70",
            "pair": "BTC/USDT",
            "interval": "5m",
            "amount": "0",
            "trades": "10"
        }
        while(True):
            userInput = input("\nbot/RSI > ")
            if "set" in userInput.lower().strip():
                userInput = userInput.removeprefix("set ")
                userInput = userInput.split(" ")
                
                rsiDict[userInput[0]] = userInput[1]

                print("")
                PrintRsiParams()
            elif userInput == "run" or userInput == "trade":
                RSI(rsiDict)

            else:
                Check(userInput)

    elif formated == "use macd":
        mode = "MACD"
        global macdDict
        macdDict = {
            "usersi": "True",
            "pair": "BTC/USDT",
            "interval": "5m",
            "amount": "0",
            "trades": "10"
        }
        while(True):
            userInput = input("\nbot/MACD > ")
            if "set" in userInput.lower().strip():
                userInput = userInput.removeprefix("set ")
                userInput = userInput.split(" ")
                
                macdDict[userInput[0]] = userInput[1]

                print("")
                PrintMacdParams()
            elif userInput == "run" or userInput == "trade":
                MACD(macdDict)
            else:
                Check(userInput)

    elif formated == "show options" and mode == "EMAC":
        print("\nDescription: The EMAC method utilizes two exponential moving averages of a cryptocurrency of your choice,\none EMA is calculated over a shorter period of time than the other. When the EMA that is calculated over \nthe shorter period of time crosses the EMA that is calculated over the longer period of time, signalling \nthat the crypto’s price is increasing, the bot proceeds to buy. When the opposite is to happen, the EMA \nthat is calculated over a longer period of time crosses the other, signalling that the crypto’s price is \ndecreasing, the bot proceeds to sell the crypto that it bought in the previous step.")
        print("\nAPI Requirments: Taapi.io and KuCoin")
        print("\nParameters: ")
        PrintEmacParams()

    elif formated == "show options" and mode == "RSI":
        print("\nDescription: The RSI method utilizes the relative strength index of a cryptocurrency of your choice, the RSI \nis calculated over a specified time period. When the RSI is less than 30 or the value that you have assigned, \nsignalling that the crypto is oversold, the bot proceeds to buy. When the RSI is greater than 70 or the value \nthat you have assigned, signaling that the crypto is overbought, the bot proceeds to sell.")
        print("\nAPI Requirments: Taapi.io and KuCoin")
        print("\nParameters: ")
        PrintRsiParams()

    elif formated == "show options" and mode == "MACD":
        print("\nDescriptions: The MACD method utilizes the difference between two exponential moving averages of a cryptocurrency \nof your choice, as well as the average of the aforementioned difference over a specified period of time. When the \ndifference (MACD line) crosses above the average of the differences (signal line), signalling that the crypto’s \nprice is increasing, the bot proceeds to buy. When the signal line crosses above the MACD line, signalling that \nthe cryptos price is decreasing, the bot proceeds to sell.")
        print("\nAPI Requirments: Taapi.io and KuCoin")
        print("\nParameters: ")
        PrintMacdParams()

    elif formated == "empty keys" and input("\nAre you sure(Y/N): ").strip().lower() == "y":
        print("FLUSHING KEYS.PY")
        file = open("Keys.py", "w")
        file.flush()
        file.close()
        sys.exit()
    elif formated == "exit":
        sys.exit()
    
    elif "analyze" in formated:
        fileName = formated.split(" ")[1]
        data = pd.read_csv(fileName)
        headers = []
        for line in data:
            headers.append(line)

        if "EMASHORT" in headers:
            if "RSI" in headers:
                GraphTriple(fileName, headers[1], headers[2], "EMA")
            else:
                GraphDouble(fileName, headers[1], headers[2], "EMA")
        elif "MACD" in headers:
            if "RSI" in headers:
                GraphTriple(fileName, headers[1], headers[2], "MACD")
            else:
                GraphDouble(fileName, headers[1], headers[2], "MACD")
        else:
            GraphRSI(fileName)