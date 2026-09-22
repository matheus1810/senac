from fastapi import FastAPI,status, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)

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


@app.get("/")
def root():
    return {"mensagem": "Olá, FastAPI!"}

@app.get("/saudacao")
def saudacao(nome = "Visitante"):
    return{
        "Message" : f"Olá: {nome}"
    }

@app.get("/sobre")
def apresentacao():
    return{
        "Nome do Projeto" : "Empresta",
        "Descrição" : "Sistema completo para gerenciamento de empréstimo de equipamentos"
    }

@app.get("/equipamento/{id_equipamento}")
def retorna_equipamento(id_equipamento : int):
   
    for item in equipamentos:
            if item["id"] == id_equipamento:
                return item
        
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail = f'Equipamento {id_equipamento} não foi encontrado'
    )



@app.get('/equipamentos')
def get_equipamentos():
    return equipamentos
    



class EquipamentoEntrada(BaseModel):
    nome: str
    


@app.post("/equipamentos",status_code=status.HTTP_201_CREATED)
def cadastraEquipamento(equipamento : EquipamentoEntrada):
    
    novo_id = len(equipamentos) + 1
    
    novo_equipamento = {
        "id": novo_id,
        "nome":equipamento.nome
    }
    
    equipamentos.append(novo_equipamento)
    return novo_equipamento

@app.put("/equipamento/{id_equipamento}")
def atualizarEquipamento(id_equipamento:int, dados:EquipamentoEntrada):
     
        for item in equipamentos:
                    if item["id"] == id_equipamento:
                        item["nome"] = dados.nome
                        return item
            
        # raise HTTPException(
        #     status.HTTP_404_NOT_FOUND,
        #     detail = f'Equipamento {id_equipamento} não foi encontrado'
        # )