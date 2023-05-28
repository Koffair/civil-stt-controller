import os
import requests

def process_transcript(audio_id, transcript, audio_url):
  program_slug = audio_id.split("_")[0]
  release_date = audio_id.split("_")[1]

  mutation_add_episode = """
    mutation CreateEpisode(
      $transcript: String,
      $programSlug: String,
      $releaseDate: Date,
      $audioUrl: String,
    ) {
      createEpisode(data: {
        transcript: $transcript
        program: {
          connect: {
            slug: $programSlug
          }
        }
        releaseDate: $releaseDate,
        audioUrl: $audioUrl
      }) {
        id
        program {
          id
        }
      }
    }
  """
  
  url='https://api-eu-central-1-shared-euc1-02.hygraph.com/v2/clfqmnhz406nv01t7fcc9azhz/master'
  token = os.getenv("HYGRAPH_TOKEN")
  headers = {"Authorization": f"Bearer {token}"}
  variables = {
    "transcript": transcript,
    "programSlug": program_slug,
    "releaseDate": release_date,
    "audioUrl": audio_url
  }

  r = requests.post(url, json={"query": mutation_add_episode, "variables": variables}, headers=headers)
  json_data = r.json()
  print(json_data)
