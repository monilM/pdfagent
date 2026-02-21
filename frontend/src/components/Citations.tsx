import React from "react";

export function Citations({ citations }: { citations: any[] }) {
  if (!citations?.length) return null;
  return (
    <div style={{marginTop: 10}}>
      <strong>Citations</strong>
      <ul>
        {citations.map((c, i) => (
          <li key={i}>
            {c.doc_title} — page {c.page} — {c.chunk_id} (score: {Number(c.score).toFixed(2)})
          </li>
        ))}
      </ul>
    </div>
  );
}