
import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [text, setText] = useState("");
  const [entry, setEntry] = useState(null);
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadEntries() {
    try {
      const response = await fetch(`${API}/entries`);
      if (!response.ok) throw new Error("Could not load saved entries");
      setEntries(await response.json());
    } catch {
      setError("Backend शी connection होत नाही. Backend चालू आहे का तपासा.");
    }
  }

  async function generateContent(event) {
    event.preventDefault();
    setError("");
    setEntry(null);
    setLoading(true);

    try {
      const response = await fetch(`${API}/entries`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Content generate झाले नाही.");
      }

      setEntry(data);
      setText("");
      await loadEntries();
    } catch (err) {
      setError(err.message || "काहीतरी चुकले. पुन्हा प्रयत्न करा.");
    } finally {
      setLoading(false);
    }
  }

  async function openEntry(id) {
    setError("");
    try {
      const response = await fetch(`${API}/entries/${id}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Entry सापडली नाही.");
      setEntry(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="page">
      <header className="header">
        <div className="logo">AI</div>
        <div>
          <h1>AI Content Assistant</h1>
          <p>Summarize, organize, and save your ideas.</p>
        </div>
      </header>

      <section className="panel">
        <h2>Create content summary</h2>
        <p className="muted">Paste your text below to generate a summary and 3 tags.</p>

        <form onSubmit={generateContent}>
          <label htmlFor="content">Your content</label>
          <textarea
            id="content"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste an article, notes, or any text (minimum 10 characters)..."
            minLength={10}
            maxLength={10000}
            required
          />
          <div className="form-footer">
            <span>{text.length}/10000 characters</span>
            <button disabled={loading || text.trim().length < 10}>
              {loading ? "Generating..." : "Generate summary"}
            </button>
          </div>
        </form>
        {error && <p className="error" role="alert">{error}</p>}
      </section>

      {entry && (
        <section className="panel">
          <h2>Summary</h2>
          <p>{entry.summary}</p>
          <h3>Tags</h3>
          <div className="tags">
            {entry.tags?.map((tag, index) => (
              <span className="tag" key={`${tag}-${index}`}>{tag}</span>
            ))}
          </div>
          <details>
            <summary>View original text</summary>
            <p className="original">{entry.original_text}</p>
          </details>
        </section>
      )}

      <section className="panel">
        <div className="section-heading">
          <div>
            <h2>Saved entries</h2>
            <p className="muted">Your previously generated summaries.</p>
          </div>
          <button className="secondary" onClick={loadEntries} type="button">
            Refresh
          </button>
        </div>

        {entries.length === 0 ? (
          <p className="muted">No saved entries loaded yet. Click Refresh to view saved content.</p>
        ) : (
          <div className="entries">
            {entries.map((item) => (
              <button
                className="entry"
                key={item.id}
                type="button"
                onClick={() => openEntry(item.id)}
              >
                <strong>{item.summary}</strong>
                <span>{item.tags?.join(" · ")}</span>
                <small>Entry #{item.id} · Click to open</small>
              </button>
            ))}
          </div>
        )}
      </section>

      <footer>AI Content Assistant · Built with React, FastAPI, and SQLite</footer>
    </main>
  );
}
