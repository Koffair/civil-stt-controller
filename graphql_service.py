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


def create_episode(audio_id, program_slug, release_date, audio_url, transcript = ""):
  mutation = """
    mutation CreateEpisode(
      $transcript: String,
      $programSlug: String,
      $releaseDate: Date,
      $audioUrl: String,
      $audioId: String
    ) {
      createEpisode(data: {
        transcript: $transcript
        program: {
          connect: {
            slug: $programSlug
          }
        }
        releaseDate: $releaseDate,
        audioUrl: $audioUrl,
        audioId: $audioId
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
    "audioUrl": audio_url,
    "audioId": audio_id
  }
  return mutate(mutation, variables)

def publish_episode(audio_id):
  mutation = """
    mutation publishEpisode($audioId: String) {
      publishEpisode(where: { audioId: $audioId }, to: PUBLISHED) {
        audioId
      }
    }
  """
  variables = {
    "audioId": audio_id
  }
  return mutate(mutation, variables)


def update_transcript(audio_id, transcript):
  mutation = """
    mutation UpdateEpisodeTranscript($audioId: String, $transcript: String){
      updateEpisode(
        where: { audioId: $audioId },
        data: {
          transcript: $transcript
        }) {
        id
      }
    }
  """
  variables = {
    "audioId": audio_id,
    "transcript": transcript
  }
  return mutate(mutation, variables)

def gql_create_episode_and_publish(audio_id, program_slug, release_date, audio_url, transcript = ""):
  create_episode(audio_id, program_slug, release_date, audio_url, transcript)
  publish_episode(audio_id)

def gql_update_episode_transcript_and_publish(audio_id, transcript):
  update_transcript(audio_id, transcript)
  publish_episode(audio_id)
  print('gql_update_episode_transcript_and_publish')
