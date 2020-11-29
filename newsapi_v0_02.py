from newsapi import NewsApiClient
import datetime as dt
import pandas as pd

my_api_key = '2a1486be989242338d4cf8f1d2920538'


newsapi = NewsApiClient(api_key=my_api_key)

data = newsapi.get_everything(q="kazakh covid-19", page_size=100)
# data = newsapi.get_top_headlines(q="covid-19", country='')

print(data.keys())

# for i, x in enumerate(data['articles']):
#     print(f"{i:3} - {x['title']}")
for key, value in data['articles'][0].items():
    print(f"\n{key.ljust(20)} {value}")
# for key, value in data['articles'][0].items():
#     print(f"\n{key.ljust(16)} {type(value)}")
# print(f"\n{pd.DataFrame(data['articles'])}")


