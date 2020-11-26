import requests
from bs4 import BeautifulSoup
import json
import os
import xlrd
import csv

# Fetches and parses data from wikipedia api
def fetch_museum_data():
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

## Source: https://stackoverflow.com/questions/20105118/convert-xlsx-to-csv-correctly-using-python
def csv_from_excel(in_path, sheet_name, out_path):
    wb = xlrd.open_workbook(in_path)
    sh = wb.sheet_by_name(sheet_name)
    csv_file = open(out_path, 'w')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    csv_file.close()

# Fetches london population dataset and saves to csv file
def download_london_dataset():
    xls_path = os.path.join(os.path.dirname(__file__), "datasets/global-city-population-estimates.xls") 
    csv_path = os.path.join(os.path.dirname(__file__), "datasets/global-city-population-estimates.csv")

    # Get .xls file
    url = "https://data.london.gov.uk/download/global-city-population-estimates/604a6a6f-2162-4d6b-bcd0-bee051703de1/global-city-population-estimates.xls"
    res = requests.request("GET", url)    
    open(xls_path, 'wb').write(res.content)

    # Convert to .csv
    csv_from_excel(xls_path, 'CITIES-OVER-300K', csv_path)
    os.remove(xls_path) # Removes original .xls file