export function createProject() {
  return {
    id: crypto.randomUUID(),
    name: "새 프로젝트",
    url: "",
    productName: "",
    price: "",
    target: "",
    pros: "",
    reviews: "",
    style: "조회수형",
    duration: "30초",
    productImage: "",
    analysis: null,
    script: "",
    scenes: [],
    captions: "",
    titles: [],
    hashtags: [],
    thumbnailTexts: [],
    imagePrompts: [],
    videoPrompts: [],
    ttsGuide: "",
    uploadPlan: null,
    jobs: [],
    team: [
      { role: "팀장 AI", status: "대기", result: "" },
      { role: "상품조사 AI", status: "대기", result: "" },
      { role: "대본 AI", status: "대기", result: "" },
      { role: "이미지 AI", status: "대기", result: "" },
      { role: "영상 AI", status: "대기", result: "" },
      { role: "음성 AI", status: "대기", result: "" },
      { role: "업로드 AI", status: "대기", result: "" },
    ],
    logs: ["프로젝트 생성 완료"],
    status: "대기",
  };
}

export function sampleProject() {
  const p = createProject();
  return {
    ...p,
    name: "무선 미니 차량용 청소기",
    productName: "무선 미니 차량용 청소기",
    price: "29,900원 / 무료배송",
    target: "차량 내부 청소가 귀찮은 사람",
    pros: "가볍고 휴대하기 좋음\n좁은 틈새 청소 가능\n책상과 차량 모두 사용 가능",
    reviews: "생각보다 흡입력이 좋아요\n차 안에 두고 쓰기 편해요\n가격 대비 만족합니다",
  };
}
