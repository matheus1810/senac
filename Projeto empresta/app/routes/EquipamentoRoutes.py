from fastapi import FastAPI,APIRouter,status, HTTPException

from controllers.EquipamentoController import (
buscar_equipamentos, 
buscar_equipamento_por_id, 
cadastraEquipamentoController,
atualizarEquipamentoController,
excluirEquipamentoController,

buscar_status_quipamento_controller,
buscar_status_equipamento_por_id_controller,
cadastra_status_equipamento_controller
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

    return cadastraEquipamentoController(equipamento)


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
    return buscar_status_equipamento_por_id_controller(status_id)

@EquipamentoRouter.post('/status-equipamento/{status}')
def cadastra_status_equipamento( status : str ):
    return cadastra_status_equipamento_controller(status)