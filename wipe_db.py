import psycopg2

conn = psycopg2.connect(
    dbname="campusguard_db", 
    user="postgres", 
    password="micheal", 
    host="localhost"
)
conn.autocommit = True
cur = conn.cursor()
try:
    cur.execute("DROP SCHEMA public CASCADE;")
    cur.execute("CREATE SCHEMA public;")
    cur.execute("GRANT ALL ON SCHEMA public TO postgres;")
    cur.execute("GRANT ALL ON SCHEMA public TO public;")
    print("Database wiped successfully.")
except Exception as e:
    print(f"Error: {e}")
finally:
    cur.close()
    conn.close()
