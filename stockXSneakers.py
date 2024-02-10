import requests
from bs4 import BeautifulSoup
import random
import time

# List of User-Agent strings for different browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
]

# List of proxy servers
proxies = [
    'http://50.171.68.130',
    'http://192.99.169.19'
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

for page_num in range(1, 3):
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
