import os
import sys
import subprocess
import psycopg2

with psycopg2.connect(dbname=os.environ['POSTGRES_DB'],
                      user=os.environ['POSTGRES_USER'],
                      password=os.environ['POSTGRES_PASSWORD'],
                      host=os.environ['POSTGRES_HOST']) as conn:
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {os.environ['PROJECT_DB_NAME']}")
    except psycopg2.errors.DuplicateDatabase:
        sys.exit(0)

with psycopg2.connect(dbname=os.environ['PROJECT_DB_NAME'],
                      user=os.environ['PROJECT_USER'],
                      password=os.environ['PROJECT_USER_PASSWORD'],
                      host=os.environ['POSTGRES_HOST']) as conn:
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION pg_trgm")
    cursor.execute("CREATE EXTENSION fuzzystrmatch")

subprocess.call(["python3.8", "./tatartwin/manage.py", "migrate"])

subprocess.call(["python3.8", "./tatartwin/manage.py", "loaddata", "./tatartwin/data/tatar.json"])
subprocess.call(["python3.8", "./tatartwin/manage.py", "loaddata", "./tatartwin/data/translation.json"])
subprocess.call(["python3.8", "./tatartwin/manage.py", "loaddata", "./tatartwin/data/example.json"])
