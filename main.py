# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sqlite3
import sched, time

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transcripts (audio_file TEXT, transcript TEXT, status TEXT)")
connection.commit()
# rows = cursor.execute("SELECT audio_file, transcript FROM transcripts").fetchall()
# print(rows)

input_dir_content = os.listdir(os.getenv('INPUT_FOLDER'))

def check_dir(scheduler): 
  scheduler.enter(5, 1, check_dir, (scheduler,))
  current_files = os.listdir(os.getenv('INPUT_FOLDER'))
  new_files = list(set(globals()['input_dir_content']).symmetric_difference(set(current_files)))
  globals()['input_dir_content'] = current_files

  if len(new_files) > 0:
    for file in new_files:
      if file.endswith('.mp3'):
        print(file, 'added to database')
        cursor.execute("INSERT INTO transcripts (audio_file, transcript, status) VALUES (?, ?, ?)", (file, '', 'pending'))
        connection.commit()
    # input_dir_content = os.listdir(os.getenv('INPUT_FOLDER'))

    # then do your stuff

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler,))
my_scheduler.run()



app = FastAPI()
@app.get("/")
async def root():
 return {"dircontetn":input_dir_content}
 