# main.py
from dotenv import load_dotenv
import os
import sched, time
from checkdir import check_dir
from db_service import add_episode_to_db
from functions import get_audio_metadata
from graphql_service import gql_create_episode_and_publish
from file_service import move_or_copy_file

load_dotenv()

def process_file(file):
  if file.endswith('.mp3'):
    audio_id, program_slug, release_date, audio_url = get_audio_metadata(file)
    add_episode_to_db(audio_id, file)
    gql_create_episode_and_publish(audio_id, program_slug, release_date, audio_url, "")  
    print(file, 'added to gql db')
    move_or_copy_file(os.getenv('INPUT_FOLDER'), os.getenv('AUDIO_PUBLIC_FOLDER'), file, True)
    print(file, 'moved to public folder')


def move_to_processed(file):
  if file.endswith('.mp3'):
    move_or_copy_file(os.getenv('INPUT_FOLDER'), os.getenv('PROCESSING_FOLDER'), file)
    print(file, 'moved to processing folder')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('INPUT_FOLDER'), process_file, move_to_processed))
my_scheduler.run()
