import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Define the paths to your CSV file and web driver
csv_file_path = 'your_file.csv'  # Replace with your CSV file path
web_driver_path = 'path_to_web_driver'  # Replace with your web driver path

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Initialize the web driver
driver = webdriver.Chrome(executable_path=web_driver_path)

# Function to search and get profile links from a search engine
def search_and_get_links(query):
    links = []

    # Search on Brave Search
    driver.get('https://search.brave.com/')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the results to load
    results = driver.find_elements(By.CSS_SELECTOR, '.result a')
    for result in results[:3]:
        links.append(result.get_attribute('href'))

    # Search on DuckDuckGo
    driver.get('https://duckduckgo.com/')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the results to load
    results = driver.find_elements(By.CSS_SELECTOR, '.result__url a')
    for result in results[:3]:
        links.append(result.get_attribute('href'))

    # Search on Google
    driver.get('https://www.google.com/')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the results to load
    results = driver.find_elements(By.CSS_SELECTOR, 'a')
    for result in results:
        href = result.get_attribute('href')
        if href and href.startswith('https://www.linkedin.com/in/'):
            links.append(href)

    return links

# Iterate through the CSV rows
for index, row in df.iterrows():
    company_name = row['Company Name']
    telephone = row['Telephone']
    sic_code = row['SIC Code']
    contact_name = row['Contact Name']

    # Construct the search query
    query = f'"{company_name}" "{telephone}" "{sic_code}" "{contact_name}" LinkedIn'

    # Search and get profile links
    profile_links = search_and_get_links(query)

    # Append the profile links to the CSV
    df.at[index, 'LinkedIn Profiles'] = ', '.join(profile_links)

# Save the updated CSV
df.to_csv(csv_file_path, index=False)

# Close the web driver
driver.quit()
