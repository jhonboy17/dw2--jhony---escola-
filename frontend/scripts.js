const API_URL = "http://127.0.0.1:8000";

// Listar alunos em tabela
async function listarAlunos() {
  const search = document.getElementById("searchAluno").value;
  let url = `${API_URL}/alunos`;
  if (search) {
    url += `?search=${search}`;
  }

  const res = await fetch(url);
  const alunos = await res.json();

  const tbody = document.getElementById("alunos");
  tbody.innerHTML = "";

  alunos.forEach(aluno => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${aluno.id}</td>
      <td>${aluno.nome}</td>
      <td>${aluno.status}</td>
      <td>${aluno.email ?? "-"}</td>
      <td>${aluno.turma_id ?? "-"}</td>
    `;
    tbody.appendChild(tr);
  });
}

window.onload = listarAlunos;
