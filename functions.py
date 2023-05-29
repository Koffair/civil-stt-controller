import os

def get_audio_metadata(file):
  audio_id = os.path.splitext(file)[0]
  program_slug = audio_id.split("_")[0]
  release_date = audio_id.split("_")[1]
  audio_url = os.getenv('AUDIO_BASE_URL') + '/' + audio_id + '.mp3'
  return audio_id, program_slug, release_date, audio_url
