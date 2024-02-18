import re
import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/58.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
]

def free_proxies():
    url = "https://free-proxy-list.net"
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    proxies = []

    proxy_rows = soup.find_all('tr')

    # iterate over each <tr> element
    for row in proxy_rows:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip() # extract IP address
            if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip): # use regex to validate the format of the IP address
                proxies.append(ip)
        except IndexError:
            continue

    return proxies
proxies = free_proxies()
print(proxies)

# base_url = 'https://stockx.com/sneakers?page={}'
# headers = {'User-Agent': random.choice(user_agents)}

# # Function to fetch page content with retries and delays
# def fetch_page(url):
#     for _ in range(3):  # Retry up to 3 times
#         try:
#             response = requests.get(url, headers=headers, proxies={'http': random.choice(proxies)})
#             if response.status_code == 200:
#                 return response.content
#             elif response.status_code == 429:
#                 print("Rate limited. Waiting before retrying...")
#                 time.sleep(60)  # Wait for 1 minute before retrying
#         except Exception as e:
#             print("Error:", e)
#         time.sleep(random.uniform(1, 3))  # Add random delay between retries

#     return None

# # Scraping logic
# product_links = []
# page_num = 1

# while len(product_links) < 20:  # Loop until 20 links are collected
#     url = base_url.format(page_num)
#     content = fetch_page(url)
    
#     if content:
#         soup = BeautifulSoup(content, 'html.parser')
#         divs = soup.find_all('div', class_='css-jurd7a')

#         for div in divs:
#             a_tag = div.find('a', {'data-testid': 'productTile-ProductSwitcherLink'})
#             if a_tag:
#                 link = a_tag.get('href')
#                 product_link = 'https://stockx.com' + link
#                 product_links.append(product_link)
                
#                 if len(product_links) >= 20:  # Stop searching after 20 links
#                     break
        
#     else:
#         print("Failed to retrieve the webpage.")
#         break  # Break out of the loop if the webpage cannot be fetched

#     page_num += 1  # Move to the next page

# product_links = product_links[:20]  # Ensure only 20 links are kept

# print("List of Links:")
# for link in product_links:
#     print(link)

# sneakers_data = []

# for product_link in product_links:
#     r = requests.get(product_link, headers=headers)
    
#     if r.status_code == 200:
#         soup = BeautifulSoup(r.content, 'html.parser')
        
#         product_title_element = soup.find('h1', class_='css-gajrnm')
#         product_title = product_title_element.text.strip() if product_title_element else "Product title not found."
        
#         retail_price_element = soup.find('div', class_='css-np08c9')
#         retail_price = retail_price_element.text.strip() if retail_price_element else "Retail price not found."
        
#         sneakers_data.append({
#             'product_title': product_title,
#             'retail_price': retail_price,
#             # 'Last sold at' : last_sold,
#             'product_link': product_link
#         })
#     else:
#         print(f"Failed to fetch {product_link}")
#         if not sneakers_data:  # If no data is collected yet, break out of the loop
#             break
#     time.sleep(5)



# df = pd.DataFrame(sneakers_data)

# # Display the DataFrame
# print(df)

# df.to_csv('sneakDf.csv', index=False)
