from pydantic import BaseModel
from sqlmodel import SQLModel,Field
from datetime import date, datetime
from pydantic import Field as PydanticField
from sqlalchemy import DateTime
from decimal import Decimal
from typing import Literal
from sqlalchemy import Column, Enum, Numeric

class EquipamentoEntrada(BaseModel):
    nome: str = PydanticField(min_length=1, max_length=255)
    valor: Decimal = PydanticField(ge=0, max_digits=8, decimal_places=2)
    numero_serie: str = PydanticField(min_length=1, max_length=255)
    status_id: int = PydanticField(gt=0)
    id_almoxarifado: int = PydanticField(gt=0)


class EquipamentoStatus(BaseModel):
    status: str = PydanticField(min_length=1, max_length=255)
    
class StatusEquipamentoTabela(SQLModel,table=True):
    __tablename__ = "status_equipamentos"
    status: str = Field(max_length=255)
    id : int | None = Field(default=None, primary_key=True)


class UsuarioEntrada(BaseModel):
    role_id: int = PydanticField(gt=0)
    nome: str = PydanticField(min_length=1, max_length=255)
    data_nascimento: date
    email: str = PydanticField(min_length=1, max_length=255)
    senha: str = PydanticField(min_length=1, max_length=255)
    cpf: str = PydanticField(min_length=1, max_length=255)


class UsuarioSaida(BaseModel):
    id: int
    role_id: int
    nome: str
    data_nascimento: date
    email: str
    cpf: str
    data_cad: datetime


class PapelTabela(SQLModel, table=True):
    __tablename__ = "papeis"
    id: int | None = Field(default=None, primary_key=True)
    responsabilidade: str = Field(max_length=255)


class UsuarioTabela(SQLModel, table=True):
    __tablename__ = "usuario"
    id: int | None = Field(default=None, primary_key=True)
    role_id: int = Field(foreign_key="papeis.id", index=True)
    nome: str = Field(max_length=255)
    data_nascimento: date
    email: str = Field(max_length=255, unique=True)
    senha: str = Field(max_length=255)
    cpf: str = Field(max_length=255, unique=True)
    data_cad: datetime = Field(default_factory=datetime.now, sa_type=DateTime)


class AlmoxarifadoTabela(SQLModel, table=True):
    __tablename__ = "almoxarifado"
    id: int | None = Field(default=None, primary_key=True)
    descricao: str = Field(max_length=255)


class EquipamentoTabela(SQLModel, table=True):
    __tablename__ = "equipamentos"
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=255)
    valor: Decimal = Field(sa_column=Column(Numeric(8, 2), nullable=False))
    numero_serie: str = Field(max_length=255)
    data_cad: datetime = Field(default_factory=datetime.now, sa_type=DateTime)
    status_id: int = Field(foreign_key="status_equipamentos.id")
    id_almoxarifado: int = Field(foreign_key="almoxarifado.id")


class SolicitacaoTabela(SQLModel, table=True):
    __tablename__ = "solicitacao"
    id: int | None = Field(default=None, primary_key=True)
    id_aluno: int = Field(foreign_key="usuario.id")
    data_solicitacao: datetime = Field(default_factory=datetime.now, sa_type=DateTime)


class ItemSolicitacaoTabela(SQLModel, table=True):
    __tablename__ = "item_solicitacao"
    id: int | None = Field(default=None, primary_key=True)
    id_solicitacao: int = Field(foreign_key="solicitacao.id")
    id_equipamento: int = Field(foreign_key="equipamentos.id")
    status: str = Field(default="analise", sa_column=Column(
        Enum("aprovado", "negado", "analise"), nullable=False, server_default="analise"))


class EmprestimoTabela(SQLModel, table=True):
    __tablename__ = "emprestimos"
    id: int | None = Field(default=None, primary_key=True)
    item_solicitacao_id: int = Field(foreign_key="item_solicitacao.id", unique=True)
    data_emprestimo: datetime = Field(default_factory=datetime.now, sa_type=DateTime)
    data_devolucao: datetime | None = Field(default=None, sa_type=DateTime)
    observacoes: str = Field(default="", max_length=255)
    estado_na_devolucao: str | None = Field(default=None, max_length=255)


class SolicitacaoEntrada(BaseModel):
    equipamento_ids: list[int] = PydanticField(min_length=1)


class DevolucaoEntrada(BaseModel):
    estado_na_devolucao: Literal["Bom estado", "Com avarias", "Necessita manutenção"]
    observacoes: str = PydanticField(default="", max_length=255)


class LoginEntrada(BaseModel):
    email: str
    senha: str
