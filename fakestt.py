# main.py
from dotenv import load_dotenv
import os
import sched, time
from checkdir import check_dir

load_dotenv()

def create_text_output(file):
  if file.endswith('.mp3'):
    audio_id = os.path.splitext(file)[0]
    f = open(os.getenv('OUTPUT_FOLDER') + '/' + audio_id + '.txt', 'w')
    f.write('Output file was created')
    print(audio_id + '.txt', "file was created in output folder")
    f.close()

def delete_from_processed(file):
  if file.endswith('.mp3'):
    os.remove(os.getenv('PROCESSING_FOLDER') + '/' + file)
    print(file, 'deleted from processing folder')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('PROCESSING_FOLDER'), create_text_output))
my_scheduler.run()
