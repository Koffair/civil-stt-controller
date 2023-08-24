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

    try:
      if program_slug == "" or release_date == "":
        raise Exception("File name was incorrect")
      
    except: 
      print("An exception occurred")

    error_message=''
    dest_folder=os.getenv('AUDIO_PUBLIC_FOLDER')
    copy=True
    try:
      gql_create_episode_and_publish(audio_id, program_slug, release_date, audio_url, "") 
      print(file, 'added to gql db')
    except Exception as error:
      error_message=str(error)
      copy=False
      dest_folder=os.getenv('ERROR_FOLDER')
      print("gql create was not succesful, error: " + str(error))

    add_episode_to_db(audio_id, file, error_message=error_message)
    move_or_copy_file(os.getenv('INPUT_FOLDER'), dest_folder=dest_folder, file=file, copy=copy)
    print(file, 'copied to public folder: ', str(copy))

def move_to_processed(file):
  if file.endswith('.mp3'):
    if os.path.isfile(os.getenv('INPUT_FOLDER') + '/' + file):
      move_or_copy_file(os.getenv('INPUT_FOLDER'), os.getenv('PROCESSING_FOLDER'), file)
      print(file, 'moved to processing folder')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('INPUT_FOLDER'), process_file, move_to_processed))
my_scheduler.run()
