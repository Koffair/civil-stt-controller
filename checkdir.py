import os

input_dir_content = []

def check_dir(scheduler, dirname, action): 
  scheduler.enter(5, 1, check_dir, (scheduler, dirname, action))
  current_files = os.listdir(dirname)
  new_files = list(set(globals()['input_dir_content']).symmetric_difference(set(current_files)))
  globals()['input_dir_content'] = current_files

  if len(new_files) > 0:
    for file in new_files:
      if file.endswith('.mp3'):
        action(file)
