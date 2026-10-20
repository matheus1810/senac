import unicodedata
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from core.security import decodificar_token
from db.db import get_db
from entidades.models import UsuarioTabela, PapelTabela

bearer_scheme = HTTPBearer(auto_error=False)

def papel_usuario(usuario: UsuarioTabela, db: Session) -> str:
    papel = db.get(PapelTabela, usuario.role_id)
    nome = unicodedata.normalize("NFKD", papel.responsabilidade if papel else "")
    nome = "".join(c for c in nome if not unicodedata.combining(c)).strip().lower()
    return {"aluno": "comum", "usuario": "comum", "usuario comum": "comum",
            "comum": "comum", "gestor": "gestor", "usuario gestor": "gestor",
            "administrador": "administrador", "usuario administrador": "administrador"}.get(nome, "")

def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
                     db: Session = Depends(get_db)) -> UsuarioTabela:
    erro = HTTPException(401, "Credenciais invalidas ou expiradas", headers={"WWW-Authenticate": "Bearer"})
    if creds is None:
        raise erro
    try:
        payload = decodificar_token(creds.credentials)
        usuario = db.get(UsuarioTabela, int(payload["sub"]))
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise erro from None
    if usuario is None:
        raise erro
    return usuario

def require_roles(*roles: str):
    def checker(usuario: UsuarioTabela = Depends(get_current_user), db: Session = Depends(get_db)):
        if papel_usuario(usuario, db) not in roles:
            raise HTTPException(403, "Seu perfil nao tem permissao para esta operacao")
        return usuario
    return checker
