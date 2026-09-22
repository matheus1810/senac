from fastapi import FastAPI

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)


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
    equipamento = [
       {
         "id" : 1,
         "nome" : 'Câmera'
       },
        {
         "id" : 2,
         "nome" : 'Câmera'
       },
    ]
    for item in equipamento:
        if item["id"] == id_equipamento:
            return item
        else:
            return "nada"

    return{
        "Equipamento" : item
    }