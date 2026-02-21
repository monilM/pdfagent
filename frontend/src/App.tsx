import React from "react";
import { Upload } from "./components/Upload";
import { Chat } from "./components/Chat";

export default function App() {
  return (
    <div style={{maxWidth: 900, margin: "30px auto", fontFamily: "system-ui"}}>
      <h2>PDF Guides Q&A (OSS RAG)</h2>
      <Upload />
      <Chat />
      <p style={{marginTop: 18, color: "#666"}}>
        Tip: Upload multiple guides. Ask questions and verify with citations.
      </p>
    </div>
  );
}