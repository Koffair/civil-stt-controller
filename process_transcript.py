from graphql_service import create_episode, publish_episode

def process_transcript(audio_id, transcript, audio_url):
  program_slug = audio_id.split("_")[0]
  release_date = audio_id.split("_")[1]

  data = create_episode(transcript, program_slug, release_date, audio_url)
  print(data)
  episode_id = data['data']['createEpisode']['id']
  publish_episode(episode_id)
  print(audio_id, 'episode created and published')
