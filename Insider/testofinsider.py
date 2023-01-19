import yfinance
import requests #<--- to get webpages in their html form
from bs4 import BeautifulSoup #<-- to parse html and find specific elements
import csv
from datetime import datetime, timedelta
from math import isnan

avg = 0
count = 0

url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=1461&fdr=&td=0&tdr=&fdlyl=1&fdlyh=&daysago=&xp=1&vl=1000&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&isceo=1&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1"

mydict = {}

#this code gets tickers and dates for the url
requestvalue = requests.get(url)
soup = BeautifulSoup(requestvalue.content, "html.parser")

for i in soup.find("table", class_="tinytable").find("tbody").find_all("tr"):
    date = i.find("a").get_text()
    ticker = i.find("b").find("a").get_text()
    mydict[ticker] = date

#print(mydict)

#changes the date from string to datetime object. 

def datemod(date):
    var = []
    var1 = 0
    for c in date:
        if var1 < 10:
            var.append(c)
            var1 += 1
    a_string = "".join(var)
    return datetime.strptime(a_string, r"%Y-%m-%d") + timedelta(1)


#adds one day to the date
def datemod1(date):
    days = timedelta(1)
    return date + days

#finds the average of stock price fluctuations and returns this average.

print(mydict)

for i in mydict.items():
    per =0
    c = list(yfinance.Ticker(i[0]).history(start=datemod1(datemod(i[1]) + timedelta(3)), end=datemod1(datemod(i[1]) + timedelta(7))).to_dict()["Close"].values())
    o = list(yfinance.Ticker(i[0]).history(start=datemod(i[1]), end=datemod1(datemod(i[1]))).to_dict()["Open"].values())
    if (len(c) !=0 and type(c[0]) == float and isnan(c[0]) == False) and (len(o) != 0 and type(o[0]) == float and isnan(o[0]) == False):
        dif = float(c[0])-float(o[0])
        per = dif/o[0]
        print(dif)
        print("Ticker: " + str(i[0]))
        print("Stock Open: " + str(o[0]))
        print("Stock Close: " + str(c[0]))
        print("This is the percentage change in value = " + str(per))
        avg += per
        count +=1


print("avg is " + str(avg/count))
print(count)