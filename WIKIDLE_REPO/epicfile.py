import psycopg2

from connection import connection
# pip install psycopg2-binary

cursor = connection.cursor()
cursor.execute("""SELECT * FROM Wikipedia_articles ORDER BY RANDOM() LIMIT 1""")
row = cursor.fetchone()

title, summary, category, picture = row

print("Title:", title)
print("Summary:", summary)
print("Category:", category)
print("Picture:", picture)

cursor.close()
connection.close()