import requests
from bs4 import BeautifulSoup
import random
import pandas as pd

# List of User-Agent strings for different browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
]

proxies = [
    'http://50.175.212.66',
    'http://96.113.159.162'
]

base_url = 'https://stockx.com/sneakers?page=1'
headers = {'User-Agent': random.choice(user_agents)}

# Function to fetch page content
def fetch_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print("Error:", e)
    return None

# Scraping logic
product_links = []

content = fetch_page(base_url)
if content:
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all('div', class_='css-jurd7a')

    for div in divs:
        a_tag = div.find('a', {'data-testid': 'productTile-ProductSwitcherLink'})
        if a_tag:
            link = a_tag.get('href')
            product_links.append('https://stockx.com' + link)
            if len(product_links) >= 64:  # Stop when 64 items are reached
                break
    print("List of Links:")
    for link in product_links:
        print(link)
else:
    print("Failed to retrieve the webpage.")

sneakers_data = []

for product_link in product_links:
    r = requests.get(product_link, headers=headers)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        
        product_title_element = soup.find('h1', class_='chakra-heading css-1qzfqqa', attrs={'data-component': 'primary-product-title'})
        product_title = product_title_element.text.strip() if product_title_element else "Product title not found."
        
        retail_price_elements = soup.find_all('p', class_='chakra-text css-pxl067')[2]
        retail_prices = [elem.text.strip() for elem in retail_price_elements]
        
        if retail_prices:
            for retail_price in retail_prices:
                sneakers_data.append({
                    'product_title': product_title,
                    'retail_price': retail_price,
                    'product_link': product_link
                })
        else:
            sneakers_data.append({
                'product_title': product_title,
                'retail_price': "Retail price not found.",
                'product_link': product_link
            })
    else:
        print(f"Failed to fetch {product_link}")

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(sneakers_data)

# Display the DataFrame
print(df)
