import shutil
import os

def move_or_copy_file(src_folder, dest_folder, file, copy=False):
  src_fpath = src_folder + '/' + file
  dest_fpath = dest_folder + '/' + file
  os.makedirs(os.path.dirname(dest_fpath), exist_ok=True)
  if copy:
    shutil.copy(src_fpath, dest_fpath)
  else:
    shutil.move(src_fpath, dest_fpath)
  