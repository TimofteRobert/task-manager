import { api } from "./api.js";

async function loadProjects() {
    const projects = await api.listProjects();
    const list = document.getElementById("project-list");
    list.innerHTML = "";

    for (const project of projects) {
        const li = document.createElement("li");
        li.textContent = `${project.name} (${project.tasks.length} tasks)`;
        list.appendChild(li);
    }
}

loadProjects();