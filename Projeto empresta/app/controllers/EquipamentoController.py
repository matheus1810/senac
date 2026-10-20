from fastapi import HTTPException
from sqlmodel import Session, select
from entidades.models import (EquipamentoEntrada, EquipamentoTabela, EquipamentoStatus,
                              StatusEquipamentoTabela, AlmoxarifadoTabela, ItemSolicitacaoTabela,
                              EmprestimoTabela)


def buscar_equipamentos(db: Session):
    return db.exec(select(EquipamentoTabela)).all()


def buscar_equipamento_por_id(id_equipamento: int, db: Session):
    return db.get(EquipamentoTabela, id_equipamento)


def validar_referencias(dados: EquipamentoEntrada, db: Session):
    if db.get(StatusEquipamentoTabela, dados.status_id) is None:
        raise HTTPException(404, "Status nao encontrado")
    if db.get(AlmoxarifadoTabela, dados.id_almoxarifado) is None:
        raise HTTPException(404, "Almoxarifado nao encontrado")


def cadastraEquipamentoController(dados: EquipamentoEntrada, db: Session):
    validar_referencias(dados, db)
    equipamento = EquipamentoTabela(**dados.model_dump())
    db.add(equipamento)
    db.commit()
    db.refresh(equipamento)
    return equipamento


def equipamento_bloqueado(id_equipamento: int, db: Session):
    return db.exec(select(EmprestimoTabela).join(ItemSolicitacaoTabela,
        EmprestimoTabela.item_solicitacao_id == ItemSolicitacaoTabela.id).where(
            ItemSolicitacaoTabela.id_equipamento == id_equipamento,
            EmprestimoTabela.data_devolucao.is_(None))).first() is not None


def atualizarEquipamentoController(id_equipamento: int, dados: EquipamentoEntrada, db: Session):
    equipamento = db.exec(select(EquipamentoTabela).where(
        EquipamentoTabela.id == id_equipamento).with_for_update()).first()
    if equipamento is None:
        return None
    validar_referencias(dados, db)
    if equipamento_bloqueado(id_equipamento, db):
        raise HTTPException(409, "Equipamento possui emprestimo ativo")
    for campo, valor in dados.model_dump().items():
        setattr(equipamento, campo, valor)
    db.add(equipamento)
    db.commit()
    db.refresh(equipamento)
    return equipamento


def excluirEquipamentoController(id_equipamento: int, db: Session):
    equipamento = db.exec(select(EquipamentoTabela).where(
        EquipamentoTabela.id == id_equipamento).with_for_update()).first()
    if equipamento is None:
        return None
    if db.exec(select(ItemSolicitacaoTabela).where(
            ItemSolicitacaoTabela.id_equipamento == id_equipamento)).first():
        raise HTTPException(409, "Equipamento possui solicitacoes vinculadas")
    db.delete(equipamento)
    db.commit()
    return {"detail": "Equipamento removido"}


def buscar_status_quipamento_controller(db: Session):
    return db.exec(select(StatusEquipamentoTabela)).all()


def buscar_status_equipamento_por_id_controller(status_id: int, db: Session):
    return db.get(StatusEquipamentoTabela, status_id)


def cadastra_status_equipamento_controller(db: Session, dados: EquipamentoStatus):
    registro = StatusEquipamentoTabela(**dados.model_dump())
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


def atualiza_status_equipamento_controller(status_id: int, dados: EquipamentoStatus, db: Session):
    registro = db.get(StatusEquipamentoTabela, status_id)
    if registro is None:
        return None
    if db.exec(select(EquipamentoTabela).where(EquipamentoTabela.status_id == status_id)).first():
        raise HTTPException(409, "Status em uso nao pode ser alterado")
    registro.status = dados.status
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro


def excluirStatusEquipamentoController(status_id: int, db: Session):
    registro = db.get(StatusEquipamentoTabela, status_id)
    if registro is None:
        return None
    if db.exec(select(EquipamentoTabela).where(EquipamentoTabela.status_id == status_id)).first():
        raise HTTPException(409, "Status em uso nao pode ser excluido")
    db.delete(registro)
    db.commit()
    return {"detail": "Status removido"}
