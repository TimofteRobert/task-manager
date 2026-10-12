import { api } from './api.js';

async function loadProjects() {
  const projects = await api.listProjects();
  const list = document.getElementById('project-list');
  list.innerHTML = '';

  for (const project of projects) {
    const li = document.createElement('li');
    li.textContent = `${project.name} (${project.tasks.length} tasks)`;
    list.appendChild(li);
  }
}

const form = document.getElementById('project-form');
const nameInput = document.getElementById('project-name');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const name = nameInput.value.trim();
  if (name === '') return;

  await api.createProject({ name: name });
  nameInput.value = '';
  await loadProjects();
})

loadProjects();
