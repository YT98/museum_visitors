import requests
import os
import pandas as pd
import numpy as np
import xlrd
import os
from unidecode import unidecode

class LondonData:
    def __init__(self):
        self.url = "https://data.london.gov.uk/download/global-city-population-estimates/604a6a6f-2162-4d6b-bcd0-bee051703de1/global-city-population-estimates.xls"
        self.path = "/tmp/global-city-population-estimates.xls"
        self.aliases = {
            "New York City": "New York",
            "South Korea": "Republic of Korea",
            "Suzhou": "Suzhou, Jiangsu",
            "Taiwan": "China"
        }
        self.extract ()
        self.transform()
        self.clean()

    def extract(self):
        # Fetch and download .xls dataset
        res = requests.request("GET", self.url)    
        open(self.path, 'wb').write(res.content)

    def transform(self):
        df = pd.read_excel(
            self.path, 
            "CITIES-OVER-300K",
            dtype={"2020": np.int64}
        )
        df = df[["Country or area", "Urban Agglomeration", "2020"]]
        df.rename(columns={
            "Country or area": "Country",
            "Urban Agglomeration": "City",
            "2020": "Population",
        }, inplace=True)
        self.df = df

    def clean(self):
        # Escape single quotes
        self.df["City"] = self.df["City"].str.replace("'", "\\'")
        self.df["Country"] = self.df["Country"].str.replace("'", "\\'")
        # Remove accents
        self.df["City"] = self.df["City"].apply(unidecode)
        self.df["Country"] = self.df["Country"].apply(unidecode)

    def load(self, controller):
        cities = controller.get_cities()

        # Load population
        for row in cities:
            id, city, country = row
            city = self.aliases[city] if city in self.aliases else city
            country = self.aliases[country] if country in self.aliases else country
            city_row = self.df[
                (self.df["City"].str.contains(city)) & 
                (self.df["Country"].str.contains(country))
            ]
            if not city_row.empty:
                pop = city_row.Population.item()
                pop = int(pop) * 1000
                controller.insert_population(id, pop)
        vatican_id = controller.get_city_id("Vatican City")
        controller.insert_population(vatican_id, 825)
        oswiecim_id = controller.get_city_id("Oswiecim")
        controller.insert_population(oswiecim_id, 41143)
        controller.commit() 

        # Load avg_population
        for row in cities:
            id, city, country = row
            visitors = controller.get_city_visitors(id)
            avg = int(np.mean(visitors))
            controller.insert_avg_visitors(id, avg)
        controller.commit() 