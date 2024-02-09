import requests
from bs4 import BeautifulSoup

baseurl = 'https://stockx.com/sneakers'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(baseurl, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

grid_container = soup.find('div', id='browse-grid')  # Assuming the grid container has an id 'browse-grid'

print(grid_container)  # Print the grid container to see its content

# If the grid container is found, proceed with the rest of the code
if grid_container:
    # Find all individual items within the grid
    items = grid_container.find_all('a', {'data-testid': 'productTile-ProductSwitcherLink'})

    # Extract links from each item
    item_links = [item['href'] for item in items]

    # Print the links
    print(item_links)
else:
    print("Grid container not found.")
