import time
import PySimpleGUI as sg
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import openpyxl
import re
#
# # Replace 'YOUR_API_KEY' with your Proxifly API key
# proxifly_api_key = '4xXKD6teyEz7RGfwwwRyTcmrsptbSpRXNYkNvbLb5rkC'
#
# # Proxifly API endpoint for proxy rotation
# proxifly_rotate_url = 'https://api.proxifly.com/v1/rotate'

# Define a list of user agents to rotate through
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/85.0',
    # Add more user agents as needed
]

# Define search engines and their URLs
search_engines = {
    "search.brave.com": "https://search.brave.com/search?q=",
    "www.bing.com": "https://www.bing.com/search?q=",
    "www.duckduckgo.com": "https://www.duckduckgo.com/?q=",
    "www.google.com": "https://www.google.com/search?q=",
}

# Define a function to select a random user agent
def get_random_user_agent():
    return random.choice(user_agents)

# Define a function to rotate Proxifly proxies
def rotate_proxifly_proxy():
    try:
        headers = {
            'user_agents'
        }
        response = requests.post(search_engines, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error rotating Proxifly proxy: {e}")
        return None

# Define a function to search the selected search engine and extract LinkedIn profiles
def search_linkedin_profiles(contact_name, company, selected_search_engine):
    if selected_search_engine not in search_engines:
        print("Invalid search engine selected.")
        return []

    search_url = search_engines[selected_search_engine] + f'"{contact_name}" LinkedIn profile'
    headers = {
        'User-Agent': get_random_user_agent()
    }

    try:
        proxy_info = rotate_proxifly_proxy()
        if not proxy_info:
            return []

        proxies = {
            'http': f'http://{proxy_info["proxy"]}',
            'https': f'http://{proxy_info["proxy"]}',
        }

        time.sleep(random.randint(5, 10))
        response = requests.get(search_url, headers=headers, proxies=proxies)
        time.sleep(3)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'linkedin.com/in/' in href:
                text = link.text
                print(text)
                if re.search(f'{contact_name}|{company}', text, re.I):
                    results.append({"Contact Name": contact_name, "Company": company, "LinkedIn Profile": href})

        return results

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

# Define the PySimpleGUI layout
layout = [
    [sg.Text("Select a .csv or .xlsx file:")],
    [sg.InputText(key="file_path"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")))],
    [sg.Text("Select a search engine:")],
    [sg.Radio("search.brave.com", "search_engine", default=True, key="search.brave.com"),
     sg.Radio("www.bing.com", "search_engine", key="www.bing.com"),
     sg.Radio("www.duckduckgo.com", "search_engine", key="www.duckduckgo.com"),
     sg.Radio("www.google.com", "search_engine", key="www.google.com")],
    [sg.Button("Start Search"), sg.Button("Exit")],
]

window = sg.Window("LinkedIn Search", layout, icon="linkedin-3-256.ico")

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Start Search":
        file_path = values["file_path"]
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            sg.popup_error("Invalid file format. Please select a .csv or .xlsx file.")
            continue

        if "Contact Name" not in df.columns or "Company" not in df.columns:
            sg.popup_error("The file must contain columns named 'Contact Name' and 'Company'.")
            continue

        selected_search_engine = next(key for key, value in values.items() if value and key in search_engines)
        results = []

        for _, row in df.iterrows():
            contact_name = row["Contact Name"]
            company = row["Company"].replace("+", " ")
            search_results = search_linkedin_profiles(contact_name, company, selected_search_engine)
            results.extend(search_results)

        if not results:
            sg.popup("No matching results found.")
        else:
            # Specify the path to your output file here
            output_file_path = "output_results.xlsx"

            # Load the existing file (CSV or XLSX)
            if output_file_path.endswith(".xlsx"):
                existing_df = pd.read_excel(output_file_path, engine="openpyxl")
            else:
                existing_df = pd.read_csv(output_file_path)

            # Concatenate the new results with the existing data
            updated_df = pd.concat([existing_df, pd.DataFrame(results)], ignore_index=True)

            # Save the updated data back to the file
            if output_file_path.endswith(".xlsx"):
                updated_df.to_excel(output_file_path, index=False, engine="openpyxl")
            else:
                updated_df.to_csv(output_file_path, index=False)

            print("Results appended to", output_file_path)

window.close()
