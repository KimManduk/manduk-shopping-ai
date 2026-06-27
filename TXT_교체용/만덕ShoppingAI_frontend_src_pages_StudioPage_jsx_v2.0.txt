import React from "react";

export default function StudioPage({ project, patch, setSceneIndex }) {
  return (
    <div className="page">
      <div className="pageHead">
        <h3>AI 제작 패키지</h3>
        <span className="pill">Script / Scenes / Strategy</span>
      </div>

      <div className="scriptGrid">
        <div className="panel soft">
          <h4>대본</h4>
          <textarea className="bigText" value={project.script || ""} onChange={e => patch({ script: e.target.value })} placeholder="AI 제작 패키지를 생성해줘." />
        </div>

        <div className="panel soft">
          <h4>추천 제목</h4>
          {(project.titles || []).map((x, i) => <p className="line" key={i}>{i + 1}. {x}</p>)}
          <h4>해시태그</h4>
          <p>{(project.hashtags || []).join(" ")}</p>
          <h4>썸네일 문구</h4>
          {(project.thumbnailTexts || []).map((x, i) => <p className="line" key={i}>{x}</p>)}
        </div>
      </div>

      <div className="sceneList">
        {(project.scenes || []).map((s, i) => (
          <button className="scene" key={i} onClick={() => setSceneIndex(i)}>
            <b>{s.time} / {s.title}</b>
            <span>{s.caption}</span>
            <small>이미지: {s.imagePrompt}</small>
            <small>영상: {s.videoPrompt}</small>
          </button>
        ))}
      </div>
    </div>
  );
}
