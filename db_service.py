import sqlite3

connection = sqlite3.connect("transcripts.sqlite")
cursor = connection.cursor()

def init_db():
  # connection = sqlite3.connect("transcripts.sqlite")
  cursor.execute("CREATE TABLE IF NOT EXISTS transcripts (audio_id TEXT UNIQUE, audio_file TEXT, transcript TEXT, status TEXT)")
  connection.commit()

def add_episode_to_db(audio_id, file):
  init_db()
  cursor.execute("INSERT INTO transcripts (audio_id, audio_file, transcript, status) VALUES (?, ?, ?, ?) ON CONFLICT(audio_id) DO UPDATE SET audio_file = excluded.audio_file, transcript = excluded.transcript", (audio_id, file, '', 'pending'))
  connection.commit()
  # print(file, 'added to database')

def update_transcript_in_db(audio_id, transcript):
  init_db()
  cursor.execute("INSERT INTO transcripts (audio_id, transcript, status) VALUES (?, ?, ?) ON CONFLICT(audio_id) DO UPDATE SET transcript = excluded.transcript, status = excluded.status", (audio_id, transcript, 'done'))
  connection.commit()
  print(audio_id, 'transcript updated in database')  
