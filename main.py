from bs4 import BeautifulSoup
import requests
import pandas as pd

def webScrap():
    base_url = 'https://books.toscrape.com/catalogue/page-'
    data = list()
    for page in range(1, 51):
        #Open the url link
        full_url = f'{base_url}{page}.html'

        #Store in html_text format
        html_text = requests.get(full_url)

        if (html_text.status_code == 200):
            soup = BeautifulSoup(html_text.text, 'html.parser')

            #Each object
            objects = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

            for object in objects:
                #To get full name, we have to loop through the links for each book and extract the full name
                book_name_link = object.h3.a['href']
                book_html = requests.get(f'https://books.toscrape.com/catalogue/{book_name_link}')
                soup2 = BeautifulSoup(book_html.text, 'html.parser')
                book_section = soup2.find('div', class_ = 'col-sm-6 product_main')
                book_name = book_section.h1.text.strip()

                book_price = object.find('p', class_ = 'price_color').text.strip().split('Â')[1]
                stock_availability = object.find('p', class_ = 'instock availability').text.strip()
                rating = object.find('p', class_ = 'star-rating')['class'][-1].strip()

                print(book_name)
                print(book_price)
                print(stock_availability)
                print(rating)
                data.append([book_name, book_price, rating, stock_availability])

            df = pd.DataFrame(data, columns=['Title', 'Price', 'Rating', 'Stock Availability'])
            df.to_excel('books_data.xlsx', index=False)
        else:
            print("Unsucessful")
            break




if __name__ == '__main__':
    webScrap()

