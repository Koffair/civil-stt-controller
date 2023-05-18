# main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sqlite3
import sched, time

load_dotenv()

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transcripts (audio_file TEXT, transcript TEXT)")
cursor.execute("INSERT INTO transcripts VALUES ('test_file.mp3', 'blablabla')")
connection.commit()
rows = cursor.execute("SELECT audio_file, transcript FROM transcripts").fetchall()
print(rows)

dircontent = os.listdir(os.getenv('INPUT_FOLDER'))

def do_something(scheduler): 
    # schedule the next call first
    scheduler.enter(5, 1, do_something, (scheduler,))
    current_files = os.listdir(os.getenv('INPUT_FOLDER'))
    new_files = list(set(globals()['dircontent']).symmetric_difference(set(current_files)))
    globals()['dircontent'] = current_files
    print(new_files)

    # dircontent = os.listdir(os.getenv('INPUT_FOLDER'))

    # then do your stuff

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, do_something, (my_scheduler,))
my_scheduler.run()



app = FastAPI()
@app.get("/")
async def root():
 return {"dircontetn":dircontent}
 