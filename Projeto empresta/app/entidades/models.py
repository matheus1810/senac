from pydantic import BaseModel
from sqlmodel import SQLModel,Field

class EquipamentoEntrada(BaseModel):
    nome: str
    status_id : int


class EquipamentoStatus(BaseModel):
    status: str
    
class StatusEquipamentoTabela(SQLModel,table=True):
    __tablename__ = "status_equipamentos"
    status : str
    id : int | None = Field(default=None, primary_key=True)