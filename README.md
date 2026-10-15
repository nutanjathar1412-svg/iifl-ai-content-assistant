\# IIFL Finance - AI Content Assistant



\## Overview

A full-stack application that summarizes text using an AI service, generates exactly three tags, and saves entries for later viewing.



\## Features

\- Input validation

\- AI-generated summary and three tags

\- SQLite persistence

\- View saved entries and open individual entries

\- Error handling

\- Automated tests



\## Technology Stack

\- Frontend: React, Vite, CSS

\- Backend: Python, FastAPI

\- Database: SQLite

\- AI: OpenAI API

\- Testing: pytest



\## Project Structure

\- `frontend/` - React application

\- `backend/main.py` - API and AI processing

\- `backend/test\_main.py` - Automated tests

\- `backend/requirements.txt` - Python dependencies

\- `backend/.env.example` - Environment variable template



\## Setup



\### Backend

Run these commands from the `backend` directory:



```bash

python -m venv venv

```



On Windows:



```cmd

venv\\Scripts\\activate

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



Create `backend/.env` using `.env.example` as a template. Add your own API key locally if API credits are available. Never upload the real key.



Start the API:



```bash

python -m uvicorn main:app --host 127.0.0.1 --port 8000

```



API documentation: http://127.0.0.1:8000/docs



Health check: http://127.0.0.1:8000/health



\### Frontend

Open a second terminal in the `frontend` directory:



```bash

npm install

npm run dev

```



Open the local URL shown in the terminal, usually http://localhost:5173.



\## Automated Tests

From the `backend` directory, activate the virtual environment and run:



```bash

python -m pytest -v

```



The current automated tests check the health endpoint and reject text shorter than the required minimum.



\## AI Integration

The backend sends the submitted text to the OpenAI API and requests a concise summary and exactly three tags in JSON format. The response is validated before it is saved.



\## Reliability

\- Input length validation

\- AI response format validation

\- Controlled API error responses

\- Parameterized SQL queries for database operations



\## Privacy and Security

\- Store secrets in a local `.env` file.

\- Never commit API keys to GitHub.

\- `.env.example` contains a placeholder, not a real key.

\- Do not submit sensitive text to an external AI service without authorization.

\- Production deployments should use HTTPS and secure secret management.



\## Limitations

Live AI generation requires a working AI provider and available API credits. The automated tests do not require a paid AI request.



\## Future Improvements

\- User authentication and access control

\- Rate limiting and request timeouts

\- Additional AI and database error tests

\- Monitoring and structured logging

\- Secure production deployment and continuous integration



\## AI Tools

AI assistance was used to help plan the implementation, code, and documentation. Review the implementation and test results before submission.

