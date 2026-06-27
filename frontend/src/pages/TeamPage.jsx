import React from "react";
import { Users } from "lucide-react";

export default function TeamPage({ project, actions }) {
  return (
    <div className="page">
      <div className="pageHead">
        <h3>AI 팀 시스템</h3>
        <button className="primary" onClick={actions.runTeam}><Users size={16}/> AI 팀 실행</button>
      </div>

      <div className="teamGrid">
        {(project.team || []).map((m, i) => (
          <div className="teamCard" key={i}>
            <b>{m.role}</b>
            <span className={m.status === "완료" ? "done" : m.status === "진행중" ? "running" : ""}>{m.status}</span>
            <p>{m.result}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
