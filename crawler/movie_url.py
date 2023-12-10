import csv
import pandas as pd
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

df = pd.read_csv('movies.dat', delimiter='::', header=None, 
    names=['movie_id', 'title', 'genre'], engine='python')

for i, row in df.iterrows():
    movie_id = row['movie_id']
    movie_title = row['title']
    domain = 'http://www.imdb.com'
    search_url = domain + '/find?q=' + urllib.parse.quote_plus(movie_title)
    with urllib.request.urlopen(search_url) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        # Get url of 1st search result
        try:
            title = soup.find('table', class_='findList').tr.a['href']
            movie_url = domain + title
            with open('movie_url.csv', 'a', newline='') as out_csv:
                writer = csv.writer(out_csv, delimiter=',')
                writer.writerow([movie_id, movie_url])
            # Ignore cases where search returns no results
        except AttributeError:
            pass