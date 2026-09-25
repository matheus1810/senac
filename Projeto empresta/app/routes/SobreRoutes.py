from fastapi import APIRouter

SobreRouter = APIRouter()

@SobreRouter.get("/sobre")
def apresentacao():
    return{
        "Nome do Projeto" : "Empresta",
        "Descrição" : "Sistema completo para gerenciamento de empréstimo de equipamentos"
    }