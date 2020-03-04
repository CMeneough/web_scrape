## Search phrases on Bing then scrap the data from the listed websites

import pandas as pd
import requests
from random import uniform
import time
from bs4 import BeautifulSoup
import urllib
import eventlet
from datetime import datetime

## Import Data o
startTime = datetime.now()
print(startTime)

df = pd.read_csv('data.csv')

list = df['search_phrase']
search_phrase = list.values

## Pull from 4 pages. Add 49,63,+14 for more pages
pages = [1,7,21,35]

## Download and save the URLs from the search results

phrases = []
url_list = []
text_data = []

## Web Scrape Bing for the URLs then Scrap the text from those URLs
for item in search_phrase:
    for page in pages:
        with eventlet.Timeout(50):
            query = 'https://www.bing.com/search?q={}&first={}&FORM=PERE'.format(urllib.parse.quote_plus(item),page)

            eventlet.sleep(uniform(1,2))

            try:
                temp_url_list = []

                getRequest = urllib.request.Request(query, None, {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'})

                urlfile = urllib.request.urlopen(getRequest)
                htmlResult = urlfile.read(200000)
                urlfile.close()
                soup = BeautifulSoup(htmlResult,'lxml')

                results = soup.findAll('li', { "class" : "b_algo" })
                for result in results:
                    temp_url_list.append((result.find('a',href=True).get('href')))

    ### text from url

                for x in temp_url_list:
                    try:
                        with eventlet.Timeout(12):
                            res = requests.get(x,allow_redirects=False, timeout=8)
                            html_page = res.content
                            soup = BeautifulSoup(html_page, 'lxml')
                            for script in soup(["script", "style"]):
                                script.extract()
                            text = soup.get_text()
                            text_data.append(text)
                            url_list.append(x)
                            phrases.append(item)
                            eventlet.sleep(uniform(1,2))
                    except Exception as e:
                        print(e)
                        print(datetime.now())
                        pass
                    except (eventlet.TimeoutError, eventlet.Timeout):
                        print('timeout and skip')
                        print(datetime.now())
                        pass

            except Exception as e:
                print(e)
                print(datetime.now())
                pass

## Create DataFrame
data = pd.DataFrame({'search_phrase':phrases,'url':url_list,'text':text_data})

print(datetime.now() - startTime)
