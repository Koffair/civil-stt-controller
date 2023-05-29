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
  data = create_episode(audio_id, program_slug, release_date, audio_url, transcript)
  episode_id = data['data']['createEpisode']['id']
  publish_episode(episode_id)

def gql_update_episode_transcript_and_publish(episode_id, transcript):
  print('gql_update_episode_transcript_and_publish')
  update_transcript(episode_id, transcript)
  publish_episode(episode_id)
