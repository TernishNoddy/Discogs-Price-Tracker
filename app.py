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


# TODO: Skip entry if it contains class_='unavailable'

entries = soup.find_all('tr', class_='shortcut_navigable')

for entry in entries:
    if entry.attrs is not {'class': 'unavailable'}:
        lowest = entry
        break
    else:
        continue

print(lowest)
