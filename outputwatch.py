# main.py
from dotenv import load_dotenv
import os
import sched, time
from checkdir import check_dir
from functions import get_audio_metadata
from graphql_service import gql_update_episode_transcript_and_publish
from db_service import update_transcript_in_db

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
    update_transcript_in_db(audio_id, transcript)
    gql_update_episode_transcript_and_publish(audio_id, transcript=transcript)

def remove_text_file(file):
  if file.endswith('.txt'):
    src_fpath = os.getenv('OUTPUT_FOLDER') + '/' + file
    os.remove(src_fpath)
    print(file, 'transcript text file removed')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('OUTPUT_FOLDER'), process_file, remove_text_file))
my_scheduler.run()
