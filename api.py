#!/usr/bin/env python3

from types import coroutine
from typing import List
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, time, sys, datetime

class style:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    divider = "------------------------------------------------------------------------------------------"
    goback = "\033[F" * 10

def terminalSizeToReload(string, count):
    i = 0
    multiplier = 1
    while i < len(string):
        if (string[i] == "\n"):
            multiplier += 1
        i += 1
    p = multiplier + count
    return ("\033[F" * p)

def getDataApi():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'55',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '[YOUR API KEY]',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        return(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def putDataInJsonFile(data_api_str):
    open('data.json', 'w').close()
    f = open('data.json', 'a')
    i = 0
    indexBr = 0
    brOpen = 0

    while i < len(data_api_str):
        if ((data_api_str[i - 1] == "{") or (data_api_str[i - 1] == "[")):
            brOpen += 1
            f.write('\n')
            while indexBr < brOpen:
                f.write('\t')
                indexBr += 1
            indexBr = 0
        if ((data_api_str[i] == "}") or (data_api_str[i] == "]")):
            brOpen -= 1
            f.write('\n')
            while indexBr < brOpen:
                f.write('\t')
                indexBr += 1
            indexBr = 0
        if (data_api_str[i - 1] == ","):
            f.write("\n")
            while indexBr < brOpen:
                f.write('\t')
                indexBr += 1
            indexBr = 0
        f.write(data_api_str[i])
        i += 1
    f.close()

def spaceThousand(value):
    string = str(value)
    i = len(string)
    isInt = False
    th = -1
    newValue = ""
    i -= 1
    m = 0
    while i >= 0:
        if (isInt):
            th += 1
            if (th == 3):
                newValue += " "
                th = 0
                m += 1
        if (string[i] == "."):
            isInt = True

        newValue += string[i]
        i -= 1
    return(newValue[::-1])

def rt(value):
    lenght = len(value)
    i = 0
    th = 0
    res = ""
    while i < lenght:
        if value[i] == " ":
            th += 1
        i += 1
    
    i = 0
    while (value[i] != " "):
        res += value[i]
        i += 1
    
    if (th == 1):
        res = res[::-1]
        res += " k"
        res = res[::-1]
    elif (th == 2):
        res = res[::-1]
        res += " M"
        res = res[::-1]
    elif (th == 3):
        res = res[::-1]
        res += " B"
        res = res[::-1]
    return res

def positiveOrNegative(data):
    if (data[0] == '-'):
        return ("⤵ " + style.FAIL + data + style.ENDC)
    else:
        return ("⤴  " + style.OKGREEN + data + style.ENDC)
    

def valueOfCrypto(data, i):
    name = data['data'][i]['name']
    symbol = data['data'][i]['symbol']
    price = spaceThousand(round(data['data'][i]['quote']['USD']['price'], 2))
    volume24 = rt(spaceThousand(round(data['data'][i]['quote']['USD']['volume_24h'], 2)))
    percentChange1h = positiveOrNegative(spaceThousand(round(data['data'][i]['quote']['USD']['percent_change_1h'], 2)))
    percentChange24h = positiveOrNegative(spaceThousand(round(data['data'][i]['quote']['USD']['percent_change_24h'], 1)))

    stdoutName = "(" + style.BOLD + symbol + style.ENDC + ") " + name
    stdoutPrice = style.BOLD + price + style.ENDC

    stdoutFinalValue = "  " + str(i + 1) + "\t" + stdoutName[0:23] + "\t\t" + percentChange1h + "\t" + percentChange24h + "\t\t" + volume24 + "\t\t" + "$ " + stdoutPrice + "\n"

    return (stdoutFinalValue)

def sumOfMarket(data, numberOfCrypto):
    total = 0
    i = 0
    while i < numberOfCrypto:
        total += data['data'][i]['quote']['USD']['percent_change_1h']
        i += 1
    return(positiveOrNegative(str(round(total / numberOfCrypto, 2))))

def display(data, timer, countOfCrypto):
    now = datetime.datetime.now()
    header = style.BOLD + "\nRefresh limit: " + str(timer) + "s\t\t\t" + now.strftime("-| %H:%M:%S |-\t\t\t") + "Market: " + sumOfMarket(data, countOfCrypto) + " %" + "\n\n" + style.divider + "\n" + "  #\tName\t\t\t1h %\t24h %\t\tVolume/24h\tPrice" + "\n" + style.divider + style.ENDC + "\n"

    def countOfCryptoToDisplay(i, data):
        count = 0
        value = ""
        value += header
        while count < i:
            value += "{}".format(valueOfCrypto(data, count))
            count += 1
        value += terminalSizeToReload(header, count)
        return (value)
    res = countOfCryptoToDisplay(countOfCrypto, data)
    print(res)

def loadData(timeFrame, countOfCrypto):
    while True:
        putDataInJsonFile(getDataApi())
        with open('data.json') as f:
            display(json.load(f), timeFrame, countOfCrypto)
        time.sleep(timeFrame)

def aver(av):
    if (len(av) < 2 or len(av) > 3 or len(av) == 2):
        print(style.FAIL + "\nError: number of arguments\n" + style.ENDC + "\nFor help type: \"./api.py help\"" + style.ENDC + "\nERROR_CODE: 84\n")
        exit(84)
    if (int(av[1]) < 0 or int(av[1]) > 20):
        print(style.FAIL + "\nError: bad arguments (time frame must be at least one and at max 20)\n" + style.ENDC + "\nFor help type: \"./api.py help\"" + style.ENDC + "\nERROR_CODE: 84\n")
        exit(84)
    if (int(av[2]) < 0 or int(av[2]) > 55):
        print(style.FAIL + "\nError: bad arguments (Number of crypto must be at least one and at max 55)\n" + style.ENDC + "\nFor help type: \"./api.py help\"" + style.ENDC + "\nERROR_CODE: 84\n")
        exit(84)

def main():
    
    aver(sys.argv)

    try:
        loadData(int(sys.argv[1]), int(sys.argv[2]))
    except:
        print(style.OKGREEN + "Program end without error" + style.ENDC)
        exit(0)
    
main()