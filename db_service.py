import sqlite3

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()

def init_db():
  # connection = sqlite3.connect("transcripts.sqlite")
  cursor.execute("CREATE TABLE IF NOT EXISTS transcripts (audio_id TEXT UNIQUE, audio_file TEXT, transcript TEXT, status TEXT, error_message TEXT)")
  connection.commit()

def add_episode_to_db(audio_id, file, error_message=''):
  init_db()
  if len(error_message) > 0:
    status = 'error'
  else: 
    status = 'pending'  
  print(status)
  cursor.execute("INSERT INTO transcripts (audio_id, audio_file, transcript, status, error_message) VALUES (?, ?, ?, ?, ?) ON CONFLICT(audio_id) DO UPDATE SET audio_file = excluded.audio_file, transcript = excluded.transcript, status = excluded.status, error_message = excluded.error_message", (audio_id, file, '', status, error_message))
  connection.commit()
  # print(file, 'added to database')

def update_transcript_in_db(audio_id, transcript, error_message=''):
  if len(error_message) > 0:
    status = 'error'
  else: 
    status = 'done' 

  if len(transcript) > 100:
    transcript=transcript[:99]

  print(status)
  cursor.execute("INSERT INTO transcripts (audio_id, transcript, status, error_message) VALUES (?, ?, ?, ?) ON CONFLICT(audio_id) DO UPDATE SET transcript = excluded.transcript, status = excluded.status, error_message = excluded.error_message", (audio_id, transcript, status, error_message))
  connection.commit()
  print(audio_id, 'transcript updated in database')  