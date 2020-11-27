import pandas as pd
import numpy as np
from Db import Db
import fetch_data as fetch_data


def populate_db(db):
    ### Reset tables
    db.truncate_tables()
    
    ### Load dataframes and create alias dict
    vis_df = fetch_data.get_visitor_df()
    london_df = fetch_data.get_population_df()
    aliases = {
        "New York City": "New York",
        "South Korea": "Republic of Korea",
        "Suzhou": "Suzhou, Jiangsu",
        "Taiwan": "China",
        "Vatican City": "Vatican"
    
    ### Populate cities table
    city_names_ls = vis_df.City.unique()
    for index, name in enumerate(city_names_ls):
        country = vis_df.loc[vis_df["City"] == name]["Country"].iloc[0]
        db.insert_city(index, name, country)

    ### Populate population table
    cities = db.get_cities()
    for row in cities:
        id, city, country = row
        city = aliases[city] if city in aliases else city
        country = aliases[country] if country in aliases else country
        city_row = london_df[
            (london_df["City"].str.contains(city)) & 
            (london_df["Country"].str.contains(country))
        ]
        if not city_row.empty:
            pop = city_row.Population.item()
            pop = int(pop) * 1000
            db.insert_population(id, pop)
    # Manually add Vatican and Oswiecim
    vatican_id = db.get_city_id("Vatican City")
    db.insert_population(vatican_id, 825)
    oswiecim_id = db.get_city_id("Oswiecim")
    db.insert_population(oswiecim_id, 41143)

    ### Populate visitors table
    for index, row in vis_df.iterrows():
        city = row["City"]
        id = db.get_city_id(city)
        museum_name = row["Museum Name"]
        visitors = row["Visitors per year"]
        db.insert_visitors(id, museum_name, visitors)

    ### Populate avg_visitors table
    for row in cities:
        id, city, country = row
        visitors = db.get_city_visitors(id)
        avg = int(np.mean(visitors))
        db.insert_avg_visitors(id, avg)

    ### Commit
    db.commit()

