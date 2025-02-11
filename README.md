
# Full Stack App Using Docker

* Create a Docker network (bridge mode) to connect the two containers.
* Create a Docker container for the database (e.g., PostgreSQL or MySQL).
* Create a Docker container for the Streamlit app and connect it to the database using the network.




## Documentation

[Docker](https://docs.docker.com/)

[My SQL](https://hub.docker.com/_/mysql)

[Docker Network](https://docs.docker.com/engine/network/)





## Deployment

1. Create The network
```bash
docker network create my_network
```
2. Set Up the Database Container

```bash
docker run -d \
  --name my_postgres \
  --network my_network \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=adminpassword \
  -e POSTGRES_DB=mydb \
  postgres
```

This will create a PostgreSQL container named my_postgres connected to my_network

3. Create the Streamlit App Container


In your Streamlit project folder, create a Dockerfile:

```bash
# Use the official Streamlit image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the app files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Streamlit
CMD ["streamlit", "run", "stream.py", "--server.port=8501", "--server.address=0.0.0.0"]

```

Ensure that requirements.txt includes streamlit and psycopg2 (for PostgreSQL):

```bash
streamlit
psycopg2
```

4. Build and Run the Streamlit Container

Build the image:

```bash
docker build -t my_streamlit_app .
```

Run the container and connect it to my_network:

```bash
docker run -d \
  --name streamlit_app \
  --network my_network \
  -p 8501:8501 \
  my_streamlit_app

```

5. Connect the Streamlit App to PostgreSQL

Now we will create stream.py

```bash
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

6. Test the Setup

```bash
http://localhost:8501
```

Now we will create the Custom Bridge network

```bash
docker network create --driver bridge my_custom_network

```

7. Insert Dummy Data

* Connect to PostgreSQL Container
To access the PostgreSQL database inside the container, run:

```bash
docker exec -it my_postgres psql -U admin -d mydb

```

8. Create a Sample Table and Insert Data

```bash

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

9. Create a Dockerfile for Streamlit

```bash

# Use Python as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir streamlit psycopg2

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "stream.py", "--server.port=8501", "--server.address=0.0.0.0"]

```
Now we will run this command to do this:

```bash
docker run --name streamlit_ap --network mybridge -p 8501:8501 streamlit_app
```

THANK YOU.
