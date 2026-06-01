import psycopg2

connection = psycopg2.connect(
    host="localhost",
    user="julianbirch",
    password="Damn", 
    dbname="wikipedia_articles",
    port= 5432
)

cursor = connection.cursor()
print("hell yeah")