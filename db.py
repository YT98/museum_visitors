import mysql.connector 

class Db:
    def __init__(self):
        self.init_db() 

    def init_db(self):
        self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password"
            )
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
        cursor.close()
        return id

    def insert_population(self, city_id, population):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO population VALUES ('%s', '%s')" % (city_id, population))
        cursor.close()

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

    def truncate_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = []
        for (table,) in cursor:
            tables.append(table)
        for table in tables:
            cursor.execute("TRUNCATE TABLE %s" % (table))
        cursor.close()
    
        
