import os
import requests

def mutate(mutation, variables):
  url=os.getenv('HYGRAPH_URL')
  token = os.getenv("HYGRAPH_TOKEN")
  headers = {"Authorization": f"Bearer {token}"}

  try:
    r = requests.post(url, json={"query3623": mutation, "variables": variables}, headers=headers)
    json_data = r.json()

    r.raise_for_status()
    return json_data
  
  except requests.exceptions.HTTPError as error: 
    print("HTTPError error", error)
    raise str(error)
  except requests.exceptions.ConnectionError as error:
    print("ConnectionError", error)
    raise error
  except requests.exceptions.Timeout:
    print("Timeout error", error)
    raise error
  except requests.exceptions.TooManyRedirects:
    print("TooManyRedirects error", error)
    raise error
  except requests.exceptions.RequestException as e:
    print("RequestException(catastrophic) error", error)
    raise error


def create_episode(audio_id, program_slug, release_date, audio_url, transcript = ""):
  mutation = """
    mutation upsertEpisode(
      $transcript: String,
      $programSlug: String,
      $releaseDate: Date,
      $audioUrl: String,
      $audioId: String
    ) {
      upsertEpisode(
        where:{ audioId: $audioId },
        upsert: {
          create: {
            transcript: $transcript
            program: {
              connect: {
                slug: $programSlug
              }
            }
            releaseDate: $releaseDate,
            audioUrl: $audioUrl,
            audioId: $audioId
          },
          update: {
            transcript: $transcript
            program: {
              connect: {
                slug: $programSlug
              }
            }
            releaseDate: $releaseDate,
            audioUrl: $audioUrl,
            audioId: $audioId
          }
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
