from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from sqlmodel import Session
from dependencies.dependencies import get_current_user, require_roles
from db.db import get_db

from controllers.EquipamentoController import (
    buscar_equipamentos,
    buscar_equipamento_por_id,
    cadastraEquipamentoController,
    atualizarEquipamentoController,
    excluirEquipamentoController,

    buscar_status_quipamento_controller,
    buscar_status_equipamento_por_id_controller,
    cadastra_status_equipamento_controller,
    atualiza_status_equipamento_controller,
    excluirStatusEquipamentoController
)

from entidades.models import EquipamentoEntrada, EquipamentoStatus

EquipamentoRouter = APIRouter(dependencies=[Depends(get_current_user)])


@EquipamentoRouter.get("/equipamentos", tags=["Equipamentos"])
def get_equipamentos(db: Session = Depends(get_db)):
    return buscar_equipamentos(db)


@EquipamentoRouter.get("/equipamento/{id_equipamento}", tags=["Equipamentos"])
def busca_equipamento_por_id(id_equipamento: int, db: Session = Depends(get_db)):

    resultado = buscar_equipamento_por_id(id_equipamento, db)

    if resultado is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Equipamento {id_equipamento} não foi encontrado'
        )

    return resultado


@EquipamentoRouter.post(
    "/equipamentos",
    status_code=status.HTTP_201_CREATED,
    tags=["Equipamentos"], dependencies=[Depends(require_roles("administrador"))])
def cadastraEquipamento(equipamento: EquipamentoEntrada, db: Session = Depends(get_db)):

    equipamento_cadastrado = cadastraEquipamentoController(equipamento, db)

    if equipamento_cadastrado is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Status id{equipamento.status_id} não foi encontrado'
        )

    return equipamento_cadastrado


@EquipamentoRouter.put("/equipamento/{id_equipamento}", tags=["Equipamentos"], dependencies=[Depends(require_roles("administrador"))])
def atualizarEquipamento(id_equipamento: int, dados: EquipamentoEntrada, db: Session = Depends(get_db)):

    equipamento_atualizado = atualizarEquipamentoController(
        id_equipamento,
        dados,
        db
    )

    if equipamento_atualizado is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Equipamento {id_equipamento} não foi encontrado'
        )

    return equipamento_atualizado


@EquipamentoRouter.delete("/equipamento/{id_equipamento}", tags=["Equipamentos"], dependencies=[Depends(require_roles("administrador"))])
def excluirEquipamento(id_equipamento: int, db: Session = Depends(get_db)):

    equipamento_excluido = excluirEquipamentoController(id_equipamento, db)

    if equipamento_excluido is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Equipamento {id_equipamento} não foi encontrado'
        )

    return equipamento_excluido


@EquipamentoRouter.get("/status-equipamento", tags=["Status Equipamentos"])
def buscar_status_quipamento(db: Session = Depends(get_db)):
    return buscar_status_quipamento_controller(db)


@EquipamentoRouter.get(
    "/status-equipamento/{status_id}",
    tags=["Status Equipamentos"]
)
def buscar_status_equipamento_por_id(status_id: int, db: Session = Depends(get_db)):

    resultado = buscar_status_equipamento_por_id_controller(status_id,db)

    if resultado is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Equipamento {status_id} não foi encontrado'
        )

    return resultado


@EquipamentoRouter.post(
    "/status-equipamento",
    status_code=status.HTTP_201_CREATED,
    tags=["Status Equipamentos"], dependencies=[Depends(require_roles("administrador"))])
def cadastra_status_equipamento(status: EquipamentoStatus, db: Session = Depends(get_db)):

    status_equipamento = cadastra_status_equipamento_controller(db, status)

    return status_equipamento


@EquipamentoRouter.put(
    "/status-equipamento/{status_id}",
    tags=["Status Equipamentos"], dependencies=[Depends(require_roles("administrador"))])
def atualiza_status_equipamento(
    status_id: int,
    equipamento: EquipamentoStatus,
    db: Session = Depends(get_db)
):

    status_equipamento_atualizado = atualiza_status_equipamento_controller(
        status_id,
        equipamento,
        db
    )

    if status_equipamento_atualizado is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Equipamento {status_id} não foi encontrado'
        )

    return status_equipamento_atualizado


@EquipamentoRouter.delete(
    "/status-equipamento/{status_id}",
    tags=["Status Equipamentos"], dependencies=[Depends(require_roles("administrador"))])
def excluirStatusEquipamento(status_id: int, db: Session = Depends(get_db)):

    status_equipamento_excluido = excluirStatusEquipamentoController(status_id, db)

    if status_equipamento_excluido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Status {status_id} nao foi encontrado'
        )

    return status_equipamento_excluido