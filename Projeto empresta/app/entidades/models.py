from pydantic import BaseModel

class EquipamentoEntrada(BaseModel):
    nome: str
    status_id : int


class EquipamentoStatus(BaseModel):
    status: str