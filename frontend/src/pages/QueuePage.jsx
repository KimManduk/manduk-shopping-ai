import React from "react";

export default function QueuePage({ project, actions }) {
  return (
    <div className="page">
      <div className="pageHead">
        <h3>작업 큐</h3>
        <button className="primary" onClick={actions.createJobs}>전체 작업 큐 생성</button>
      </div>

      <div className="queue">
        {(project.jobs || []).length ? project.jobs.map((j) => (
          <div className="job" key={j.id}>
            <b>{j.title}</b>
            <span>{j.type}</span>
            <p>{j.status}</p>
          </div>
        )) : <p className="muted">아직 작업이 없습니다.</p>}
      </div>
    </div>
  );
}
