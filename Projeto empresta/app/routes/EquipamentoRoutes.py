from fastapi import FastAPI,APIRouter,status, HTTPException

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

from entidades.models import EquipamentoEntrada,EquipamentoStatus

EquipamentoRouter = APIRouter()

@EquipamentoRouter.get("/equipamentos")
def get_equipamentos():
    return buscar_equipamentos()
    
@EquipamentoRouter.get("/equipamento/{id_equipamento}")
def busca_equipamento_por_id(id_equipamento : int):

    resultado = buscar_equipamento_por_id(id_equipamento)

    if(resultado is None):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = f'Equipamento {id_equipamento} não foi encontrado'
        )

    return resultado

@EquipamentoRouter.post("/equipamentos",status_code=status.HTTP_201_CREATED)
def cadastraEquipamento(equipamento : EquipamentoEntrada):
    
    equipamento_cadastrado = cadastraEquipamentoController(equipamento)
    
    if (equipamento_cadastrado is None):
        raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail = f'Status id{equipamento.status_id} não foi encontrado'
            )

    return equipamento_cadastrado

@EquipamentoRouter.put("/equipamento/{id_equipamento}")
def atualizarEquipamento(id_equipamento:int, dados:EquipamentoEntrada):

    equipamento_atualizado =  atualizarEquipamentoController(id_equipamento, dados)

    if(equipamento_atualizado is None):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = f'Equipamento {id_equipamento} não foi encontrado'
        )

    return equipamento_atualizado
  
@EquipamentoRouter.delete("/equipamento/{id_equipamento}")
def excluirEquipamento(id_equipamento:int):

    equipamento_excluido = excluirEquipamentoController(id_equipamento)

    if(equipamento_excluido is None):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = f'Equipamento {id_equipamento} não foi encontrado'
        )


    return equipamento_excluido

@EquipamentoRouter.get("/status-equipamento")
def buscar_status_quipamento():
    return buscar_status_quipamento_controller()

@EquipamentoRouter.get("/status-equipamento/{status_id}")
def buscar_status_equipamento_por_id( status_id : int ):
    
    resultado = buscar_status_equipamento_por_id_controller(status_id)
    
    if(resultado is None):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = f'Equipamento {status_id} não foi encontrado'
        )

    return resultado

@EquipamentoRouter.post('/status-equipamento',status_code=status.HTTP_201_CREATED)
def cadastra_status_equipamento( status : EquipamentoStatus):

    status_equipamento = cadastra_status_equipamento_controller(status)
    
    return status_equipamento

@EquipamentoRouter.put('/status-equipamento/{status_id}')
def atualiza_status_equipamento(status_id : int, equipamento : EquipamentoStatus):
    
    status_equipamento_atualizado =  atualiza_status_equipamento_controller(status_id, equipamento)
    
    if(status_equipamento_atualizado is None):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail = f'Equipamento {status_id} não foi encontrado'
        )

    return status_equipamento_atualizado

@EquipamentoRouter.delete('/status-equipamento/{status_id}')
def excluirStatusEquipamento(status_id : int):
    status_equipamento_exluido = excluirStatusEquipamentoController(status_id)
    
    return status_equipamento_exluido