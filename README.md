# 🚀 Full Stack App Using Docker

This guide will help you set up a **Full Stack Application** using Docker, featuring a **PostgreSQL database** and a **Streamlit web app**. The two containers will communicate using a **Docker network** for seamless integration.

## 📄 Documentation
- [Docker](https://docs.docker.com/)
- [MySQL](https://hub.docker.com/_/mysql)
- [Docker Network](https://docs.docker.com/engine/network/)

---

## 🛠️ Deployment Steps

### 1️⃣ Create a Docker Network
To enable communication between containers, create a custom network:
```bash
docker network create my_network
```

### 2️⃣ Set Up the Database Container
Run a **PostgreSQL** container connected to `my_network`:
```bash
docker run -d \
  --name my_postgres \
  --network my_network \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=adminpassword \
  -e POSTGRES_DB=mydb \
  postgres
```
This starts a PostgreSQL container named `my_postgres` inside `my_network`.

### 3️⃣ Create a Dockerfile for the Streamlit App
Inside your **Streamlit project folder**, create a `Dockerfile`:
```dockerfile
# Use Python as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "stream.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Ensure `requirements.txt` includes the necessary dependencies:
```bash
streamlit
psycopg2
```

### 4️⃣ Build and Run the Streamlit Container
Build the **Streamlit Docker image**:
```bash
docker build -t my_streamlit_app .
```
Run the container and connect it to `my_network`:
```bash
docker run -d \
  --name streamlit_app \
  --network my_network \
  -p 8501:8501 \
  my_streamlit_app
```

### 5️⃣ Connect Streamlit to PostgreSQL
Create a `stream.py` file in your project folder:
```python
import streamlit as st
import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname="mydb",
    user="admin",
    password="adminpassword",
    host="my_postgres",  # Container name as hostname
    port="5432"
)
cur = conn.cursor()

# Example query
cur.execute("SELECT version();")
db_version = cur.fetchone()

st.title("Streamlit App with PostgreSQL")
st.write("Connected to database:", db_version)

cur.close()
conn.close()
```

### 6️⃣ Test Your Setup 🎯
After deployment, open your browser and visit:
```bash
http://localhost:8501
```

---

## 🏗️ Additional Setup: Creating a Custom Bridge Network
Create a custom bridge network for flexibility:
```bash
docker network create --driver bridge my_custom_network
```

### 7️⃣ Insert Dummy Data into PostgreSQL
Connect to your **PostgreSQL** container:
```bash
docker exec -it my_postgres psql -U admin -d mydb
```
Run the following SQL commands to create a table and insert sample data:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

INSERT INTO users (name, email) VALUES
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com');

SELECT * FROM users;
```

### 8️⃣ Running the Streamlit App with a Custom Network
```bash
docker run --name streamlit_ap --network my_custom_network -p 8501:8501 my_streamlit_app
```

---

## 🎉 Conclusion
You have successfully built and deployed a **Full Stack App** using **Docker, PostgreSQL, and Streamlit**! Your app is now running in isolated containers that communicate over a **Docker network**. 🚀

Happy Coding! ✨

