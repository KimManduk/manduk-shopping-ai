import React from "react";

export default function Preview({ project, sceneIndex, setSceneIndex }) {
  const scenes = project.scenes || [];
  const scene = scenes[sceneIndex];

  return (
    <div className="panel previewPanel">
      <div className="panelHead">
        <h3>9:16 미리보기</h3>
        <span>{scenes.length ? `${sceneIndex + 1}/${scenes.length}` : "0/0"}</span>
      </div>

      <div className="phone">
        <div className="screen">
          {project.productImage ? <img src={project.productImage} alt="" /> : null}
          <div className="shade"></div>
          <div className="screenBadge">AI PRODUCT REELS</div>
          <div className="screenText">
            <h2>{scene?.caption || project.productName || "상품명을 입력하세요"}</h2>
            <p>{scene?.title || "AI가 장면을 구성합니다"}</p>
          </div>
        </div>
      </div>

      <div className="two">
        <button onClick={() => setSceneIndex(Math.max(0, sceneIndex - 1))}>이전</button>
        <button onClick={() => setSceneIndex(Math.min(Math.max(0, scenes.length - 1), sceneIndex + 1))}>다음</button>
      </div>
    </div>
  );
}
