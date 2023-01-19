import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import pandas
import datetime as dt
import pandas as pd

start = dt.datetime(2015,1,5)
end = start + dt.timedelta(days = 1)

if start.weekday() != 4 and start.weekday() != 5 and start.weekday() != 6:
    df = web.DataReader("TSLA", "yahoo", start, end)
    opens = list(df.to_dict()["Open"].values())
    print(opens[1])


