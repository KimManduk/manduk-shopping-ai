import React from "react";
import { BarChart3, PackageSearch, Wand2, Users, ListChecks, Image, Video, Mic, Upload, Settings, Plus } from "lucide-react";

const menus = [
  ["dashboard", BarChart3, "대시보드"],
  ["product", PackageSearch, "상품"],
  ["studio", Wand2, "AI 제작"],
  ["team", Users, "AI 팀"],
  ["queue", ListChecks, "작업 큐"],
  ["image", Image, "이미지"],
  ["video", Video, "영상"],
  ["voice", Mic, "음성"],
  ["export", Upload, "업로드"],
  ["settings", Settings, "설정"],
];

export default function Sidebar({ projects, currentId, page, setPage, setCurrentId, addProject }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brandLogo">M</div>
        <div>
          <h1>만덕 Shopping AI</h1>
          <p>Studio v2.0 Clean</p>
        </div>
      </div>

      <button className="newBtn" onClick={addProject}><Plus size={17}/> 새 프로젝트</button>

      <div className="sideTitle">메뉴</div>
      <nav className="menu">
        {menus.map(([id, Icon, label]) => (
          <button key={id} className={page === id ? "active" : ""} onClick={() => setPage(id)}>
            <Icon size={17}/>{label}
          </button>
        ))}
      </nav>

      <div className="sideTitle">프로젝트</div>
      <div className="projectList">
        {projects.map((p) => (
          <button key={p.id} className={p.id === currentId ? "project active" : "project"} onClick={() => setCurrentId(p.id)}>
            <b>{p.name}</b>
            <span>{p.status}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
