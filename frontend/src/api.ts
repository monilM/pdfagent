const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8001";

export async function chat(question: string) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question })
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function ingest(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/ingest`, {
    method: "POST",
    body: form
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}