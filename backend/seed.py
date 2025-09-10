from database import Base, engine, SessionLocal
from models import Turma, Aluno
from datetime import date
import random

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Turmas iniciais
turmas = [
    Turma(nome="1º Ano A", capacidade=3),
    Turma(nome="1º Ano B", capacidade=2),
    Turma(nome="2º Ano A", capacidade=4),
]
for turma in turmas:
    if not db.query(Turma).filter(Turma.nome == turma.nome).first():
        db.add(turma)
db.commit()

# Alunos iniciais
nomes = ["Ana", "Bruno", "Carla", "Diego", "Eduarda", "Felipe", "Gabriela", "Henrique", "Isabela", "Jhony"]
emails = [f"{nome.lower()}@escola.com" for nome in nomes]

for i in range(10):
    if not db.query(Aluno).filter(Aluno.email == emails[i]).first():
        aluno = Aluno(
            nome=nomes[i],
            data_nascimento=date(2010, random.randint(1, 12), random.randint(1, 28)),
            email=emails[i],
            status="inativo"
        )
        db.add(aluno)
db.commit()
db.close()
print("✅ Banco populado com sucesso!")
