import React, { useState } from "react";
import { chat } from "../api";
import { Citations } from "./Citations";

export function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function ask() {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer(null);
    try {
      const res = await chat(question);
      setAnswer(res);
    } catch (e: any) {
      setAnswer({ answer: `Error: ${e.message}`, citations: [] });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{border: "1px solid #ddd", padding: 12, borderRadius: 8, marginTop: 16}}>
      <h3>Ask a question</h3>
      <textarea
        rows={3}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{width: "100%"}}
        placeholder="Ask based on the uploaded PDF guides..."
      />
      <button onClick={ask} disabled={loading} style={{marginTop: 8}}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div style={{marginTop: 12}}>
          <div style={{whiteSpace: "pre-wrap"}}>{answer.answer}</div>
          <div style={{marginTop: 6, color: "#666"}}>
            Confidence: {Number(answer.confidence || 0).toFixed(2)}
            {answer.refusal ? " (refused)" : ""}
            {answer.reason ? ` — ${answer.reason}` : ""}
          </div>
          <Citations citations={answer.citations || []} />
        </div>
      )}
    </div>
  );
}