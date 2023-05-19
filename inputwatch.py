# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sqlite3
import sched, time
from checkdir import check_dir

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transcripts (audio_file TEXT, transcript TEXT, status TEXT)")
connection.commit()

input_dir_content = os.listdir(os.getenv('INPUT_FOLDER'))

def add_to_db(file):
  print(file, 'added to database')
  cursor.execute("INSERT INTO transcripts (audio_file, transcript, status) VALUES (?, ?, ?)", (file, '', 'pending'))
  connection.commit()

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('INPUT_FOLDER'), add_to_db))
my_scheduler.run()
