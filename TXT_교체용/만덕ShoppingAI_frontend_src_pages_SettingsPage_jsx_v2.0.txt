import React from "react";

export default function SettingsPage({ health }) {
  return (
    <div className="page">
      <div className="pageHead"><h3>설정</h3><span className="pill">API</span></div>
      <div className="statGrid">
        <div className="stat"><span>백엔드</span><b>{health.ok ? "연결됨" : "미연결"}</b></div>
        <div className="stat"><span>OpenAI</span><b>{health.openai ? "준비됨" : "미설정"}</b></div>
        <div className="stat"><span>이미지 API</span><b>{health.image ? "준비됨" : "미설정"}</b></div>
        <div className="stat"><span>영상 API</span><b>{health.video ? "준비됨" : "미설정"}</b></div>
      </div>
      <div className="panel soft"><pre>{`OPENAI_API_KEY=\nIMAGE_API_KEY=\nVIDEO_API_KEY=\nTTS_API_KEY=\nSUPABASE_URL=\nSUPABASE_KEY=`}</pre></div>
    </div>
  );
}
