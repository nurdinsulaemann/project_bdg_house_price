import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import time

headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}


main_url = 'https://www.rumah123.com/jual/bandung/rumah/?page='
list_product_link = []

for page in range(1, 100):
    link_pages = main_url + str(page)
    try:
        r = requests.get(link_pages, headers=headers)
        if r.status_code != 200:
            print(f"Warning: Page {page} returned status code {r.status_code}")
            time.sleep(2)
            continue
        
        soup = BeautifulSoup(r.content, 'lxml')
        product_card = soup.find_all('div', class_='card-featured__middle-section')
        
        for item in product_card:
            
            link = 'https://www.rumah123.com/' + (item.find('a')['href'] if item.find('a') and item.find('a').get('href') else "null")
            nama = item.find('h2').text.strip() if item.find('h2') else "null"
            harga = item.find('div', class_='card-featured__middle-section__price').text.strip() if item.find('div', class_='card-featured__middle-section__price') else "null"
            
            anchor = item.find('a')
            alamat = anchor.find_next('span').text.strip() if anchor and anchor.find_next('span') else "null"
            
            items = item.find_all('div', class_='relative ui-molecules-list__item')
            bedroom = items[0].text.strip() if len(items) > 0 else "null"
            bathroom = items[1].text.strip() if len(items) > 1 else "null"
            garage = items[2].text.strip() if len(items) > 2 else "null"
            
            specs = item.find_all('div', class_='attribute-info')
            LT = specs[0].text.strip() if len(specs) > 0 else "null"
            LB = specs[1].text.strip() if len(specs) > 1 else "null"

            dict_result = {
                'link': link,
                'nama': nama,
                'harga': harga,
                'alamat': alamat,
                'kamar_tidur': bedroom,
                'kamar_mandi': bathroom,
                'garasi/carport': garage,
                'luas_tanah': LT,
                'luas_bangunan': LB
            }

            list_product_link.append(dict_result)
        
        print(f"Page {page} processed. Total items: {len(list_product_link)}")
        time.sleep(2)

    except Exception as e:
        print(f"Error on page {page}: {e}")
    time.sleep(3)

print(f"Total products: {len(list_product_link)}")

df_link_house = pd.DataFrame(list_product_link)
df_link_house.to_csv('bandung_house_price.csv', index=False)
