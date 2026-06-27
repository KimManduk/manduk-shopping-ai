import React, { useState } from "react";
import { Search, Wand2 } from "lucide-react";

export default function ProductPage({ project, patch, actions }) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);
    try {
      const data = await actions.analyzeUrl();
      setResult(data);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <div className="pageHead">
        <h3>상품 입력/URL 분석</h3>
        <div className="row">
          <button onClick={analyze} disabled={loading}><Search size={16}/>{loading ? "분석중" : "URL 분석"}</button>
          <button className="primary" onClick={actions.generate}><Wand2 size={16}/> AI 제작 패키지</button>
        </div>
      </div>

      {result && (
        <div className={result.ok ? "notice success" : "notice error"}>
          <b>{result.ok ? "URL 분석 성공" : "URL 분석 실패"}</b>
          <p>{result.message}</p>
          {result.imageUrl ? <p>이미지: {result.imageUrl}</p> : null}
        </div>
      )}

      <div className="formGrid">
        <Field full label="상품 URL"><input value={project.url} onChange={e => patch({ url: e.target.value })} placeholder="쿠팡/스마트스토어/쇼핑몰 URL" /></Field>
        <Field label="상품명"><input value={project.productName} onChange={e => patch({ productName: e.target.value, name: e.target.value || "새 프로젝트" })} /></Field>
        <Field label="가격/혜택"><input value={project.price} onChange={e => patch({ price: e.target.value })} /></Field>
        <Field label="타깃 고객"><input value={project.target} onChange={e => patch({ target: e.target.value })} placeholder="예: 차량 청소가 귀찮은 사람" /></Field>
        <Field label="스타일"><select value={project.style} onChange={e => patch({ style: e.target.value })}><option>조회수형</option><option>광고형</option><option>정보형</option><option>리뷰형</option></select></Field>
        <Field label="길이"><select value={project.duration} onChange={e => patch({ duration: e.target.value })}><option>30초</option><option>45초</option><option>60초</option></select></Field>
        <Field full label="장점"><textarea value={project.pros} onChange={e => patch({ pros: e.target.value })} /></Field>
        <Field full label="리뷰/후기"><textarea value={project.reviews} onChange={e => patch({ reviews: e.target.value })} /></Field>
      </div>
    </div>
  );
}

function Field({ label, full, children }) {
  return <div className={full ? "field full" : "field"}><label>{label}</label>{children}</div>
}
