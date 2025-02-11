import streamlit as st
import psycopg2

# PostgreSQL connection details
host = "postgres-db"  # Use the name of the PostgreSQL container
dbname = "mydb"
user = "myuser"
password = "mypassword"

# Connect to PostgreSQL
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
cur = conn.cursor()

# Query the database
cur.execute("SELECT * FROM employees;")
rows = cur.fetchall()

# Display data in Streamlit
st.write("Employee Data:")
for row in rows:
    st.write(row)

# Close the connection
cur.close()
conn.close()
