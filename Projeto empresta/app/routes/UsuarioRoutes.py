from dependencies.dependencies import require_roles
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from controllers.UsuarioController import (
    atualizar_usuario_controller,
    buscar_usuario_por_id,
    buscar_usuarios,
    cadastrar_usuario_controller,
    excluir_usuario_controller,
)
from db.db import get_db
from entidades.models import UsuarioEntrada, UsuarioSaida

UsuarioRouter = APIRouter(tags=["Usuarios"], dependencies=[Depends(require_roles("administrador"))])


@UsuarioRouter.get("/usuarios", response_model=list[UsuarioSaida])
def get_usuarios(db: Session = Depends(get_db)):
    return buscar_usuarios(db)


@UsuarioRouter.get("/usuario/{id_usuario}", response_model=UsuarioSaida)
def get_usuario_por_id(id_usuario: int, db: Session = Depends(get_db)):
    usuario = buscar_usuario_por_id(id_usuario, db)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario nao foi encontrado")
    return usuario


@UsuarioRouter.post(
    "/usuarios", status_code=status.HTTP_201_CREATED, response_model=UsuarioSaida
)
def cadastrar_usuario(dados: UsuarioEntrada, db: Session = Depends(get_db)):
    return cadastrar_usuario_controller(dados, db)


@UsuarioRouter.put("/usuario/{id_usuario}", response_model=UsuarioSaida)
def atualizar_usuario(id_usuario: int, dados: UsuarioEntrada, db: Session = Depends(get_db)):
    usuario = atualizar_usuario_controller(id_usuario, dados, db)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario nao foi encontrado")
    return usuario


@UsuarioRouter.delete("/usuario/{id_usuario}")
def excluir_usuario(id_usuario: int, db: Session = Depends(get_db)):
    resultado = excluir_usuario_controller(id_usuario, db)
    if resultado is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario nao foi encontrado")
    return resultado
