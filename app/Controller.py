import mysql.connector 

from .WikiData import WikiData
from .LondonData import LondonData

class Controller:
    def __init__(self):
        self.init_conn()
        self.init_db() 

    def init_conn(self):
        self.conn = mysql.connector.connect(
                host="db",
                user="root",
                password="password"
            )

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS museum_visitors_db")
        cursor.execute("USE museum_visitors_db")
        cursor.execute("CREATE TABLE IF NOT EXISTS cities (id INT, name VARCHAR(100), country VARCHAR(100))")
        cursor.execute("CREATE TABLE IF NOT EXISTS population (city_id INT, population INT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS visitors (city_id INT, museum_name VARCHAR(100), visitors INT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS avg_visitors (city_id INT, avg_visitors INT)")
        cursor.close()

    def commit(self):
        self.conn.commit()

    def truncate_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = []
        for (table,) in cursor:
            tables.append(table)
        for table in tables:
            cursor.execute("TRUNCATE TABLE %s" % (table))
        cursor.close()

    def populate(self):
        self.truncate_tables()
        wiki = WikiData()
        london = LondonData()
        wiki.load(self)
        london.load(self)

    def get_data_page_data(self):
        cursor = self.conn.cursor()

        pop_cols = ["City", "Country", "Population"]
        cursor.execute("SELECT name, country, population FROM population INNER JOIN cities ON population.city_id = cities.id")
        pop = cursor.fetchall()

        vis_cols = ["Museum Name", "City", "Country", "Visitors (/year)"]
        cursor.execute("SELECT museum_name, name, country, visitors FROM visitors INNER JOIN cities ON visitors.city_id = cities.id")
        vis = cursor.fetchall()

        avg_vis_cols = ["City", "Country", "Average Visitors (/year)"]
        cursor.execute("SELECT name, country, avg_visitors FROM avg_visitors INNER JOIN cities ON avg_visitors.city_id = cities.id")
        avg_vis = cursor.fetchall()

        cursor.close()

        data_obj = {
            "pop": {
                "cols": pop_cols,
                "data": pop
            },
            "vis": {
                "cols": vis_cols,
                "data": vis
            },
            "avg_vis": {
                "cols": avg_vis_cols,
                "data": avg_vis
            }
        }
        return data_obj


    ### CITIES METHODS
    def insert_city(self, id, name, country):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO cities VALUES (%s, '%s', '%s')" % (id, name, country))
        cursor.close()
    
    def get_cities(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cities")
        cities = cursor.fetchall()
        cursor.close()
        return cities

    def get_city_id(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM cities WHERE name = '%s'" % (name))
        id = cursor.fetchone()[0]
        return id
        cursor.close()


    ### POPULATION METHODS
    def insert_population(self, city_id, population):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO population VALUES ('%s', '%s')" % (city_id, population))
        cursor.close()


    ## VISITORS METHODS
    def insert_visitors(self, city_id, museum_name, visitors):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO visitors VALUES (%s, '%s', %s)" % (city_id, museum_name, visitors))
        cursor.close()

    def get_city_visitors(self, city_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT visitors FROM visitors WHERE city_id = %s" % (city_id))
        vis_ls = []
        for (vis,) in cursor:
            vis_ls.append(vis)
        cursor.close()
        return vis_ls

    def insert_avg_visitors(self, city_id, avg_visitors):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO avg_visitors VALUES (%s, %s)" % (city_id, avg_visitors))
        cursor.close()

    def get_training_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT population, avg_visitors FROM population INNER JOIN avg_visitors ON population.city_id = avg_visitors.city_id")
        training_data = cursor.fetchall()
        cursor.close()
        return training_data