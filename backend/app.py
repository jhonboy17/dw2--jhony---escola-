from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Aluno, Turma
from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional, List

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Gestão Escolar")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# Schemas
# ------------------------------
class TurmaSchema(BaseModel):
    nome: str
    capacidade: int
class TurmaResponse(TurmaSchema):
    id: int
    class Config: orm_mode = True

class AlunoSchema(BaseModel):
    nome: str
    data_nascimento: date
    email: Optional[EmailStr] = None
    status: str = "inativo"
    turma_id: Optional[int] = None
class AlunoResponse(AlunoSchema):
    id: int
    class Config: orm_mode = True

class MatriculaSchema(BaseModel):
    aluno_id: int
    turma_id: int

# ------------------------------
# Health check
# ------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------------
# Turmas
# ------------------------------
@app.post("/turmas", response_model=TurmaResponse)
def criar_turma(turma: TurmaSchema, db: Session = Depends(get_db)):
    nova = Turma(nome=turma.nome, capacidade=turma.capacidade)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@app.get("/turmas", response_model=List[TurmaResponse])
def listar_turmas(db: Session = Depends(get_db)):
    return db.query(Turma).all()

# ------------------------------
# Alunos
# ------------------------------
@app.post("/alunos", response_model=AlunoResponse)
def criar_aluno(aluno: AlunoSchema, db: Session = Depends(get_db)):
    idade = (date.today() - aluno.data_nascimento).days // 365
    if idade < 5:
        raise HTTPException(status_code=400, detail="Aluno deve ter pelo menos 5 anos.")
    novo = Aluno(
        nome=aluno.nome,
        data_nascimento=aluno.data_nascimento,
        email=aluno.email,
        status=aluno.status,
        turma_id=aluno.turma_id
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@app.get("/alunos", response_model=List[AlunoResponse])
def listar_alunos(
    search: Optional[str] = None,
    turma_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Aluno)
    if search:
        query = query.filter(Aluno.nome.contains(search))
    if turma_id:
        query = query.filter(Aluno.turma_id == turma_id)
    if status:
        query = query.filter(Aluno.status == status)
    return query.all()

@app.put("/alunos/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, dados: AlunoSchema, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno.nome = dados.nome
    aluno.data_nascimento = dados.data_nascimento
    aluno.email = dados.email
    aluno.status = dados.status
    aluno.turma_id = dados.turma_id
    db.commit()
    db.refresh(aluno)
    return aluno

@app.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return {"detail": "Aluno deletado com sucesso"}

# ------------------------------
# Matrícula
# ------------------------------
@app.post("/matriculas")
def matricular(matricula: MatriculaSchema, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == matricula.aluno_id).first()
    turma = db.query(Turma).filter(Turma.id == matricula.turma_id).first()
    if not aluno: raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if not turma: raise HTTPException(status_code=404, detail="Turma não encontrada")
    ocupacao = db.query(Aluno).filter(Aluno.turma_id == turma.id).count()
    if ocupacao >= turma.capacidade:
        raise HTTPException(status_code=400, detail="Turma sem vagas disponíveis")
    aluno.turma_id = turma.id
    aluno.status = "ativo"
    db.commit()
    db.refresh(aluno)
    return {"detail": f"Aluno {aluno.nome} matriculado na turma {turma.nome} com sucesso!"}
