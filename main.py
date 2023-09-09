import pandas as pd
import requests
from bs4 import BeautifulSoup
import random  # To select a random user agent from the list

# Read the CSV file
csv_file_path = 'C:\\Users\\.Com\\Documents\\EndoleTest.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# List of user agents
user_agents = {
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; pl-PL; rv:1.0.1) Gecko/20021111 Chimera/0.6',
    'AmigaVoyager/3.2 (AmigaOS/MC680x0)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Browzar)',

    # Add more user agents as needed
}

# Function to generate the LinkedIn link
def generate_link(row):
    return f"https://recruitmentgeek.com/tools/linkedin#gsc.tab=0&gsc.q={row['B']}AND{row['K']}location%20United%20Kingdom&gsc.sort="

# Function to extract URLs from search results
def extract_urls(link):
    # Randomly select a user agent from the list
    header = {
        'User-Agent': random.choice(user_agents),
    }
    response = requests.get(link, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='gs-bidi-start-align gs-visibleUrl gs-visibleUrl-long')
    urls = [result.get_text() for result in results]
    print(urls)
    return urls[:3]  # Get the first three results

# Iterate through rows and update the CSV file
# for index, row in df.iterrows():
#     link = generate_link(row)
#     urls = extract_urls(link)
#     df.at[index, 'LinkedIn URLs'] = ', '.join(urls)

# Save the updated dataframe to a new CSV file
# output_csv_file_path = 'output_file.csv'  # Replace with the desired output file path
# df.to_csv(output_csv_file_path, index=False)
