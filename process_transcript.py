import os
import requests

def process_transcript(audio_id, transcript):
  mutation_add_episode = """
    mutation CreateEpisode($transcript: String) {
      createEpisode(data: { transcript: $transcript }) {
        id
      }
    }
  """
  
  url='https://api-eu-central-1-shared-euc1-02.hygraph.com/v2/clfqmnhz406nv01t7fcc9azhz/master'
  token = os.getenv("HYGRAPH_TOKEN")
  headers = {"Authorization": f"Bearer {token}"}
  variables = {"transcript": transcript}


  r = requests.post(url, json={"query": mutation_add_episode, "variables": variables}, headers=headers)
  json_data = r.json()
  print(json_data)
