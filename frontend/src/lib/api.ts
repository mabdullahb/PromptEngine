const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
};

export const api = {
  async get(endpoint: string) {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      headers: getAuthHeaders(),
    });
    if (res.status === 401) {
      window.location.href = "/login";
      throw new Error("Unauthorized");
    }
    if (!res.ok) throw new Error(`API Error: ${res.statusText}`);
    return res.json();
  },

  async post(endpoint: string, data: any) {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (res.status === 401) {
      window.location.href = "/login";
      throw new Error("Unauthorized");
    }
    if (!res.ok) throw new Error(`API Error: ${res.statusText}`);
    return res.json();
  },

  auth: {
    me: () => api.get("/auth/me"),
  },

  engine: {
    enhance: (rawPrompt: string, providerOverride?: string) => 
      api.post("/engine/enhance", { raw_prompt: rawPrompt, provider_override: providerOverride }),
    
    classify: (rawPrompt: string) => 
      api.post("/engine/classify", { raw_prompt: rawPrompt }),
    
    providers: () => api.get("/engine/providers"),
    
    history: (skip = 0, limit = 10) => 
      api.get(`/engine/history?skip=${skip}&limit=${limit}`),
  }
};
