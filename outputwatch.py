# main.py
from dotenv import load_dotenv
import os
import sched, time
from checkdir import check_dir
from functions import get_audio_metadata
from graphql_service import gql_update_episode_transcript_and_publish
from db_service import update_transcript_in_db
from file_service import move_or_copy_file

load_dotenv()

def read_textfile(file):
  src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
  f = open(src_fpath, 'r')
  content = f.read()
  f.close()
  return content


def process_file(file):
  if file.endswith('.txt'):
    audio_id, program_slug, release_date, audio_url = get_audio_metadata(file)
    transcript = read_textfile(file)
    error_message = ''
    try:
      gql_update_episode_transcript_and_publish(audio_id, transcript=transcript)

    except Exception as error:
      print("gql update was not succesful, error: ", error)
      move_or_copy_file(os.getenv('PROCESSING_FOLDER'), os.getenv('ERROR_FOLDER'), audio_id + '.mp3', True)
      move_or_copy_file(os.getenv('OUTPUT_FOLDER'), os.getenv('ERROR_FOLDER'), file, True)
      error_message=str(error)

    update_transcript_in_db(audio_id, transcript, error_message=error_message)

def delete_from_processed(file):
  audio_id, program_slug, release_date, audio_url = get_audio_metadata(file)
  os.remove(os.getenv('PROCESSING_FOLDER') + '/' + audio_id + '.mp3')
  print(file, 'deleted from processing folder')


def remove_text_file(file):
  if file.endswith('.txt'):
    delete_from_processed(file)
    src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
    os.remove(src_fpath)
    print(file, 'transcript text file removed')


my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('OUTPUT_FOLDER'), process_file, remove_text_file))
my_scheduler.run()
