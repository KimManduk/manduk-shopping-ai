import React, { useEffect, useMemo, useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import Topbar from "./components/Topbar.jsx";
import Preview from "./components/Preview.jsx";
import LogPanel from "./components/LogPanel.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import ProductPage from "./pages/ProductPage.jsx";
import StudioPage from "./pages/StudioPage.jsx";
import TeamPage from "./pages/TeamPage.jsx";
import QueuePage from "./pages/QueuePage.jsx";
import { ImagePage, VideoPage, VoicePage } from "./pages/MediaPages.jsx";
import ExportPage from "./pages/ExportPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";
import { createProject, sampleProject } from "./utils/project.js";
import { api } from "./services/api.js";

const KEY = "manduk-shopping-ai-v2-clean";

export default function App() {
  const [projects, setProjects] = useState(() => {
    const saved = localStorage.getItem(KEY);
    return saved ? JSON.parse(saved) : [createProject()];
  });
  const [currentId, setCurrentId] = useState(projects[0]?.id);
  const [page, setPage] = useState("dashboard");
  const [sceneIndex, setSceneIndex] = useState(0);
  const [health, setHealth] = useState({ ok: false });

  const project = useMemo(() => projects.find(p => p.id === currentId) || projects[0], [projects, currentId]);

  useEffect(() => { api.health().then(setHealth).catch(() => setHealth({ ok:false })); }, []);

  function persist(next) {
    setProjects(next);
    localStorage.setItem(KEY, JSON.stringify(next));
  }

  function patch(data) {
    persist(projects.map(p => p.id === project.id ? { ...p, ...data } : p));
  }

  function log(msg) {
    patch({ logs: [`[${new Date().toLocaleTimeString("ko-KR")}] ${msg}`, ...(project.logs || [])] });
  }

  function addProject() {
    const p = createProject();
    persist([p, ...projects]);
    setCurrentId(p.id);
    setPage("product");
  }

  async function analyzeUrl() {
    const data = await api.analyzeUrl(project);
    if (data.ok) {
      patch({
        productName: data.productName || project.productName,
        name: data.productName || project.name,
        price: data.price || project.price,
        pros: data.pros ? (project.pros ? project.pros + "\n" + data.pros : data.pros) : project.pros,
        productImage: data.imageUrl || project.productImage,
        target: project.target || "이 상품이 필요한 사람",
        status: "URL 분석 완료"
      });
      log("URL 분석 완료");
    } else {
      log(data.message || "URL 분석 실패");
    }
    return data;
  }

  async function generate() {
    patch({ status: "AI 제작 패키지 생성중" });
    const data = await api.generatePackage(project);
    patch({ ...data, name: data.productName || project.productName || project.name, status: "AI 제작 패키지 완료" });
    setPage("studio");
    setSceneIndex(0);
    log("AI 제작 패키지 생성 완료");
  }

  async function runTeam() {
    patch({ status: "AI 팀 실행중" });
    const data = await api.runTeam(project);
    patch({ team: data.team, status: "AI 팀 완료" });
    setPage("team");
    log("AI 팀 실행 완료");
  }

  async function createJobs() {
    const data = await api.createJobs(project);
    patch({ jobs: data.jobs, status: "작업 큐 생성 완료" });
    setPage("queue");
    log("작업 큐 생성 완료");
  }

  async function uploadPlan() {
    const data = await api.uploadPlan(project);
    patch({ uploadPlan: data.plan, status: "업로드 준비 완료" });
    setPage("export");
    log("업로드 플랜 생성 완료");
  }

  async function oneClick() {
    await generate();
    const latest = JSON.parse(localStorage.getItem(KEY)).find(p => p.id === project.id) || project;
    const team = await api.runTeam({ ...project, ...latest });
    const jobs = await api.createJobs({ ...project, ...latest });
    const plan = await api.uploadPlan({ ...project, ...latest });
    patch({ team: team.team, jobs: jobs.jobs, uploadPlan: plan.plan, status: "원클릭 제작 준비 완료" });
    setPage("dashboard");
    log("원클릭 제작 준비 완료");
  }

  function copy() {
    navigator.clipboard.writeText(JSON.stringify(project, null, 2));
    log("프로젝트 전체 복사 완료");
  }

  const actions = {
    analyzeUrl,
    generate,
    runTeam,
    createJobs,
    uploadPlan,
    oneClick,
    sample: () => {
      const p = sampleProject();
      persist([p, ...projects]);
      setCurrentId(p.id);
      setPage("product");
    },
    copy,
    save: () => { persist(projects); log("저장 완료"); },
  };

  const props = { project, patch, actions, health, setSceneIndex };

  return (
    <div className="appShell">
      <Sidebar projects={projects} currentId={project.id} page={page} setPage={setPage} setCurrentId={setCurrentId} addProject={addProject} />
      <main className="main">
        <Topbar project={project} health={health} actions={actions} />
        <section className="workGrid">
          <div className="mainPanel">
            {page === "dashboard" && <Dashboard {...props} />}
            {page === "product" && <ProductPage {...props} />}
            {page === "studio" && <StudioPage {...props} />}
            {page === "team" && <TeamPage {...props} />}
            {page === "queue" && <QueuePage {...props} />}
            {page === "image" && <ImagePage {...props} />}
            {page === "video" && <VideoPage {...props} />}
            {page === "voice" && <VoicePage {...props} />}
            {page === "export" && <ExportPage {...props} />}
            {page === "settings" && <SettingsPage {...props} />}
          </div>
          <aside className="rightPanel">
            <Preview project={project} sceneIndex={sceneIndex} setSceneIndex={setSceneIndex} />
            <LogPanel logs={project.logs} />
          </aside>
        </section>
      </main>
    </div>
  );
}
