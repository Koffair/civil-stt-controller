# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
rows = cursor.execute("SELECT audio_file, transcript, status FROM transcripts").fetchall()

input_dir_content = os.listdir(os.getenv('INPUT_FOLDER'))

app = FastAPI()
@app.get("/")
async def root():
  return rows



 