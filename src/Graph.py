import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def GraphTriple(fileName, first, second, gen):
    times = []
    listOne = []
    listTwo = []
    rsi = []
    price = []
    counter = 0

    data = pd.read_csv(fileName)
    trades = data[(data["TRADED"] == "Bought") | (data["TRADED"] == "Sold")]

    fig, ax = plt.subplots(1, 3)

    for x in range(int(len(trades) / 2)):
        dates = []
        prices = []
        dates.append(datetime.strptime(trades.iat[counter, 4], "%m/%d/%Y %H:%M:%S"))
        dates.append(datetime.strptime(trades.iat[counter + 1, 4], "%m/%d/%Y %H:%M:%S"))
        prices.append(float(trades.iat[counter, 0]))
        prices.append(float(trades.iat[counter + 1, 0]))
        if x == len(trades) / 2 - 1:
            ax[1].plot_date(dates, prices, "k-", zorder=10, lw="3", label="Trades")
        else:
            ax[1].plot_date(dates, prices, "k-", zorder=10, lw="3")
        counter += 2

    for line in data["TIME"]:
        times.append(datetime.strptime(line, "%m/%d/%Y %H:%M:%S"))

    for line in data[first]:
        listOne.append(float(line))

    for line in data[second]:
        listTwo.append(float(line))

    for line in data["RSI"]:
        rsi.append(float(line))

    for line in data["CURRENTPRICE"]:
        price.append(float(line))

    ax[0].plot_date(times, listOne, "b-" ,label=first, lw="2")
    ax[0].plot_date(times, listTwo, "r-" ,label=second, lw="2")
    ax[1].plot_date(times, price, "g-", label="Price", lw="2")
    ax[2].plot_date(times, rsi, "m-", label="RSI", lw="2")

    ax[0].set_title(gen, loc="center")
    ax[1].set_title("Price", loc="center")
    ax[2].set_title("RSI", loc="center")

    ax[0].set_xlabel("Time")
    ax[1].set_xlabel("Time")
    ax[2].set_xlabel("Time")

    ax[0].set_ylabel("Price (USD)")
    ax[1].set_ylabel("Price (USD)")
    ax[2].set_ylabel("Relative Strenght Index")

    ax[0].legend()
    ax[1].legend()
    ax[2].legend()

    ax[0].grid()
    ax[1].grid()
    ax[2].grid()

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.tight_layout()
    plt.gcf().autofmt_xdate()

    plt.show()

def GraphDouble(fileName, first, second, gen):
    times = []
    listOne = []
    listTwo = []
    price = []
    counter = 0

    data = pd.read_csv(fileName)
    trades = data[(data["TRADED"] == "Bought") | (data["TRADED"] == "Sold")]

    fig, ax = plt.subplots(1, 2)


    for x in range(int(len(trades) / 2)):
        dates = []
        prices = []
        dates.append(datetime.strptime(trades.iat[counter, 3], "%m/%d/%Y %H:%M:%S"))
        dates.append(datetime.strptime(trades.iat[counter + 1, 3], "%m/%d/%Y %H:%M:%S"))
        prices.append(float(trades.iat[counter, 0]))
        prices.append(float(trades.iat[counter + 1, 0]))
        if x == len(trades) / 2 - 1:
            ax[1].plot_date(dates, prices, "k-", zorder=10, lw="3", label="Trades")
        else:
            ax[1].plot_date(dates, prices, "k-", zorder=10, lw="3")
        counter += 2

    for line in data["TIME"]:
        times.append(datetime.strptime(line, "%m/%d/%Y %H:%M:%S"))

    for line in data[first]:
        listOne.append(float(line))

    for line in data[second]:
        listTwo.append(float(line))

    for line in data["CURRENTPRICE"]:
        price.append(float(line))

    ax[0].plot_date(times, listOne, "b-" ,label=first, lw="2")
    ax[0].plot_date(times, listTwo, "r-" ,label=second, lw="2")
    ax[1].plot_date(times, price, "m-", label="Price", lw="2")

    ax[0].set_title(gen, loc="center")
    ax[1].set_title("Price", loc="center")

    ax[1].set_xlabel("Time")
    ax[0].set_xlabel("Time")

    ax[0].set_ylabel("Price (USD)")
    ax[1].set_ylabel("Price (USD)")

    ax[0].legend()
    ax[1].legend()

    ax[0].grid()
    ax[1].grid()

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.tight_layout()
    plt.gcf().autofmt_xdate()

    plt.show()

def GraphRSI(fileName):
    times = []
    rsi = []
    price = []
    counter = 0

    data = pd.read_csv(fileName)
    trades = data[(data["TRADED"] == "Bought") | (data["TRADED"] == "Sold")]

    fig, ax = plt.subplots(1, 2)

    for x in range(int(len(trades) / 2)):
        dates = []
        prices = []
        dates.append(datetime.strptime(trades.iat[counter, 2], "%m/%d/%Y %H:%M:%S"))
        dates.append(datetime.strptime(trades.iat[counter + 1, 2], "%m/%d/%Y %H:%M:%S"))
        prices.append(float(trades.iat[counter, 0]))
        prices.append(float(trades.iat[counter + 1, 0]))
        if x == len(trades) / 2 - 1:
            ax[1].plot_date(dates, prices, "k-", zorder=10, lw="3", label="Trades")
        else:
            ax[1].plot_date(dates, prices, "k-", zorder=10, lw="3")
        counter += 2

    for line in data["TIME"]:
        times.append(datetime.strptime(line, "%m/%d/%Y %H:%M:%S"))

    for line in data["RSI"]:
        rsi.append(float(line))

    for line in data["CURRENTPRICE"]:
        price.append(float(line))

    ax[0].plot_date(times, rsi, "m-" ,label="RSI", lw="2")
    ax[1].plot_date(times, price, "g-", label="Price", lw="2")

    ax[0].set_title("RSI", loc="center")
    ax[1].set_title("Price", loc="center")

    ax[1].set_xlabel("Time")
    ax[0].set_xlabel("Time")

    ax[0].set_ylabel("Relative Strenght Index")
    ax[1].set_ylabel("Price (USD)")

    ax[0].legend()
    ax[1].legend()

    ax[0].grid()
    ax[1].grid()

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.tight_layout()
    plt.gcf().autofmt_xdate()

    plt.show()

