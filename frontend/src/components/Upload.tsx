import React, { useState } from "react";
import { ingest } from "../api";

export function Upload() {
  const [status, setStatus] = useState<string>("");

  async function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setStatus("Uploading + indexing...");
    try {
      const out = await ingest(f);
      setStatus(`Indexed: ${out.title} (chunks: ${out.chunks_indexed})`);
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    }
  }

  return (
    <div style={{border: "1px solid #ddd", padding: 12, borderRadius: 8}}>
      <h3>Upload PDF</h3>
      <input type="file" accept="application/pdf" onChange={onFileChange} />
      <div style={{marginTop: 8, color: "#444"}}>{status}</div>
    </div>
  );
}