from bs4 import BeautifulSoup
import requests

html_text = requests.get('http://books.toscrape.com/index.html')

soup = BeautifulSoup(html_text, 'lxml')
job = soup.find('ol', class_ = 'row').text
print(job)