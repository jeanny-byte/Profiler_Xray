import PySimpleGUI as sg
import pandas as pd
from openpyxl import load_workbook
import datetime
import requests
from bs4 import BeautifulSoup
import logging
import random

# Define a list of User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    # Add more User-Agent strings here
]

# Define the search engines
search_engines = {
    "DuckDuckGo": "https://duckduckgo.com/html/?q=",
    "Google": "https://www.google.com/search?q=",
    "Bing": "https://www.bing.com/search?q=",
    "RecruitmentGeek": "https://www.recruitmentgeek.com/search?q=",
}

# Configure logging to both file and terminal
logging.basicConfig(filename="linkedin_data_extraction.log", level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

# Define the GUI layout with radio buttons for search engines
layout = [
    [sg.Text("Select a CSV or Excel file:")],
    [sg.Input(key="input_file"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")))],
    [sg.Text("Select a Search Engine:")],
    [sg.Radio("DuckDuckGo", "search_engine", default=True), sg.Radio("Google", "search_engine"), sg.Radio("Bing", "search_engine"), sg.Radio("RecruitmentGeek", "search_engine")],
    [sg.Button("Extract Data")],
]

# Create the GUI window
window = sg.Window("LinkedIn Data Extractor", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Extract Data":
        input_file = values["input_file"]
        selected_search_engine = [key for key, value in values.items() if "DuckDuckGo" in key or "Google" in key or "Bing" in key or "RecruitmentGeek" in key][0]

        if input_file.endswith(".csv"):
            df = pd.read_csv(input_file)
        elif input_file.endswith(".xlsx"):
            df = pd.read_excel(input_file)

        for index, row in df.iterrows():
            company_name = row["Company Name"]
            contact_name = row["Contact"]
            telephone = row["Telephone"]

            # Select a random User-Agent from the list
            user_agent = random.choice(user_agents)
            headers = {'User-Agent': user_agent}

            search_query = f'"{contact_name}" site:linkedin.com/in AND "{company_name}" "United Kingdom" -"Customer Support"'
            search_url = search_engines[selected_search_engine] + search_query

            response = requests.get(search_url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                search_results = soup.find_all('div', class_='result')

                extracted_results = []
                for result in search_results[:3]:  # Only extract the first three results
                    title = result.find('a', class_='result__a').text
                    url = result.find('a', class_='result__url')['href']
                    extracted_results.append(f"{title} - {url}")

                # Append the extracted results to the current row
                df.at[index, "LinkedIn Results"] = ', '.join(extracted_results)

                logging.info(f"Data extracted for row {index}: {company_name}, {contact_name}, {telephone}")

        # Save the updated DataFrame to a new file
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_file_name = f"output_{current_datetime}.xlsx"
        df.to_excel(new_file_name, index=False, engine='openpyxl')

        logging.info(f"Data saved to {new_file_name}")

        # Ask the user where to save the new file
        save_location = sg.popup_get_file("Save the new file as:", save_as=True, file_types=(("Excel Files", "*.xlsx"),))

        if save_location:
            # Copy styles from the input file to the new file (if it's an Excel file)
            if input_file.endswith(".xlsx"):
                input_wb = load_workbook(input_file)
                output_wb = load_workbook(new_file_name)
                for sheet_name in input_wb.sheetnames:
                    input_sheet = input_wb[sheet_name]
                    output_sheet = output_wb[sheet_name]
                    for row in input_sheet.iter_rows(min_row=2, min_col=1, max_col=len(df.columns) + 1):
                        for cell in row:
                            output_cell = output_sheet.cell(row=cell.row, column=cell.column, value=cell.value)
                            output_cell._style = cell._style
                output_wb.save(new_file_name)

                logging.info("Styles copied from input file to the new file.")

            sg.popup(f"Data extracted and saved to:\n{new_file_name}")

window.close()
