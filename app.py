import re
import discogs_client
from bs4 import BeautifulSoup
import requests
from api_key import api_key

# Instantiates client object with personal access token
ds = discogs_client.Client('PriceTracker/0.1', user_token=api_key)

# Eventually from user input
rel_type = 'master'         # 'master' or 'release'
rel_format = 'Vinyl'        # 'Vinyl' or 'CD'
squery = 'kids see ghosts'

# Gets URL based on user input
results = ds.search(squery, type=rel_type)
rel_id = results[0].id
url = 'https://www.discogs.com/sell/list?sort=price%2Casc' \
        f'&{rel_type}_id={rel_id}&format={rel_format}'

source = requests.get(url).text
soup = BeautifulSoup(source, 'lxml')

# Get items listed for sale
items = soup.find_all('tr', class_='shortcut_navigable')

# Remove unavailable items
for item in items:
    match = re.search('shortcut_navigable unavailable', str(item))
    if match:
        items.remove(item)

# Store lowest price
price = items[0].find('td', class_='item_price') \
        .find('span', class_='converted_price').text


# TODO: Remove everything besides regex pattern

pattern = re.compile('.\d*\.?\d{0,2}')
