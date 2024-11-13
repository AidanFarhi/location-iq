import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep, time

# Load ZIP codes from CSV
df = pd.read_csv(
    'data/RDC_Inventory_Core_Metrics_Zip_History.csv',
    dtype={'postal_code': 'str'},
    usecols=['postal_code']
)
zip_codes = list(filter(lambda x: x is not None, df.postal_code.unique()))

# User-agent list to simulate different browsers
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
]

base_url = 'https://crimegrade.org/safest-places-in-'

# Retry parameters
RETRY_LIMIT = 3
TIMEOUT = 10

start_time = time()

for zip_code in zip_codes:
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    url = f'{base_url}{zip_code}'

    attempt = 0
    while attempt < RETRY_LIMIT:
        try:
            # Request with timeout and retry logic
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            table_element = soup.find(class_='gradeComponents')

            if table_element:
                file_name = f'data/raw_crime_data/{zip_code}.html'
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(str(table_element))
                print(f'Saved table for ZIP code {zip_code} to {file_name}')
            else:
                print(f'No table found for ZIP code {zip_code}')
            
            # If successful, break out of retry loop
            break

        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f'Attempt {attempt} failed for ZIP code {zip_code}: {e}')
            if attempt < RETRY_LIMIT:
                sleep_time = random.choice([3, 5, 7])  # Backoff before retrying
                print(f'Retrying in {sleep_time} seconds...')
                sleep(sleep_time)
            else:
                print(f'Failed to retrieve data for ZIP code {zip_code} after {RETRY_LIMIT} attempts.')
    
    # Sleep between requests to avoid overwhelming the server
    sleep(random.choice([7, 8, 9]))

end_time = time()
print(f'Elapsed time: {(end_time - start_time) / 60} minutes')