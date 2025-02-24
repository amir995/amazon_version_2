
import time
import re
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
from os.path import exists
import os
# from fake_useragent import UserAgent
import pandas as pd

df = pd.read_excel("Competitors.xlsx")

df.head()
result = pd.DataFrame(columns=['ASIN', 'product name', 'price', 'date', 'time', 'Fetched', "Ranking", "Category", "Star", "Rating_count"])

print(result)


def New_Part(soup,url):
    time.sleep(2.5)
    try:
        table = soup.find("table", {"id": "productDetails_detailBullets_sections1"})
        rows = table.find_all("tr")
        last_row = rows[-1]
        column = last_row.find("td")
        last_row = rows[-1]
        column = last_row.find("td")
    except:
        table = soup.find("table", {"id": "productDetails_detailBullets_sections1"})
        rows = table.find_all("tr")
        last_row = rows[-1]
        column = last_row.find("td")
        last_row = rows[-1]
        column = last_row.find("td")


    text = column.text
    # Use regex to extract rank and category
    matches = re.findall(r"#([\d,]+) in ([\w\s&]+)", text)
    ranking = ""
    category = ""
    # Print extracted data
    try:
        # Print extracted data
        ranking, category = matches[1]


    except:
        for rank, cate in matches:
            ranking = rank
            category = cate

    stars_data = soup.find("span", {"id": "acrPopover"}).text

    star = re.search(r"\d+\.\d+", stars_data).group()  # Find the first decimal number

    rating_count_data = soup.find("span", {"id": "acrCustomerReviewText"}).text
    #rating_count = re.search(r"\d+", rating_count_data).group()  # Find the first number
    rating_count = rating_count_data
    return ranking, category, star,rating_count
def Main_code(url):
    global result
    useragent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 YaBrowser/21.11.3.855 Yowser/2.5 Safari/537.36",
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    useragnt = random.choice(useragent_list)
    # useragnt = UserAgent().random

    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': useragnt,
               'x-requested-with': 'XMLHttpRequest',
               'cache-control': 'no-cache',
               'authority': 'www.amazon.com',
               'accept': 'text/html,*/*',
               'accept-language': 'en-US,en;q=0.9',
               "device-memory": random.choice(["2", "4", "8"]),
               'rtt': '50',
               'sec-ch-dpr': '1',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"Windows"',
               'sec-ch-ua-platform-version': '"8.0.0"',
               'sec-ch-viewport-width': '250',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'viewport-width': '250'
               }
    '''
    {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Requested-With':'XMLHttpRequest',
               'User-Agent': useragnt
               }
    '''

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, headers=requests.session().headers.update(headers))
    soup = BeautifulSoup(response.content, 'html.parser')

    count = 1

    checker = True
    location = ""
    soup1 = ""
    price = ""
    ranking = ""
    category = ""
    star = ""
    rating_count = ""
    while "Sorry! Something went wrong!" in soup.text:
        if "Currently unavailable" not in soup.text:
            session.headers.update(headers)
            response = session.get(url)  # , headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            soup1 = soup

            print(f'Wait... trying count >> {count}')

            count = count + 1
            time.sleep(random.choice([0.5, 0.6, 0.7, 0.9, 1, 1.25, 1.50, 1.75, 2]))

            if count > 15:
                print("Maximun Try 15, is out of limit")
                success = False
                price = ""
                product_name = ""
                date = ""
                time_1 = ""
                ranking = ""
                category = ""
                stars = ""
                rating_count = ""
                url = url.replace("https://www.amazon.com/dp/", "")
                data = pd.DataFrame(
                    {'ASIN': [url], 'product name': [product_name], 'price': [price], 'date': [date], 'time': time_1,
                     'Fetched': success, 'ranking': [ranking], 'category': [category], 'stars':[stars], 'rating count':[rating_count]

                })

                result = pd.concat([result, data], ignore_index=True)

                checker = False
                break

        else:
            print("untracable")
            price = "Currently unavailable"
            product_name = soup1.find('span', id='productTitle').text.strip()

            checker = False

    if checker:
        if "Currently unavailable" not in soup.text:
            try:
                product_name = soup.find('span', id='productTitle').text.strip()


                price1 = soup.find('td', class_='a-span12')
                price = price1.find('span', class_='a-price a-text-price a-size-medium apexPriceToPay').text
                price = price.split("$")
                price = price[1]
                ranking, category, star, rating_count = New_Part(soup,url)

                print(price)
                print(ranking)
                print(category)
                print(star)
                print(rating_count)

                '''
                if "This item cannot be shipped to your selected delivery location" in soup.text:
                    print("This item cannot be shipped to your selected delivery location")
                '''



            except:
                product_name = soup.find('span', id='productTitle').text.strip()
                # print("________________")
                price_1 = soup.find(class_='a-price-whole').text
                price_2 = soup.find(class_='a-price-fraction').text
                price_1 = price_1.replace(".", "")
                price = price_1 + "." + price_2
                ranking, category, star, rating_count = New_Part(soup,url)




        else:
            product_name = soup.find('span', id='productTitle').text.strip()
            price = "Currently Unvailable"
        # _________________
        d = datetime.now()
        date = d.strftime("%d-%m-%Y")
        t = datetime.now().time()
        # Format the time in 24-hour format
        time_1 = t.strftime("%I:%M:%S %p")
        # _________________

        print(product_name)
        print(price)
        print(date)
        print(time_1)
        ranking, category, star, rating_count = New_Part(soup,url)
        print(ranking)
        print(category)
        print(star)
        print(rating_count)

        url = url.replace("https://www.amazon.com/dp/", "")
        success = True
        data = pd.DataFrame(
            {'ASIN': [url], 'product name': [product_name], 'price': [price], 'date': [date], 'time': time_1,
             'Fetched': success, 'ranking': [ranking], 'category': [category], 'stars': [star],
             'rating count': [rating_count]
             })
        result = pd.concat([result, data], ignore_index=True)

a = 1
for index, row in df.iterrows():
    url = row['urls']
    print("_______________")
    print(url)
    print("Count " +str(a))
    a+=1
    if "https://www." not in url:
        url = "https://www." + str(url)
        try:
            Main_code(url)
        except requests.exceptions.ConnectionError as e:
            pass

print(result)
mergedResult = df.merge(result, on="ASIN", how="left")


print(mergedResult.head())
