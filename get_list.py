import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from tqdm import tqdm

domain = "https://www.isca-speech.org/archive/"

for year in range(2020, 2024):

    res = requests.get(f"https://www.isca-speech.org/archive/interspeech_{year}/index.html")

    sub_domain = f"https://www.isca-speech.org/archive/interspeech_{year}/"

    soup = BeautifulSoup(res.text, 'html.parser')

    books = soup.find_all('a', {'class': 'w3-text'})
    print(len(books))

    book_list = []
    for book in tqdm(books):
        if book.get('href')[0] != '#':
            link = urljoin(sub_domain, book.get('href'))

            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'html.parser')

            try:
                title = soup.find('h3').text.strip()
                pdf_link = urljoin(domain, soup.find('h3').find_next_sibling('a').get('href'))
                book_list.append({
                    'title': title,
                    'pdf_link': pdf_link
                })

            except Exception as e:
                continue
    
    book_list = list(set(book_list))
    with open(f"{year}.json", "w", encoding= "utf-8") as f:
        json.dump(book_list, f, indent= 4)
        