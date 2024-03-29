import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver

# List of User-Agent strings for different browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
]

# List of proxy servers
proxies = [
    'http://50.175.212.66',
    'http://96.113.159.162'
]

base_url = 'https://stockx.com/sneakers?page={}'
headers = {'User-Agent': random.choice(user_agents)}

# Function to fetch page content with retries and delays
def fetch_page(url):
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, proxies={'http': random.choice(proxies)})
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print("Error:", e)
        time.sleep(random.uniform(1, 3))  # Add random delay between retries

    return None

# Scraping logic
product_links = []

for page_num in range(1, 2):
    url = base_url.format(page_num)
    content = fetch_page(url)
    
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        divs = soup.find_all('div', class_='css-jurd7a')

        for div in divs:
            a_tag = div.find('a', {'data-testid': 'productTile-ProductSwitcherLink'})
            if a_tag:
                link = a_tag.get('href')
                product_links.append('https://stockx.com' + link)
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
    time.sleep(5)

def scrape_last_sale_price(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5) 
    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    last_sold_element = soup.find('p', class_='chakra-text css-1q8ctst')
    last_sold = last_sold_element.text.strip() if last_sold_element else "Last sale price not found"
    return last_sold

for sneaker in sneakers_data:
    last_sale_price = scrape_last_sale_price(sneaker['product_link'])
    sneaker['last_sale_price'] = last_sale_price

print(sneakers_data)

