
import os
import json
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DB_PATH = BASE_DIR / "content.db"

app = FastAPI(title="AI Content Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    text: str = Field(min_length=10, max_length=10000)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT NOT NULL,
                summary TEXT NOT NULL,
                tags TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/entries")
def create_entry(request: ContentRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Set OPENAI_API_KEY."
        )

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Summarize the supplied text and return only valid JSON "
                        'with keys "summary" and "tags". Summary must be concise. '
                        "Tags must be an array containing exactly 3 short strings."
                    ),
                },
                {"role": "user", "content": request.text},
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        result = json.loads(content or "{}")
        summary = result.get("summary")
        tags = result.get("tags")

        if (
            not isinstance(summary, str)
            or not summary.strip()
            or not isinstance(tags, list)
            or len(tags) != 3
            or not all(isinstance(tag, str) and tag.strip() for tag in tags)
        ):
            raise ValueError("Invalid AI response format")

    except Exception as exc:
        print(f"AI processing failed: {exc}")
        raise HTTPException(
            status_code=502,
            detail="AI processing failed. Please try again."
        )

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO entries (original_text, summary, tags) VALUES (?, ?, ?)",
                (request.text, summary.strip(), json.dumps(tags)),
            )
            entry_id = cursor.lastrowid

        return {
            "id": entry_id,
            "original_text": request.text,
            "summary": summary.strip(),
            "tags": tags,
        }
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Could not save content.")

@app.get("/entries")
def list_entries():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, original_text, summary, tags, created_at "
            "FROM entries ORDER BY id DESC"
        ).fetchall()

    return [
        {
            "id": row[0],
            "original_text": row[1],
            "summary": row[2],
            "tags": json.loads(row[3]),
            "created_at": row[4],
        }
        for row in rows
    ]

@app.get("/entries/{entry_id}")
def get_entry(entry_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, original_text, summary, tags, created_at "
            "FROM entries WHERE id = ?",
            (entry_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Entry not found.")

    return {
        "id": row[0],
        "original_text": row[1],
        "summary": row[2],
        "tags": json.loads(row[3]),
        "created_at": row[4],
    }
