import mysql.connector

# Returns db cursor and initializes database
def db_connect():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
    cursor = conn.cursor()
    ###  Create database and tables
    cursor.execute("CREATE DATABASE IF NOT EXISTS museum_visitors_db")
    cursor.execute("USE museum_visitors_db")
    cursor.execute("CREATE TABLE IF NOT EXISTS cities (id INT, name VARCHAR(100), country VARCHAR(100))")
    cursor.execute("CREATE TABLE IF NOT EXISTS population (city_id INT, population INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS visitors (city_id INT, museum_name VARCHAR(100), visitors INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS avg_visitors (city_id INT, avg_visitors INT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS city_aliases (id INT, alias VARCHAR(100))")

    return cursor

