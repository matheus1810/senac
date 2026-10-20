from fastapi import HTTPException
from sqlmodel import Session, select
from entidades.models import UsuarioTabela
from core.security import verifica_senha, criar_token
from dependencies.dependencies import papel_usuario

def fazer_login(db: Session, username: str, password: str):
    usuario = db.exec(select(UsuarioTabela).where(UsuarioTabela.email == username)).first()
    if usuario is None or not verifica_senha(password, usuario.senha):
        raise HTTPException(401, "E-mail ou senha invalidos", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": criar_token(str(usuario.id), [papel_usuario(usuario, db)]),
            "token_type": "bearer"}
