# main.py
from dotenv import load_dotenv
import os
import sqlite3
import sched, time
from checkdir import check_dir

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
connection.commit()

def update_transcript_in_db(file):
  if file.endswith('.txt'):
    audio_id = os.path.splitext(file)[0]
    src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
    f = open(src_fpath, 'r')
    cursor.execute("INSERT INTO transcripts (audio_id, transcript, status) VALUES (?, ?, ?) ON CONFLICT(audio_id) DO UPDATE SET transcript = excluded.transcript, status = excluded.status", (audio_id, f.read(), 'done'))
    connection.commit()
    f.close()    
    print(file, 'transcript updated in database')

def process_file(file):
  update_transcript_in_db(file)

def remove_text_file(file):
  if file.endswith('.txt'):
    src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
    os.remove(src_fpath)
    print(file, 'transcript text file removed')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('OUTPUT_FOLDER'), process_file, remove_text_file))
my_scheduler.run()
