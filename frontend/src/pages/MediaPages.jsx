import React from "react";

export function ImagePage({ project }) {
  return <Media title="이미지 생성 준비" items={project.scenes || []} field="imagePrompt" />;
}

export function VideoPage({ project }) {
  return <Media title="영상 생성 준비" items={project.scenes || []} field="videoPrompt" />;
}

export function VoicePage({ project }) {
  return (
    <div className="page">
      <div className="pageHead"><h3>AI 음성</h3><span className="pill">TTS</span></div>
      <div className="panel soft"><h4>TTS 가이드</h4><p>{project.ttsGuide || "제작 패키지를 먼저 생성해줘."}</p><pre>{project.script}</pre></div>
    </div>
  );
}

function Media({ title, items, field }) {
  return (
    <div className="page">
      <div className="pageHead"><h3>{title}</h3><span className="pill">API Ready</span></div>
      <div className="promptGrid">
        {items.map((s, i) => <div className="panel soft" key={i}><b>{i+1}. {s.title}</b><p>{s[field]}</p></div>)}
      </div>
    </div>
  );
}
