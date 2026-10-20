from core.security import cria_hash_senha
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from entidades.models import PapelTabela, UsuarioEntrada, UsuarioTabela


def buscar_usuarios(db: Session):
    return db.exec(select(UsuarioTabela)).all()


def buscar_usuario_por_id(id_usuario: int, db: Session):
    return db.get(UsuarioTabela, id_usuario)


def validar_usuario(dados: UsuarioEntrada, db: Session, id_usuario: int | None = None):
    if db.get(PapelTabela, dados.role_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Papel nao foi encontrado")

    for campo in ("email", "cpf"):
        consulta = select(UsuarioTabela).where(
            getattr(UsuarioTabela, campo) == getattr(dados, campo)
        )
        if id_usuario is not None:
            consulta = consulta.where(UsuarioTabela.id != id_usuario)
        if db.exec(consulta).first() is not None:
            raise HTTPException(status.HTTP_409_CONFLICT, f'{campo} ja cadastrado')


def salvar_usuario(usuario: UsuarioTabela, db: Session):
    db.add(usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Os dados do usuario conflitam com os registros existentes",
        ) from None
    db.refresh(usuario)
    return usuario


def cadastrar_usuario_controller(dados: UsuarioEntrada, db: Session):
    validar_usuario(dados, db)
    valores = dados.model_dump()
    valores["senha"] = cria_hash_senha(dados.senha)
    return salvar_usuario(UsuarioTabela(**valores), db)


def atualizar_usuario_controller(id_usuario: int, dados: UsuarioEntrada, db: Session):
    usuario = buscar_usuario_por_id(id_usuario, db)
    if usuario is None:
        return None
    validar_usuario(dados, db, id_usuario)
    valores = dados.model_dump()
    valores["senha"] = cria_hash_senha(dados.senha)
    for campo, valor in valores.items():
        setattr(usuario, campo, valor)
    return salvar_usuario(usuario, db)


def excluir_usuario_controller(id_usuario: int, db: Session):
    usuario = buscar_usuario_por_id(id_usuario, db)
    if usuario is None:
        return None
    db.delete(usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Usuario possui registros vinculados e nao pode ser excluido",
        ) from None
    return f"Usuario {id_usuario} foi removido com sucesso"
