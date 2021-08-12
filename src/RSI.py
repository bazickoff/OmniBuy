from datetime import datetime
from Functions import SheetSetup, KeySetup, Buy, Sell
from kucoin.client import Trade
from tradingview_ta import TA_Handler
import sys
import csv
from time import sleep

def RSI(rsiDict):
    sheet = SheetSetup()
    title = datetime.now().strftime("%H-%M-%S")
    csvFile = open(title + ".csv", "w", newline="")
    csvWriter = csv.writer(csvFile)

    kuKey, kuPass, kuSecret = KeySetup()
    kuPair = rsiDict["pair"].upper().replace("/", "-")
    taPair = rsiDict["pair"].split("/")
    taPair = taPair[0] + taPair[1]
    funds = rsiDict["amount"]

    client = Trade(key=kuKey, secret=kuSecret, passphrase=kuPass)

    handler = TA_Handler(
        screener="CRYPTO",
        exchange="BINANCE",
        symbol=taPair,
        interval=rsiDict["interval"]
    )

    try:
        handler.get_analysis()
        client.get_order_list()
    except Exception as x:
        print(x)
        sys.exit()

    counter = 0
    listCounter = 0
    csvList = []
    csvList.append(["CURRENTPRICE", "RSI", "TIME", "TRADED"])

    while True:
        toWrite = []
        if counter >= int(rsiDict["trades"]):
            for line in csvList:
                csvWriter.writerow(line)
            csvFile.close()
            return
        try:
            analysis = handler.get_analysis().indicators
            rsi = analysis["RSI"]
            currentPrice = analysis["close"]
            time = datetime.now().strftime("%H:%M:%S")

            if csvList[listCounter][0] != currentPrice:
                toWrite.append(currentPrice)
                toWrite.append(rsi)
                toWrite.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                listCounter += 1
            print(f"rsi={rsi}, currentPrice={currentPrice}, time={time}")
        except Exception as x:
            print(x)
            continue

        if len(toWrite) > 0:
            csvList.append(toWrite)

        if rsi <= int(rsiDict["buyrsi"]):
            timeBought, size, feesPaid, startFunds, buyPrice = Buy(kuPair, funds, client, currentPrice)
            csvList[len(csvList) - 1].append("Bought")

            while True:
                toWrite = []
                try:
                    analysis = handler.get_analysis().indicators
                    rsi = analysis["RSI"]
                    currentPrice = analysis["close"]
                    time = datetime.now().strftime("%H:%M:%S")

                    if csvList[listCounter][0] != currentPrice:
                        toWrite.append(currentPrice)
                        toWrite.append(rsi)
                        toWrite.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                        listCounter += 1
                    print(f"rsi={rsi}, currentPrice={currentPrice}, buyPrice={buyPrice}, time={time}")
                except Exception as x:
                    print(x)
                    continue
                
                if len(toWrite) > 0:
                    csvList.append(toWrite)

                if rsi >= int(rsiDict["sellrsi"]):
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
            