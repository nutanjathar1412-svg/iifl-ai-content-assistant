# IIFL Finance – AI Content Assistant

A full-stack application that accepts user-provided text, generates a concise summary and three tags, and stores the result for later viewing.

## Features

- React-based frontend built with Vite.
- FastAPI REST API with input validation.
- Summary and exactly three tags in the normal AI integration flow.
- SQLite database for persistent entry storage.
- View saved entries and open individual entries.
- Error handling for invalid input, database errors, and AI failures.
- Free Demo Mode for local testing without OpenAI API credits.
- Automated tests using pytest.

## Technology Stack

- **Frontend:** React, Vite, CSS
- **Backend:** Python, FastAPI
- **Database:** SQLite
- **AI provider:** OpenAI API
- **Testing:** pytest

## Architecture

1. The user enters text in the React frontend and submits it.
2. The frontend sends a request to the FastAPI backend.
3. The backend validates the input and checks the configured operating mode.
4. In AI mode, the backend sends the text to the configured OpenAI model and requests JSON containing a summary and three tags.
5. The backend validates the AI response before saving the entry.
6. The original text, summary, and tags are stored in SQLite.
7. The frontend displays the generated result and retrieves saved entries through the API.

## Project Structure

```text
iifl-ai-content-assistant/
├── backend/
│   ├── main.py
│   ├── test_main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── .gitignore
└── README.md
```

## Prerequisites

- Python installed on your system.
- Node.js and npm installed.
- Git (optional, for cloning the repository).
- An OpenAI API key with available API credits for live AI generation.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nutanjathar1412-svg/iifl-ai-content-assistant.git
cd iifl-ai-content-assistant
```

If the project is already on your computer, open a terminal in the project directory instead.

### 2. Configure the Backend

Open a terminal in the project directory and run:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows using Git Bash:

```bash
source venv/Scripts/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the local environment file from the example:

```bash
cp .env.example .env
```

Edit `backend/.env` and configure the required settings.

For free local Demo Mode:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
DEMO_MODE=true
```

For live AI mode, use a valid OpenAI API key with available API credits and set:

```env
OPENAI_API_KEY=your_actual_api_key
OPENAI_MODEL=gpt-4o-mini
DEMO_MODE=false
```

Replace the placeholder with your own key locally. Never commit the real key to GitHub.

Start the backend from the `backend` directory:

```bash
python -m uvicorn main:app --reload
```

The API runs at:

- API base URL: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

### 3. Configure the Frontend

Open a second terminal in the project directory and run:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in the terminal, for example:

http://localhost:5173/

Keep both the frontend and backend terminals running while using the application.

## How to Use the Application

1. Open the frontend in your browser.
2. Enter text containing at least 10 characters.
3. Click **Generate summary**.
4. Review the summary and three tags returned by the backend.
5. View saved entries and open an entry to inspect its content.

## Demo Mode and Limitations

Demo Mode is intended for local development and testing when OpenAI API credits are unavailable.

When `DEMO_MODE=true`:

- The backend does not call the OpenAI API.
- The summary is created from the first 35 words of the submitted text, with an ellipsis when more words remain.
- Three fixed tags are returned: `Demo Mode`, `Content Summary`, and `Local Preview`.
- The original text, demo summary, and tags are stored in SQLite.

**Important:** Demo Mode is not genuine LLM-generated summarization or tagging. It allows the application flow and database persistence to be tested without API usage. The assignment's real LLM integration requirement must be validated separately using a working provider configuration.

When `DEMO_MODE=false`, the backend attempts to use the configured OpenAI model. Live AI generation requires a valid API key and available API credits.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check backend health |
| POST | `/entries` | Validate text, generate output, and save an entry |
| GET | `/entries` | Retrieve saved entries |
| GET | `/entries/{entry_id}` | Retrieve a specific entry |
| GET | `/docs` | Explore the API documentation |

The content submission endpoint accepts JSON such as:

```json
{
  "text": "Enter at least ten characters of content here."
}
```

In the normal AI flow, the expected output contains a summary and exactly three tags.

## Automated Tests

From the `backend` directory, activate the virtual environment and run:

```bash
python -m pytest -v
```

The current automated tests cover:

- The health endpoint.
- Rejection of text shorter than the minimum allowed length.

Latest local test result:

- 2 tests passed.
- 2 deprecation warnings were reported for the FastAPI startup event handler.

The current test suite does not verify a live OpenAI API call or every Demo Mode and failure-handling scenario.

## Assignment Questions

### 1. Architecture

The React frontend collects text and sends it to the FastAPI REST API. The backend validates the input and either invokes the configured OpenAI model or uses Demo Mode. In AI mode, the response is parsed and validated to ensure that it contains a summary and exactly three tags. The original text, summary, and tags are stored in SQLite. The frontend displays the result and retrieves previously saved entries through the API.

### 2. AI Choice

The implementation is configured to use OpenAI's `gpt-4o-mini` model through the OpenAI API. The model is requested to return JSON containing a concise summary and exactly three tags. This is a lightweight design for a small text-processing prototype. Live generation depends on valid API credentials and available credits. Demo Mode is used for testing when live API access is unavailable.

### 3. Reliability

The backend validates input length and checks the structure of the AI response before saving it. Invalid AI output and model-call failures are handled with controlled API errors rather than returning malformed content as a successful result. Database failures are also handled. Further improvements could include request timeouts, retries with limits, and dedicated automated tests for AI failure scenarios.

### 4. Privacy

In live AI mode, the submitted text is sent to the configured OpenAI API for processing. Users should avoid submitting confidential financial information, personal identifiers, account numbers, authentication credentials, or other sensitive customer data without appropriate authorization and safeguards. Production use should include data minimization, access controls, secure secret management, and review of applicable provider data-handling requirements. Demo Mode does not send submitted text to OpenAI.

### 5. Production Next Steps

- Add more automated tests for Demo Mode, database persistence, malformed AI responses, and API failures.
- Improve reliability with timeouts, bounded retries, structured logging, and better frontend error messages.
- Strengthen privacy and deployment security through data minimization, access controls, HTTPS, and secure configuration management.

### 6. AI Coding Tools

ChatGPT was used to assist with implementation guidance, code changes, debugging, testing steps, and README preparation. The generated code was reviewed and modified during development. Validation included running the application locally, testing API endpoints, checking Demo Mode and SQLite persistence, and running pytest. AI-assisted output should be reviewed and tested before production use.

## Screenshot

Add a screenshot of the working application showing the input, generated result, three tags, and saved entries.

Save the screenshot as `docs/screenshot.png` in the repository, then use:

![AI Content Assistant working application](docs/screenshot.png)

The screenshot should use non-sensitive sample text. Do not include API keys or private customer information.

## Security

- Keep `.env` local and excluded from version control.
- Commit `.env.example` with placeholder configuration names only.
- Never publish API keys, credentials, or confidential customer data.
- Rotate any API key that has been exposed.
- Review all configuration and AI-generated code before deployment.

## AI Assistance Disclosure

AI assistance was used during development and documentation. The implementation was reviewed through local execution, API checks, and automated tests. Demo Mode was used to validate the main application flow without requiring paid API usage.

## License

No license has been specified for this project.
s