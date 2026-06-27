import React from "react";
import { Sparkles, Save, Copy, Database } from "lucide-react";

export default function Topbar({ project, health, actions }) {
  return (
    <header className="topbar">
      <div>
        <div className={health.ok ? "badge online" : "badge offline"}>
          <Database size={13}/> 백엔드 {health.ok ? "연결됨" : "미연결"}
        </div>
        <h2>{project.name}</h2>
        <p>상품 URL 하나로 쇼츠 제작 패키지와 AI 팀 작업을 준비합니다.</p>
      </div>

      <div className="topActions">
        <button onClick={actions.sample}>샘플</button>
        <button onClick={actions.copy}><Copy size={16}/> 복사</button>
        <button onClick={actions.save}><Save size={16}/> 저장</button>
        <button className="primary" onClick={actions.oneClick}><Sparkles size={17}/> 원클릭 제작 준비</button>
      </div>
    </header>
  );
}
