import os
import requests

def mutate(mutation, variables):
  url=os.getenv('HYGRAPH_URL')
  token = os.getenv("HYGRAPH_TOKEN")
  headers = {"Authorization": f"Bearer {token}"}

  r = requests.post(url, json={"query": mutation, "variables": variables}, headers=headers)
  json_data = r.json()
  # print(json_data)
  return json_data


def create_episode(transcript, program_slug, release_date, audio_url):
  mutation = """
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

  variables = {
    "transcript": transcript,
    "programSlug": program_slug,
    "releaseDate": release_date,
    "audioUrl": audio_url
  }
  return mutate(mutation, variables)

def publish_episode(episode_id):
  mutation = """
    mutation publishEpisode($episodeId: ID) {
      publishEpisode(where: { id: $episodeId }, to: PUBLISHED) {
        id
      }
    }
  """
  variables = {
    "episodeId": episode_id
  }
  return mutate(mutation, variables)
