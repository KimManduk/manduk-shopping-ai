const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function request(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: body ? "POST" : "GET",
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `API error ${res.status}`);
  }

  return res.json();
}

export const api = {
  health: () => request("/api/health"),
  analyzeUrl: (project) => request("/api/product/analyze-url", project),
  generatePackage: (project) => request("/api/ai/generate-package", project),
  runTeam: (project) => request("/api/team/run", project),
  createJobs: (project) => request("/api/jobs/create-all", project),
  uploadPlan: (project) => request("/api/export/upload-plan", project),
};
