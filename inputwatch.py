# main.py
from dotenv import load_dotenv
import os
import sqlite3
import sched, time
import shutil
from checkdir import check_dir

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transcripts (audio_file TEXT, transcript TEXT, status TEXT)")
connection.commit()

input_dir_content = os.listdir(os.getenv('INPUT_FOLDER'))

def add_to_db(file):
  if file.endswith('.mp3'):
    cursor.execute("INSERT INTO transcripts (audio_file, transcript, status) VALUES (?, ?, ?)", (file, '', 'pending'))
    connection.commit()
    print(file, 'added to database')

def process_file(file):
  add_to_db(file)

def move_to_processed(file):
  if file.endswith('.mp3'):
    src_fpath = os.getenv('INPUT_FOLDER') + '/' + file
    dest_fpath = os.getenv('PROCESSING_FOLDER') + '/' + file
    os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
    shutil.move(src_fpath, dest_fpath)
    print(file, 'moved to processing folder')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('INPUT_FOLDER'), process_file, move_to_processed))
my_scheduler.run()
