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
    f.write('"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."')
    print(audio_id + '.txt', "file was created in output folder")
    f.close()

def delete_from_processed(file):
  if file.endswith('.mp3'):
    os.remove(os.getenv('PROCESSING_FOLDER') + '/' + file)
    print(file, 'deleted from processing folder')

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(5, 1, check_dir, (my_scheduler, os.getenv('PROCESSING_FOLDER'), create_text_output))
my_scheduler.run()
