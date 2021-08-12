import sys
from time import sleep
import datetime
import csv
from kucoin.client import Trade
import kucoin
from tradingview_ta import TA_Handler
from Functions import SheetSetup, KeySetup, Buy, Sell

def EMAC(emacDict):
    sheet = SheetSetup()
    title = datetime.datetime.now().strftime("%H-%M-%S")
    csvFile = open(title + ".csv", "w", newline="")
    csvWriter = csv.writer(csvFile)

    kuKey, kuPass, kuSecret = KeySetup()

    client = kucoin(key=kuKey, secret=kuSecret, passphrase=kuPass)
    
    kuPair = emacDict["pair"].upper().replace("/", "-")
    taPair = emacDict["pair"].split("/")
    taPair = taPair[0] + taPair[1]
    funds = emacDict["amount"]

    handler = TA_Handler(
        screener="CRYPTO",
        exchange="BINANCE",
        symbol=taPair,
        interval=emacDict["interval"]
    )

    try:
        handler.get_analysis()
        client.get_order_list()
    except Exception as x:
        print(x)
        sys.exit()

    if emacDict["usersi"].lower() == "true":
        useRsi = True
    else:
        useRsi = False

    analysis = handler.get_analysis()
    shortEma = analysis.indicators["EMA" + emacDict["shortlen"]]
    longEma = analysis.indicators["EMA" + emacDict["longlen"]]

    while shortEma > longEma:
        try:
            analysis = handler.get_analysis().indicators
            shortEma = analysis["EMA" + emacDict["longlen"]]
            longEma = analysis["EMA" + emacDict["longlen"]]
        except Exception as x:
            print(x)
            continue
        print(f"Waiting for Golden Cross to end, shortEMA={shortEma}, longEMA={longEma}, time={datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))}")
        sleep(5)

    counter = 0
    listCounter = 0
    csvList = []
    if useRsi:
        csvList.append(["CURRENTPRICE", "EMASHORT", "EMALONG", "RSI", "TIME", "TRADED"])
    else:
        csvList.append(["CURRENTPRICE", "EMASHORT", "EMALONG", "TIME", "TRADED"])

    while True:
        toWrite = []
        if counter >= int(emacDict["trades"]):
            for line in csvList:
                csvWriter.writerow(line)
            csvFile.close()
            return

        try:
            analysis = handler.get_analysis().indicators
            shortEma = analysis["EMA" + emacDict["shortlen"]]
            longEma = analysis["EMA" + emacDict["longlen"]]
            currentPrice = analysis["close"]

            if csvList[listCounter][0] != currentPrice and useRsi == False:
                toWrite.append(currentPrice)
                toWrite.append(shortEma)
                toWrite.append(longEma)
                toWrite.append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                listCounter += 1
        except Exception as x:
            print(x)
            continue
        
        if useRsi:
            rsi = analysis["RSI"]
            print(f"shortEMA={shortEma}, longEMA={longEma}, rsi={rsi}, currentPrice={currentPrice}, time={datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))}")

            if csvList[listCounter][0] != currentPrice:
                toWrite.append(currentPrice)
                toWrite.append(shortEma)
                toWrite.append(longEma)
                toWrite.append(rsi)
                toWrite.append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                listCounter += 1
        else:
            rsi = 50
            print(f"shortEMA={shortEma}, longEMA={longEma}, currentPrice={currentPrice}, time={datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))}")

        if len(toWrite) > 0:
            csvList.append(toWrite)

        if shortEma > longEma and rsi < 70:
            timeBought, size, feesPaid, startFunds, buyPrice = Buy(kuPair, funds, client, analysis["close"])
            csvList[len(csvList) - 1].append("Bought")

            while True:
                toWrite = []
                try:
                    analysis = handler.get_analysis().indicators
                    shortEma = analysis["EMA" + emacDict["shortlen"]]
                    longEma = analysis["EMA" + emacDict["longlen"]]
                    currentPrice = analysis["close"]

                    if csvList[listCounter][0] != currentPrice and useRsi == False:
                        toWrite.append(currentPrice)
                        toWrite.append(shortEma)
                        toWrite.append(longEma)
                        toWrite.append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                        listCounter += 1
                except Exception as x:
                    print(x)
                    continue

                if useRsi:
                    rsi = analysis["RSI"]
                    print(f"shortEMA={shortEma}, longEMA={longEma}, rsi={rsi}, buy price={buyPrice}, current price={currentPrice}, time={datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))}")
                    
                    if csvList[listCounter][0] != currentPrice:
                        toWrite.append(currentPrice)
                        toWrite.append(shortEma)
                        toWrite.append(longEma)
                        toWrite.append(rsi)
                        toWrite.append(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                        listCounter += 1
                else:
                    print(f"shortEMA={shortEma}, longEMA={longEma}, buy price={buyPrice}, current price={currentPrice}, time={datetime.datetime.time(datetime.datetime.now().replace(microsecond=0))}")
                    rsi = 50

                if len(toWrite) > 0:
                    csvList.append(toWrite)
                if longEma > shortEma and rsi > 30:
                    timeSold, funds, feesPaid, finishFunds, sellPrice, date = Sell(kuPair, size, client, currentPrice, feesPaid)
                    csvList[len(csvList) - 1].append("Sold")
                    
                    try:
                        sheetParams = [str(date), str(timeBought), str(timeSold), float(feesPaid), float(finishFunds - startFunds), float((finishFunds - startFunds) / startFunds), float(buyPrice), float(sellPrice), str(kuPair)]
                        sheet.append_row(sheetParams)
                        counter += 1
                        
                        break
                    except:
                        print("ERROR APPENDING TO GOOGLE SHEET, EXITING")
                        sys.exit()
                sleep(3)
        sleep(3)

