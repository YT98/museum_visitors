import requests
from bs4 import BeautifulSoup
import json
from unidecode import unidecode
import pandas as pd

class WikiData:
    def __init__(self):
        self.url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&page=list_of_most-visited_museums&section=2&prop=text"
        self.extract ()
        self.transform()
        self.clean()

    def extract(self):
        # Fetch html table from Wikipedia API
        res = requests.request("GET", self.url).text
        res_data = json.loads(res)
        html_table = res_data["parse"]["text"]["*"]

        # Parse html table
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

        self.data = data

    def transform(self):
        cols = ["Museum Name", "Country", "City", "Visitors per year"]
        df = pd.DataFrame(self.data, columns=cols)
        self.df = df

    def clean(self):
        # Escape single quotes
        self.df["City"] = self.df["City"].str.replace("'", "\\'")
        self.df["Museum Name"] = self.df["Museum Name"].str.replace("'", "\\'")
        self.df["Country"] = self.df["Country"].str.replace("'", "\\'")
        # Remove accents
        self.df["City"] = self.df["City"].apply(unidecode)
        self.df["Museum Name"] = self.df["Museum Name"].apply(unidecode)
        self.df["Country"] = self.df["Country"].apply(unidecode)

    def load(self, controller):
        # Load cities
        city_names_ls = self.df["City"].unique()
        for index, name in enumerate(city_names_ls):
            country = self.df.loc[self.df["City"] == name]["Country"].iloc[0]
            controller.insert_city(index, name, country)
        controller.commit()
        
        # Load visitors
        for index, row in self.df.iterrows():
            city = row["City"]
            id = controller.get_city_id(city)
            museum_name = row["Museum Name"]
            visitors = row["Visitors per year"]
            controller.insert_visitors(id, museum_name, visitors)
        controller.commit()
        