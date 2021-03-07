# from google.cloud import language_v1
import os
import time
import datetime
import pickle
import pandas as pd
import numpy as np

"""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="moodFinder-2d03c34a57da.json"
# Instantiates a client
client = language_v1.LanguageServiceClient()
"""

def create_df():
    titles = open("/Users/jennyromero/Desktop/code/STOCKS/titles.p","rb")
    titles = pickle.load(titles)

    times = open("/Users/jennyromero/Desktop/code/STOCKS/time.p","rb")
    times = pickle.load(times)
    times = [int(float(i)) for i in times] 
    for i in range(len(times)):
        time = times[i]
        time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d')
        times[i] = time

    upvotes = open("/Users/jennyromero/Desktop/code/STOCKS/upvotes.p","rb")
    upvotes = pickle.load(upvotes)

    mag = open("/Users/jennyromero/Desktop/code/stocks/magnitude.p","rb")
    mag = pickle.load(mag)
    mag = [float(i) for i in mag]

    sent = open("/Users/jennyromero/Desktop/code/STOCKS/sent.p","rb")
    sent = pickle.load(sent)
    sent = [float(i) for i in sent]

    tickers = open("/Users/jennyromero/Desktop/code/STOCKS/tickers.p", "rb")
    tickers = pickle.load(tickers)

    cleaned_tickers = []
    for tick in tickers:
        temp = tick.replace(" ", "")
        temp = temp.replace("$", "")
        cleaned_tickers.append(temp)

    df = pd.DataFrame(
    {'Date': times,
    'Ticker': cleaned_tickers,
    'Post_Title': titles,
    'upvotes': upvotes,
    'sentiment': sent,
    'magnitude': mag
    })

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    #print(df.info())
    #print(df.head(10))
    return df

tickers = open("/Users/jennyromero/Desktop/code/STOCKS/tickers.p", "rb")
tickers = pickle.load(tickers)

cleaned_tickers = []
for tick in tickers:
    temp = tick.replace(" ", "")
    temp = temp.replace("$", "")
    cleaned_tickers.append(temp)

df = create_df() 

#returns dictionary where key is ticker, value is dataframe of all observations with that ticker
def create_tickerseries():
    ticker_timeseries = dict()
    ticker_timeseries = {key: 0 for key in cleaned_tickers}
    for key in ticker_timeseries.keys():
        curr_df = df.loc[df['Ticker'] == key] 
        ticker_timeseries[key] = curr_df
    return ticker_timeseries


ticker_timeseries = create_tickerseries()
#print(ticker_timeseries['GME'])


#get sentiment of ticker over time
#accepts list of sentiments and list of magnitudes
def aggregate_sent(sent, mag, sub_df):
    result = 0
    magsum = 0
    print(type(mag))
    print(type(sent))
    print(type(sub_df))
    #assert(len(sent) == len(mag))
    for i in range(len(sent)):
        result += sent[i]*mag[i]
        magsum += mag[i]
    if magsum == 0: return 0
    return result/magsum


# TODO: finish this lmao
sentiment_timeseries = dict()
sentiment_timseries = {key: 0 for key in cleaned_tickers}

#total_df = pd.DataFrame(index=index, columns=columns)
#total_df = total_df.fillna(0) # with 0s rather than NaNs


total_df = pd.DataFrame(columns=['Date', 'Ticker', 'Post_Title', 'upvotes', 'sentiment', 'magnitude'])

unique_dates = []

for key in ticker_timeseries.keys():
    
    curr_df = ticker_timeseries[key]
    #total_df = total_df.append(curr_df)


    columns = ['Ticker', 'Sentiment Score']
    #use set to get the unique dates
    dates = list(set(curr_df.index.tolist()))
    unique_dates.append(dates)
    #print(dates)
    #want to populate this dataframe
    #each date will have a ticker and sentiment score
    new_df = pd.DataFrame(index = dates, columns = columns)
    total_df.append(new_df)
    
    #grouped_by_data = curr_df
    #print("CURRENT DF")
    #print("current_df",curr_df)
    
    for date in dates:
        #print("hi")
        #print("date", date)
        sub_df = curr_df.loc[date]
        total_df.append(sub_df)
        #sent = sub_df['sentiment'].tolist()
        #mag = sub_df['magnitude'].tolist()
        #agg_sent = aggregate_sent(sent, mag, sub_df)
        #new_df.loc[date] = [key] + [agg_sent]
#-->print(total_df)
#print(total_df)
#grouped = total_df.groupby(['Ticker'], sort = False)
#print(type(total_df["Date"]))

#series = total_df["Date"]


#print(series).
#type(series[1])

#total_df.groupby(['Ticker']).mean()
group_data = df.groupby(['Date','Ticker']) #sum function ['sentiment'].mean()
group_data = group_data["sentiment","upvotes"].agg([np.mean,np.sum])

html = group_data.to_html()
#total_df.groupby(['Ticker'], as_index=False).mean().groupby('sentiment')['magnitude'].mean()
#total_df.groupby(level="Date").mean()
#print(type(html))

result = html.replace("\n", "")

#lets me pass on the html stuff on another file
def pass_on_html():
    print('in fixed_sentiments, unproductive')
    return result

if __name__ == '__main__':
    pass_on_html()