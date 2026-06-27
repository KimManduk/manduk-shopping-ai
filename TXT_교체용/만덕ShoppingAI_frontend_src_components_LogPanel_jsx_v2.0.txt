import React from "react";

export default function LogPanel({ logs }) {
  return (
    <div className="panel">
      <div className="panelHead">
        <h3>로그</h3>
        <span>LOG</span>
      </div>
      <div className="logs">
        {(logs || []).slice(0, 12).map((x, i) => <p key={i}>{x}</p>)}
      </div>
    </div>
  );
}
