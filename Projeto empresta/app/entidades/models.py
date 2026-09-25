from pydantic import BaseModel

class EquipamentoEntrada(BaseModel):
    nome: str


class EquipamentoStatus(BaseModel):
    status: str