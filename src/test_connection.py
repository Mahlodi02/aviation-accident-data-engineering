import os
from dotenv import load_dotenv
from sqlalchemy import text
from db import get_engine


load_dotenv()


engine = get_engine()

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print("Connected! Postgres version:", result.fetchone()[0])