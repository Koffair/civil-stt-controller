import os

def check_dir(scheduler, dirname, action, purgeAction=None): 
  scheduler.enter(5, 1, check_dir, (scheduler, dirname, action, purgeAction))
  files = os.listdir(dirname)

  if len(files) > 0:
    for file in files:
      action(file)

      if purgeAction:
        purgeAction(file)
