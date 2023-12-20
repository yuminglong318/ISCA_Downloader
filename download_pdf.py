import requests
import json
import os
import re
from tqdm import tqdm

def download_pdf(title, url, dir):

    title = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = os.path.join(dir, title)

    response = requests.get(url, stream=True)

    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

if __name__ == '__main__':


    for year in (2020,2024):
        print(year)

        if not os.path.exists(year):
            os.mkdir(year)
        
        with open(f"{year}.json", "r", encoding= "utf-8") as f:
            pdfs = json.load(f)
        
        for pdf in tqdm(pdfs):
            try:
                download_pdf(pdf['title'], pdf['url_link'], year)
            except Exception as e:
                pass