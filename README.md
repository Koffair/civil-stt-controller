# Civil STT Controller

## Description

This repository contains the controller for a Speech to Text (STT) service. The controller is responsible for handling MP3 audio files, hand over to the STT service and processing the generated transcripts.

The controller utilizes a local SQLite database and also maintains a remote GraphQL connection to the CMS system of a radio's archive website. It updates the MP3's path in the CMS along with the corresponding transcript.

The filenames of the MP3 audio files contain important metadata, including the slug of the program and the release date of the episode.

## Features

- Monitors a designated folder for incoming MP3 files.
- Moves incoming MP3 files to the "processing" folder (configured in the .env file under the variable `PROCESSING_FOLDER`).
- Adds a record to the local SQLite database indicating that the file is being processed, with the status field set to "processing".
- Resolves metadata from the filename and stores it in the database.
- Adds a record to the remote hygraph CMS via a GraphQL mutation, updating the MP3's path and associated metadata.

## How to Use

1. Clone the repository to your local machine.
2. Configure the necessary environment variables in the `.env` file:
   - `INPUT_FOLDER`: Path to the folder where incoming MP3 files are placed.
   - `PROCESSING_FOLDER`: Path to the folder where files are moved for processing.
   - `OUTPUT_FOLDER`: Path to the folder where the STT-generated transcripts are stored.
3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
4. Start the input watcher by running the following command:
   ```
   python inputwatch.py
   ```
   or
   ```
   python3 inputwatch.py
   ```
   This will begin monitoring the designated input folder for incoming MP3 files. When a new file arrives, it will be moved to the processing folder, a processing record will be added to the local SQLite database, and the metadata will be updated in the remote hygraph CMS.
5. Start the output watcher by running the following command:
   ```
   python outputwatch.py
   ```
   or
   ```
   python3 outputwatch.py
   ```
   This will monitor the output folder for the STT-generated transcripts. When a corresponding TXT file is detected (with the same name as the original MP3 file), the content of the TXT file will be read. The corresponding record in the SQLite database will be updated with the transcript content, the status will be set to "done," and the transcript will be added to the hygraph CMS.

## Requirements

- Python (version 3.x)

Certainly! Here's an additional section describing the REST API connected to the local SQLite database:

## REST API

The repository also includes a FastAPI engine that provides a REST API interface to interact with the local SQLite database. While not mandatory for enabling audio and transcript processing, starting the FastAPI server allows you to monitor the progress of the ongoing processes.

To start the FastAPI server, run the following command:
```
uvicorn main:app --reload
```

Once the server is running, you can access the API at `http://localhost:8000`.

### Endpoint

The following GET endpoint is available:

- **GET /**: Retrieves a list of all audio files in the database with the status of the transcripting process and the transcript.


## Handle running processes

If you reach your server via ssh and wanna kill the running python processes, do the following:

```
ps -ef | grep python
kill -9 <PID>
```