import requests
from bs4 import BeautifulSoup
import re


def search_linkedin_profiles(name, country, company):
    query = f'site:linkedin.com "{name}" {country} {company}'
    google_search_url = f'https://www.google.com/search?q={query}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',    }

    try:
        # Send a GET request to Google Search
        response = requests.get(google_search_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract search results URLs using regex
            search_results = soup.find_all('a')

            linkedIn_urls = re.search(r'https://www.linkedin.com/in/([a-zA-Z0-9-]+)'
            print(linkedIn_urls)
            linkedin_profiles = [a['href'] for a in search_results if
                                re.search(r"https://www.linkedin.com/in/([a-zA-Z0-9-]+)", str(a))]

            for profile_url in linkedin_profiles:
                # TODO: Jean, do the lookup here

                # Regular expression pattern to match LinkedIn profile links
                match = r"https://www.linkedin.com/in/([a-zA-Z0-9-]+)"

                # Loop through each search result
                for result in soup.find_all("a", href=True):
                    link = result["href"]

                    # Check if the result is a LinkedIn profile link
                    match = re.match(match, link)
                    if match:
                        # Extract the LinkedIn profile username
                        username = match.group(1)

                        # Check if the LinkedIn profile contains data from columns B and K
                        if any(re.search(re.escape(company), username, re.I) and re.search(re.escape(contact),
                                                                                                username, re.I) for
                               company_name, contact in zip(company)):
                            search_results.append(link)

                return search_results

        else:
            print(f"Failed to retrieve search results. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    name = "Gavin Whitehead"
    country = "United Kingdom"
    company = "William Freer Limited"

    search_linkedin_profiles(name, country, company)
