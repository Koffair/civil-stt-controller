# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import sqlite3

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()

app = FastAPI()
@app.get("/")
async def root():
  rows = cursor.execute("SELECT audio_id, audio_file, transcript, status FROM transcripts").fetchall()
  return rows



 