from fastapi import APIRouter, Depends
from sqlmodel import Session
from controllers.AuthController import fazer_login
from db.db import get_db
from dependencies.dependencies import get_current_user, papel_usuario
from entidades.models import LoginEntrada, UsuarioTabela, UsuarioSaida

AuthRouter = APIRouter(tags=["Autenticacao"])

@AuthRouter.post("/login")
def login(dados: LoginEntrada, db: Session = Depends(get_db)):
    return fazer_login(db, dados.email, dados.senha)

@AuthRouter.get("/auth/me")
def me(usuario: UsuarioTabela = Depends(get_current_user), db: Session = Depends(get_db)):
    dados = UsuarioSaida.model_validate(usuario, from_attributes=True).model_dump()
    return {**dados, "papel": papel_usuario(usuario, db)}
