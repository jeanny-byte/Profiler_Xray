import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Load the CSV file
csv_file = 'your_file.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Set up web drivers for different browsers
driver = webdriver.Chrome()  # Change this to your preferred browser

# Define search engines
search_engines = {
    'Brave Search': 'https://search.brave.com/search?q=',
    'DuckDuckGo': 'https://duckduckgo.com/?q=',
    'Google': 'https://www.google.com/search?q='
}

# Define the columns
company_column = 'Company Name'
telephone_column = 'Telephone'
sic_code_column = 'SIC Code'
contact_name_column = 'Contact Name'

# Function to perform a search and grab the first three profile links
def search_and_get_profiles(search_engine, query):
    driver.get(search_engine + query)
    time.sleep(2)  # Wait for the search results to load

    profile_links = []

    if search_engine == 'Google':
        results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
        for result in results[:3]:
            link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            profile_links.append(link)
    else:
        links = driver.find_elements(By.CSS_SELECTOR, 'a')
        for link in links[:3]:
            href = link.get_attribute('href')
            if href and 'linkedin.com/in/' in href:
                profile_links.append(href)

    return profile_links

# Iterate through each row in the CSV and perform searches
for index, row in df.iterrows():
    company_name = row[company_column]
    telephone = row[telephone_column]
    sic_code = row[sic_code_column]
    contact_name = row[contact_name_column]

    for engine, base_url in search_engines.items():
        query = f'"{company_name}" "{telephone}" "{sic_code}" "{contact_name}" site:linkedin.com'
        profile_links = search_and_get_profiles(base_url, query)

        # Append the profile links to the CSV
        profile_links_str = ', '.join(profile_links)
        df.at[index, f'{engine} Profiles'] = profile_links_str

# Save the updated CSV
df.to_csv('updated_file.csv', index=False)  # Replace with your desired output filename

# Close the web driver
driver.quit()
