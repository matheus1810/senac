from entidades.models import EquipamentoEntrada,EquipamentoStatus,StatusEquipamentoTabela
from sqlmodel import Session, select

equipamentos = [
       {
         "id" : 1,
         "nome" : 'Câmera'
       },
        {
         "id" : 2,
         "nome" : 'Notebook'
       }, 
    ]

#------------------------------- EQUIPAMENTO CONTROLLERS ------------------------------------------------------------

def buscar_equipamentos():
    return equipamentos

def buscar_equipamento_por_id(id_equipamento : int):
   
    for item in equipamentos:
            if item["id"] == id_equipamento:
                return item

    return None

def cadastraEquipamentoController(equipamento: EquipamentoEntrada, db: Session):
    
    maior = 0
    for item in equipamentos:
       
        if item["id"] > maior:
            maior = item["id"]
    
    novo_id = maior + 1 
    
    status_encontrado = buscar_status_equipamento_por_id_controller(equipamento.status_id, db)
    
    if (status_encontrado is None):
        return

    novo_equipamento = {
        "id": novo_id,
        "nome":equipamento.nome,
        "status_id" : equipamento.status_id
    }
    
    equipamentos.append(novo_equipamento)
    return novo_equipamento

def atualizarEquipamentoController(id_equipamento: int, dados: EquipamentoEntrada, db: Session):
    
    status_encontrado = buscar_status_equipamento_por_id_controller(dados.status_id, db)
    
    if (status_encontrado is None):
        return
    
    for item in equipamentos:
                if item["id"] == id_equipamento:
                    item["nome"] = dados.nome
                    return item 

def excluirEquipamentoController(id_equipamento:int):

    for item in equipamentos:
        if item["id"] == id_equipamento:
            equipamentos.remove(item)
            return f"item {id_equipamento} foi removido com sucesso"

#------------------------------- STATUS EQUIPAMENTO CONTROLLERS ------------------------------------------------------------

def buscar_status_quipamento_controller(db:Session):
    statement = select(StatusEquipamentoTabela)
    status_encontrados = db.exec(statement).all()
    return status_encontrados

def buscar_status_equipamento_por_id_controller(status_id: int, db: Session):
    return db.get(StatusEquipamentoTabela, status_id)


def cadastra_status_equipamento_controller(db:Session, status_equipamento: EquipamentoStatus):
    
    novo_status_equipamento = StatusEquipamentoTabela(**status_equipamento.model_dump())

    db.add(novo_status_equipamento)
    db.commit()
    db.refresh(novo_status_equipamento)

    return novo_status_equipamento

def atualiza_status_equipamento_controller(
    status_id: int, equipamento: EquipamentoStatus, db: Session
):
    status_equipamento = buscar_status_equipamento_por_id_controller(status_id, db)
    if status_equipamento is None:
        return None

    status_equipamento.status = equipamento.status
    db.add(status_equipamento)
    db.commit()
    db.refresh(status_equipamento)
    return status_equipamento


def excluirStatusEquipamentoController(id_status: int, db: Session):
    status_equipamento = buscar_status_equipamento_por_id_controller(id_status, db)
    if status_equipamento is None:
        return None

    db.delete(status_equipamento)
    db.commit()
    return f"item {id_status} foi removido com sucesso"
