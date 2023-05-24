# main.py
from dotenv import load_dotenv
import os
import sqlite3
import sched, time
from checkdir import check_dir
from process_transcript import process_transcript

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
connection.commit()

def read_textfile(file):
  src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
  f = open(src_fpath, 'r')
  content = f.read()
  f.close()
  return content

def get_audio_id(file):
  audio_id = os.path.splitext(file)[0]
  return audio_id

def update_transcript_in_db(audio_id, transcript):
  cursor.execute("INSERT INTO transcripts (audio_id, transcript, status) VALUES (?, ?, ?) ON CONFLICT(audio_id) DO UPDATE SET transcript = excluded.transcript, status = excluded.status", (audio_id, transcript, 'done'))
  connection.commit()
  print(audio_id, 'transcript updated in database')

def process_file(file):
  if file.endswith('.txt'):
    audio_id = get_audio_id(file)
    transcript = read_textfile(file)
    update_transcript_in_db(audio_id, transcript)
    process_transcript(audio_id, transcript)

def remove_text_file(file):
  if file.endswith('.txt'):
    src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
    os.remove(src_fpath)
    print(file, 'transcript text file removed')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('OUTPUT_FOLDER'), process_file, remove_text_file))
my_scheduler.run()
