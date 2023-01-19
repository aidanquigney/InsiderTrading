import requests #<--- to get webpages in their html form
from bs4 import BeautifulSoup #<-- to parse html and find specific elements
import pandas_datareader.data as web
import pandas
import datetime as dt
import pandas as pd

avg = 0
count = 0
count2= 0
urllist =[]


mydict = {}

def dater(date):
    var = []
    var1 = 0
    for c in date:
        if var1 < 10:
            var.append(c)
            var1 += 1
    a_string = "".join(var)
    return dt.datetime.strptime(a_string, r"%Y-%m-%d")

def appender(urlsoup):
    global count2 
    for i in urlsoup.find("table", class_="tinytable").find("tbody").find_all("tr"):
        date = i.find("a").get_text()
        ticker = i.find("b").find("a").get_text()
        mydict[ticker + str(count2).zfill(4)] = dater(date)
        
        count2 +=1

for i in range(1, 7):
    urllist.append(BeautifulSoup(requests.get("http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=1461&fdr=&td=0&tdr=&fdlyl=1&fdlyh=&daysago=&xp=1&vl=1000&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=1000&page=" + str(i)).content, "html.parser"))

for i in urllist:
    appender(i)

print(len(urllist))
print(mydict)

def stock(stock, start, end):
    avg1 = 0
    count1=0
    try:
        if end.weekday() !=5 and start.weekday() != 6: 
            df = web.DataReader(stock, "yahoo", start, end)
            opens = list(df.to_dict()["Open"].values())
            closes = list(df.to_dict()["Close"].values())
            o = opens[0]
            c =  closes[len(closes )-1]
            print("ticker: " + stock)
            print("open: " + str(o))
            print("close: " + str(c))
            dif = c - o - .34
            per = dif/ o
            print("per change: " + str(per))
            if per != 0:
                avg1 += per
                count1 +=1
    except:
        print("fail")
    return [avg1, count1]


for i in mydict.items():
    a =stock(i[0].strip("0123456789"), (i[1] + dt.timedelta(days=1)), (i[1] + dt.timedelta(days=1)))
    avg += a[0]
    count += a[1]
    if count != 0:
        print("Average: " + str(avg/count))


