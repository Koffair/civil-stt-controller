# main.py
from dotenv import load_dotenv
import os
import sched, time
import shutil
from checkdir import check_dir
from db_service import add_episode_to_db
from functions import get_audio_metadata
from graphql_service import gql_create_episode_and_publish

load_dotenv()

def process_file(file):
  if file.endswith('.mp3'):
    audio_id, program_slug, release_date, audio_url = get_audio_metadata(file)
    add_episode_to_db(audio_id, file)
    gql_create_episode_and_publish(audio_id, program_slug, release_date, audio_url, "")  

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
