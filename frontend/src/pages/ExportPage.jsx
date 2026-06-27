import React from "react";

export default function ExportPage({ project, actions }) {
  return (
    <div className="page">
      <div className="pageHead">
        <h3>업로드 준비</h3>
        <button className="primary" onClick={actions.uploadPlan}>업로드 플랜 생성</button>
      </div>

      <div className="exportGrid">
        <div className="panel soft"><h4>유튜브/인스타/틱톡 플랜</h4><pre>{project.uploadPlan ? JSON.stringify(project.uploadPlan, null, 2) : "업로드 플랜을 생성해줘."}</pre></div>
        <div className="panel soft"><h4>복사용 해시태그</h4><p>{(project.hashtags || []).join(" ")}</p></div>
      </div>
    </div>
  );
}
