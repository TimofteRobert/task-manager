const API_URL = "http://localhost:8000";

async function request(path, options = {}) {
    const response = await fetch(API_URL + path, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (response.status === 204) return null;
    if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    return response.json();
}

export const api = {
    listProjects: () => request("/projects"),
    getProject: (id) =>  request (`/projects/${id}`),
    createProject: (data) =>
        request("/projects", { method: "POST", body: JSON.stringify(data) }),
    updateProject: (id, data) =>
        request(`/projects/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    deleteProject: (id) => request(`/projects/${id}`, { method: "DELETE" }),
};