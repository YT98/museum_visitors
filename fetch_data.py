import requests
from bs4 import BeautifulSoup
import json
import os
import xlrd
import csv
import pandas as pd
import numpy as np

LONDON_DS_PATH = os.path.join(os.path.dirname(__file__), "datasets/global-city-population-estimates.xls")

# Fetches and parses data from wikipedia api
def fetch_visitor_data():
    # Fetch html table from wikipedia api
    url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page=list_of_most-visited_museums&section=2&prop=text"
    wiki_data_text = requests.request("GET", url).text
    wiki_data_json = json.loads(wiki_data_text)
    html_table = wiki_data_json["parse"]["text"]["*"]

    # Parse html_table
    soup = BeautifulSoup(html_table, 'html.parser')
    tbody = soup.table.tbody
    ls_rows = tbody.find_all(["tr"])

    # Extract data from rows
    data = []
    for tr in ls_rows[1:]:
        cells = tr.find_all(["td"])

        # [0]: Name
        # Ex: <td><a href="/wiki/Louvre" title="Louvre"> Louvre </a></td>
        museum_name = cells[0].a.text
        # [1]: Country flag, city
        # Ex: <td> <span><a href="/wiki/France"><img/></a></span> <a href="/wiki/Paris" title="Paris"> Paris</a> </td>
        a_tags = cells[1].find_all(["a"])
        country = a_tags[0].attrs["href"][6:]
        country = country.replace("_", " ")
        city = a_tags[1].contents[0]
        # [2]: Visitors per year
        # Ex: <td>9,600,000</td>
        visitors = cells[2].text
        visitors = visitors.replace(",", "")
        visitors = int(visitors)

        row = [museum_name, country, city, visitors]
        data.append(row)

    return data

def get_visitor_df():
    vis_data = fetch_visitor_data()
    vis_cols = ["Museum Name", "Country", "City", "Visitors per year"]
    vis_df = pd.DataFrame(vis_data, columns=vis_cols)
    return vis_df 

# Fetches london population dataset
def download_london_dataset():
    url = "https://data.london.gov.uk/download/global-city-population-estimates/604a6a6f-2162-4d6b-bcd0-bee051703de1/global-city-population-estimates.xls"
    res = requests.request("GET", url)    
    open(LONDON_DS_PATH, 'wb').write(res.content)

def get_population_df():
    if not os.path.exists(LONDON_DS_PATH):
        download_london_dataset()

    pop_df = pd.read_excel(
        r"datasets/global-city-population-estimates.xls", 
        "CITIES-OVER-300K",
        dtype={"2020": np.int64}
        )
    pop_df = pop_df[["Country or area", "Urban Agglomeration", "2020"]]
    pop_df.rename(columns={
        "Country or area": "Country",
        "Urban Agglomeration": "City",
        "2020": "Population",
    }, inplace=True)

    return pop_df