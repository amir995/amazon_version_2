import time
import re
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
import pandas as pd

df = pd.read_excel("Competitors.xlsx")

result = pd.DataFrame(columns=['ASIN', 'product name', 'price', 'date', 'time', 'Fetched', "Ranking", "Category", "Star", "Rating_count"])


def New_Part(soup):
    page_source = soup.text
    match = re.search(r"Best Sellers Rank\s+.*", page_source)

    ranking, category, star, rating_count = "None", "None", "None", "None"

    # Extract star rating
    stars_data = soup.find("span", {"id": "acrPopover"})
    if stars_data:
        star_match = re.search(r"\d+\.\d+", stars_data.text)
        if star_match:
            star = star_match.group()

    # Extract rating count
    rating_count_data = soup.find("span", {"id": "acrCustomerReviewText"})
    if rating_count_data:
        rating_count = rating_count_data.text.replace("ratings", "").replace("rating", "").strip()

    # Extract ranking & category
    if match:
        text = match.group()
        matches = re.findall(r"#\d+[^#]+?(?=  )", text)
        if matches and len(matches) > 1:
            rank_data_ls = str(matches[1]).strip().split("in")
            if len(rank_data_ls) > 1:
                ranking = rank_data_ls[0].strip()
                category = rank_data_ls[1].strip()

    return ranking, category, star, rating_count


def Main_code(url):
    global result

    useragent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    ]
    useragnt = random.choice(useragent_list)

    headers = {
        'User-Agent': useragnt,
        'Accept-Language': 'en-US,en;q=0.9',
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an error if response is not 200
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Handle unavailable products
    if "Currently unavailable" in soup.text:
        price = "Currently Unavailable"
        product_name = soup.find('span', id='productTitle')
        product_name = product_name.text.strip() if product_name else "Unknown Product"
    else:
        # Extract product name
        product_name = soup.find('span', id='productTitle')
        product_name = product_name.text.strip() if product_name else "Unknown Product"

        # Extract price
        price = "Not Found"
        price_whole = soup.find(class_='a-price-whole')
        price_fraction = soup.find(class_='a-price-fraction')

        if price_whole and price_fraction:
            price = f"{price_whole.text.strip()}{price_fraction.text.strip()}"

    # Extract ranking, category, star rating, and review count
    ranking, category, star, rating_count = New_Part(soup)

    # Get current date and time
    d = datetime.now()
    date = d.strftime("%d-%m-%Y")
    time_1 = d.strftime("%I:%M:%S %p")

    print(f"Product: {product_name}\nPrice: {price}\nDate: {date}\nTime: {time_1}\nRanking: {ranking}\nCategory: {category}\nStar: {star}\nRatings: {rating_count}")

    asin = url.replace("https://www.amazon.com/dp/", "")
    data = pd.DataFrame(
        {'ASIN': [asin], 'product name': [product_name], 'price': [price], 'date': [date], 'time': time_1,
         'Fetched': True, 'Ranking': [ranking], 'Category': [category], 'Star': [star], 'Rating_count': [rating_count]})
    result = pd.concat([result, data], ignore_index=True)


# Loop through URLs
for index, row in df.iterrows():
    url = row['urls']
    print(f"Fetching {url}...")
    if "https://www." not in url:
        url = "https://www." + url
    Main_code(url)

print(result)
mergedResult = df.merge(result, on="ASIN", how="left")
print(mergedResult.head())
