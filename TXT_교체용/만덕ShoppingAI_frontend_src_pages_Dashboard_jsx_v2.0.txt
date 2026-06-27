import React from "react";
import { CheckCircle2, Circle } from "lucide-react";

export default function Dashboard({ project, actions }) {
  const items = [
    ["상품 정보", project.productName],
    ["AI 제작 패키지", project.analysis],
    ["대본", project.script],
    ["장면", project.scenes?.length],
    ["작업 큐", project.jobs?.length],
    ["업로드 플랜", project.uploadPlan],
  ];

  return (
    <div className="page">
      <div className="pageHead">
        <h3>대시보드</h3>
        <button className="primary" onClick={actions.oneClick}>원클릭 제작 준비</button>
      </div>

      <div className="statGrid">
        <Stat title="상품" value={project.productName || "대기"} />
        <Stat title="장면" value={`${project.scenes?.length || 0}개`} />
        <Stat title="작업" value={`${project.jobs?.length || 0}개`} />
        <Stat title="상태" value={project.status} />
      </div>

      <div className="checkGrid">
        {items.map(([label, done]) => (
          <div className="checkCard" key={label}>
            {done ? <CheckCircle2 className="green" /> : <Circle className="mutedIcon" />}
            <b>{label}</b>
            <span>{done ? "완료" : "대기"}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Stat({ title, value }) {
  return <div className="stat"><span>{title}</span><b>{value}</b></div>;
}
