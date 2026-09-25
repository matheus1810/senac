from entidades.models import EquipamentoEntrada,EquipamentoStatus

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

status_equipamento = [
    {
        "id" : 1,
        "status" : 'DISPONIVEL'
    },
     {
        "id" : 2,
        "status" : 'EMPRESTADO'
    },
     {
        "id" : 3,
        "status" : 'IDISPONIVEL'
    },
     {
        "id" : 4,
        "status" : 'MANUTENCAO'
    }
]


#------------------------------- EQUIPAMENTO CONTROLLERS ------------------------------------------------------------

def buscar_equipamentos():
    return equipamentos

def buscar_equipamento_por_id(id_equipamento : int):
   
    for item in equipamentos:
            if item["id"] == id_equipamento:
                return item

    return None

def cadastraEquipamentoController(equipamento : EquipamentoEntrada):
    
    maior = 0
    for item in equipamentos:
       
        if item["id"] > maior:
            maior = item["id"]
    
    novo_id = maior + 1 
    
    status_encontrado = buscar_status_equipamento_por_id_controller(equipamento.status_id)
    
    if (status_encontrado is None):
        return

    novo_equipamento = {
        "id": novo_id,
        "nome":equipamento.nome,
        "status_id" : equipamento.status_id
    }
    
    equipamentos.append(novo_equipamento)
    return novo_equipamento

def atualizarEquipamentoController(id_equipamento:int, dados:EquipamentoEntrada):
    
    status_encontrado = buscar_status_equipamento_por_id_controller(dados.status_id)
    
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

def buscar_status_quipamento_controller():
    return status_equipamento

def buscar_status_equipamento_por_id_controller( status_id : int):

    for status in status_equipamento:
        if status["id"] == status_id:
            return status
    
    return None

def cadastra_status_equipamento_controller( eq_status: EquipamentoStatus ):
    
    maior = 0
    for item in status_equipamento:
       
        if item["id"] > maior:
            maior = item["id"]
    
    novo_id = maior + 1 

    status_equipamento_novo = {
        "id": novo_id,
        "status":eq_status.status
    }
    
    status_equipamento.append(status_equipamento_novo)
    return status_equipamento_novo

def atualiza_status_equipamento_controller(status_id : int, equipamento : EquipamentoStatus):
    for item in status_equipamento:
        if item["id"] == status_id:
            item["status"] = equipamento.status
            return item 

def excluirStatusEquipamentoController(id_status:int):

    for item in status_equipamento:
        if item["id"] == id_status:
            status_equipamento.remove(item)
            return f"item {id_status} foi removido com sucesso"