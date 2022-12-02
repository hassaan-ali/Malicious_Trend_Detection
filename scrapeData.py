from datetime import date
from pytrends.request import TrendReq
import os
import json
from time import sleep
from math import ceil
from googlesearch import search
import requests
import tweepy
import csv
import sys

####input your Twitter credentials here
consumer_key = 'l9Bt05rooG2Vfo5zCqtlrFtvp'
consumer_secret = 'ql1Gy4fupW73moobmSUxBT5n2g4CaMVcrSX802ZYB3MfU3EFQg'
access_token = '1590476064261906433-7cnjSxlCkLhIIdyBIYd2L4jKulOE46'
access_token_secret = 'aIJIaBGytKVgQYlRawde3CbdetxXxwSkwtusZtbazHM57'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# Define how many trends to pull and how to store them
TRENDS_COUNT = 10
TRENDS_HEADER = ['Date', 'Source'] + list('Trend ' + str(index + 1) for index in range(TRENDS_COUNT))
TRENDS_FILE = 'trends-record.csv'
DATE = date.today().isoformat()

#search results constants
URL_COUNT = 10
URL_FILE = "URLs-record.csv"
URL_HEADER = ['Date', 'Source', 'SearchEngine', 'Trend'] + list('URL ' + str(index + 1) for index in range(URL_COUNT))

# subscription key
BING_SUBSCRIPTION_KEY = 'd0138d4b9bf842c09dcba8d0058e0b74'

def getTrends():
    pytrends = TrendReq()
    trends = pytrends.trending_searches(pn = 'united_states')[0].tolist()[0:TRENDS_COUNT]
    print("Today's trends:", trends)
    appendCsv(TRENDS_FILE, TRENDS_HEADER, [DATE, 'Google'] + trends)
    return trends

def getTwitterTrends(loc_id, count):
    trends = api.get_place_trends(loc_id)
    trendList = [t['name'] for t in trends[0]['trends'][:count]]
    appendCsv(TRENDS_FILE, TRENDS_HEADER, [DATE, 'Twitter'] + trendList)
    print("Today's Twitter trends: ", trendList)
    return trendList

def appendCsv(filename, headers, data):
    with open(filename, mode = 'a') as file:
        if os.path.getsize(filename) == 0:
            file.write(','.join(headers) + '\n')
        file.write(','.join(data) + '\n')

#Search Google Results
def searchGoogleResults(trend, trendSource):
    results = list(search(trend, num_results=URL_COUNT))
    print("Search Results for", trend, ": ", results, "\n")
    appendCsv(URL_FILE, URL_HEADER, [DATE, trendSource, 'Google', trend] + results)

#Search Bing Results
def searchBingResults(bing_subscription_key,trendSource, trend):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_subscription_key}
    params = {
        "q": trend,
        "count": URL_COUNT,
        "responseFilter": "Webpages",
        "textDecorations": True,
        "textFormat": "HTML"}
    results = requests.get(search_url, headers = headers, params = params)
    urllist = []
    for i in range(0,10):
        urllist.append(results.json()['webPages']['value'][i]['url'])
    appendCsv(URL_FILE, URL_HEADER, [DATE, trendSource,'Bing', trend] + urllist)
    
        


if __name__ == "__main__":
    trends =  getTrends()
    for trend in trends:
        searchBingResults(BING_SUBSCRIPTION_KEY, 'Google', trend)
    for trend in trends:
       searchGoogleResults(trend, trendSource='Google')
    
    loc_id= 23424977 #Tweets for US region
    twitter_trends = getTwitterTrends(loc_id=loc_id, count= TRENDS_COUNT)  
    for twitter_trend in twitter_trends:
        searchBingResults(BING_SUBSCRIPTION_KEY, 'Twitter', twitter_trend)
    for twitter_trend in twitter_trends:
        searchGoogleResults(twitter_trend, trendSource='Twitter')
