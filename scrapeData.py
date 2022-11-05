from datetime import date
from pytrends.request import TrendReq
import os
import json
from time import sleep
from math import ceil
from googlesearch import search

# Define a constant for the result origin (search engine)
RESULT_SOURCE = 'Google'
# Define how many trends to pull and how to store them
TRENDS_COUNT = 10
TRENDS_HEADER = ['Date', 'Source'] + list('Trend ' + str(index + 1) for index in range(TRENDS_COUNT))
TRENDS_FILE = 'trends.csv'
DATE = date.today().isoformat()

#search results constants
URL_COUNT = 10
URL_FILE = "URLs.csv"
URL_HEADER = ['Date', 'Source', 'Trend'] + list('URL ' + str(index + 1) for index in range(URL_COUNT))

def getTrends():
    pytrends = TrendReq()
    trends = pytrends.trending_searches(pn = 'united_states')[0].tolist()[0:TRENDS_COUNT]
    print("Today's trends:", trends)
    appendCsv(TRENDS_FILE, TRENDS_HEADER, [DATE, RESULT_SOURCE] + trends)
    return trends

def appendCsv(filename, headers, data):
    with open(filename, mode = 'a') as file:
        if os.path.getsize(filename) == 0:
            file.write(','.join(headers) + '\n')
        file.write(','.join(data) + '\n')

def searchResults(trend):
    results = list(search(trend, num_results=URL_COUNT))
    print("Search Results for", trend, ": ", results, "\n")
    appendCsv(URL_FILE, URL_HEADER, [DATE, RESULT_SOURCE, trend] + results)
    return results

if __name__ == "__main__":
   trends =  getTrends()
   for trend in trends:
       results = searchResults(trend)