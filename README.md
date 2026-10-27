# MeetingMind

MeetingMind is a Python-based API that answers questions about team meeting transcripts. It retrieves relevant transcript evidence, uses a local language model to generate an answer, and returns citations so users can trace answers back to the source meetings.

## Features

- FastAPI endpoints for health checks and meeting questions.
- Supports VTT, SRT, TXT, and JSON transcript formats.
- Loads meeting metadata from a manifest and SQLite database.
- Normalizes speaker names and aliases.
- Retrieves relevant transcript turns using keyword-based ranking.
- Supports project, date, speaker, and reference-date filtering.
- Limits transcript evidence using `tiktoken`.
- Returns citations with meeting IDs, timestamps, and speaker IDs.
- Handles unanswerable and out-of-scope questions.

## Requirements

- Python 3.10 or later
- [Ollama](https://ollama.com/) installed and running
- The local Ollama model `qwen3:4b`

## Setup

1. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Make sure Ollama is running and download the model if needed.

   ```powershell
   ollama pull qwen3:4b
   ```

4. Start the API from the project root.

   ```powershell
   uvicorn main:app --reload
   ```

The API will be available at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Health check

`GET /health`

Checks whether the API is running.

### Ask a question

`POST /ask`

Example request:

```json
{
  "question": "What was the mobile launch date?",
  "project": "mobile-app-launch",
  "as_of": "2026-04-01"
}
```

The response includes the answer, route, citations, applied filters, and reference date.

Possible routes include:

- `answer` — relevant evidence supports an answer.
- `no_answer` — the available evidence does not support an answer.
- `out_of_scope` — the question is outside the supported meeting-information scope.

## Configuration

The application uses the following default paths and settings:

- `data/manifest.json` — meeting manifest.
- `data/orbit.db` — SQLite meeting metadata.
- `data/transcripts/` — transcript files.
- `APP_TODAY` — defaults to `2026-07-01`, used as the fixed reference date.
- `LLM_PROVIDER` — configuration value defaults to `ollama`.

The transcript and database paths can be overridden using `TRANSCRIPTS_DIR`, `MANIFEST_PATH`, and `DB_PATH` environment variables.

##