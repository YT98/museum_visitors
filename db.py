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
        cursor.execute("CREATE TABLE IF NOT EXISTS city_aliases (id INT, alias VARCHAR(100))")

    def get_cursor(self):
        return self.conn.cursor()
    
    def commit(self):
        self.conn.commit()

    def insert_city(self, id, name, country):
        self.get_cursor().execute("INSERT INTO cities VALUES (%s, '%s', '%s')" % (id, name, country))

    def truncate_tables(self):
        cursor = self.conn.cursor(buffered=True)
        cursor.execute("SHOW TABLES")
        for (table,) in cursor:
            cursor.execute("DROP TABLE %s" % (table))
    
        
