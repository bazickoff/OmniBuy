from datetime import datetime
from Functions import SheetSetup, KeySetup, Buy, Sell
from kucoin.client import Trade
import sys
from tradingview_ta import TA_Handler
import csv
from time import sleep

def MACD(macdDict):
    sheet = SheetSetup()
    title = datetime.now().strftime("%H-%M-%S")
    csvFile = open(title + ".csv", "w", newline="")
    csvWriter = csv.writer(csvFile)

    kuKey, kuPass, kuSecret = KeySetup()
    kuPair = macdDict["pair"].upper().replace("/", "-")
    taPair = macdDict["pair"].split("/")
    taPair = taPair[0] + taPair[1]
    funds = macdDict["amount"]

    client = Trade(key=kuKey, secret=kuSecret, passphrase=kuPass)

    handler = TA_Handler(
        screener="CRYPTO",
        exchange="BINANCE",
        symbol=taPair,
        interval=macdDict["interval"]
    )

    try:
        handler.get_analysis()
        client.get_order_list()
    except Exception as x:
        print(x)
        sys.exit()

    if macdDict["usersi"].strip().lower() == "false":
        useRsi = False
    else:
        useRsi = True

    analysis = handler.get_analysis().indicators
    macd = analysis["MACD.macd"]
    signal = analysis["MACD.signal"]

    # so it doesnt buy while macd is over signal when startup
    while macd > signal:
        try:
            analysis = handler.get_analysis().indicators
            macd = analysis["MACD.macd"]
            signal = analysis["MACD.signal"]
        except Exception as x:
            print(x)
            continue
        print(f"Waiting for Signal to crossover MACD before starting the bot, macd={macd}, signal={signal}, time={datetime.time(datetime.now().replace(microsecond=0))}")
        sleep(5)

    counter = 0
    listCounter = 0
    csvList = []

    if useRsi:
        csvList.append(["CURRENTPRICE", "MACD", "SIGNAL", "RSI", "TIME", "TRADED"])
    else:
        csvList.append(["CURRENTPRICE", "MACD", "SIGNAL", "TIME", "TRADED"])

    while True:
        toWrite = []
        if counter >= int(macdDict["trades"]):
            for line in csvList:
                csvWriter.writerow(line)
            csvFile.close()
            return

        try:
            analysis = handler.get_analysis().indicators
            macd = analysis["MACD.macd"]
            signal = analysis["MACD.signal"]
            currentPrice = analysis["close"]

            if csvList[listCounter][0] != currentPrice and useRsi == False:
                toWrite.append(currentPrice)
                toWrite.append(macd)
                toWrite.append(signal)
                toWrite.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                listCounter += 1
            now = datetime.now().strftime("%H:%M:%S")
        except Exception as x:
            print(x)
            continue

        if useRsi:
            rsi = analysis["RSI"]
            print(f"MACD={macd}, signal={signal}, rsi={rsi}, currentPrice={currentPrice}, time={now}")

            if csvList[listCounter][0] != currentPrice:
                toWrite.append(currentPrice)
                toWrite.append(macd)
                toWrite.append(signal)
                toWrite.append(rsi)
                toWrite.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                listCounter += 1
        else:
            rsi = 50
            print(f"MACD={macd}, signal={signal}, currentPrice={currentPrice}, time={now}")

        if len(toWrite) > 0:
            csvList.append(toWrite)

        if macd > signal and rsi < 70:
            timeBought, size, feesPaid, startFunds, buyPrice = Buy(kuPair, funds, client, currentPrice)
            csvList[len(csvList) - 1].append("Bought")

            while True:
                toWrite = []
                try:
                    analysis = handler.get_analysis().indicators
                    macd = analysis["MACD.macd"]
                    signal = analysis["MACD.signal"]
                    currentPrice = analysis["close"]

                    if csvList[listCounter][0] != currentPrice and useRsi == False:
                        toWrite.append(currentPrice)
                        toWrite.append(macd)
                        toWrite.append(signal)
                        toWrite.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                        listCounter += 1
                    now = datetime.now().strftime("%H:%M:%S")
                except:
                    continue

                if useRsi:
                    rsi = analysis["RSI"]
                    print(f"MACD={macd}, signal={signal}, rsi={rsi}, buy price={buyPrice}, current price={currentPrice}, time={now}")
                    if csvList[listCounter][0] != currentPrice:
                        toWrite.append(currentPrice)
                        toWrite.append(macd)
                        toWrite.append(signal)
                        toWrite.append(rsi)
                        toWrite.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
                        listCounter += 1
                else:
                    print(f"MACD={macd}, signal={signal}, buy price={buyPrice}, current price={currentPrice}, time={now}")
                    rsi = 50

                if len(toWrite) > 0:
                    csvList.append(toWrite)

                if signal > macd and rsi > 30:
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
