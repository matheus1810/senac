from datetime import datetime
import unicodedata

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.db import get_db
from dependencies.dependencies import get_current_user, require_roles, papel_usuario
from entidades.models import (UsuarioTabela, PapelTabela, AlmoxarifadoTabela,
    EquipamentoTabela, StatusEquipamentoTabela, SolicitacaoTabela, ItemSolicitacaoTabela,
    EmprestimoTabela, SolicitacaoEntrada, DevolucaoEntrada)
from controllers.EquipamentoController import equipamento_bloqueado

EmprestimoRouter = APIRouter(tags=["Emprestimos"], dependencies=[Depends(get_current_user)])


def normalizar(texto):
    return "".join(c for c in unicodedata.normalize("NFKD", texto.lower())
                   if not unicodedata.combining(c)).strip()


def status_por_nome(db, *nomes):
    for registro in db.exec(select(StatusEquipamentoTabela)).all():
        if normalizar(registro.status) in nomes:
            return registro
    raise HTTPException(409, "Cadastre o status de equipamento: " + nomes[0])


def validar_disponivel(equipamento, db):
    disponivel = status_por_nome(db, "disponivel")
    if equipamento.status_id != disponivel.id or equipamento_bloqueado(equipamento.id, db):
        raise HTTPException(409, "Equipamento indisponivel: " + equipamento.nome)


def detalhar_solicitacao(solicitacao, db):
    itens = db.exec(select(ItemSolicitacaoTabela).where(
        ItemSolicitacaoTabela.id_solicitacao == solicitacao.id)).all()
    usuario = db.get(UsuarioTabela, solicitacao.id_aluno)
    return {**solicitacao.model_dump(), "solicitante": usuario.nome,
            "itens": [{**item.model_dump(), "equipamento": db.get(
                EquipamentoTabela, item.id_equipamento).nome} for item in itens]}


@EmprestimoRouter.get("/papeis", dependencies=[Depends(require_roles("administrador"))])
def papeis(db: Session = Depends(get_db)):
    return db.exec(select(PapelTabela)).all()


@EmprestimoRouter.get("/almoxarifados")
def almoxarifados(db: Session = Depends(get_db)):
    return db.exec(select(AlmoxarifadoTabela)).all()


@EmprestimoRouter.post("/solicitacoes", status_code=201)
def solicitar(dados: SolicitacaoEntrada, usuario: UsuarioTabela = Depends(require_roles("comum")),
              db: Session = Depends(get_db)):
    ids = sorted(set(dados.equipamento_ids))
    if len(ids) != len(dados.equipamento_ids):
        raise HTTPException(422, "Nao repita equipamentos na solicitacao")
    for id_equipamento in ids:
        equipamento = db.exec(select(EquipamentoTabela).where(
            EquipamentoTabela.id == id_equipamento).with_for_update()).first()
        if equipamento is None:
            raise HTTPException(404, "Equipamento nao encontrado")
        validar_disponivel(equipamento, db)
        pendente = db.exec(select(ItemSolicitacaoTabela).join(SolicitacaoTabela,
            ItemSolicitacaoTabela.id_solicitacao == SolicitacaoTabela.id).where(
                SolicitacaoTabela.id_aluno == usuario.id,
                ItemSolicitacaoTabela.id_equipamento == id_equipamento,
                ItemSolicitacaoTabela.status == "analise")).first()
        if pendente:
            raise HTTPException(409, "Voce ja solicitou este equipamento")
    solicitacao = SolicitacaoTabela(id_aluno=usuario.id)
    db.add(solicitacao)
    db.flush()
    for id_equipamento in ids:
        db.add(ItemSolicitacaoTabela(id_solicitacao=solicitacao.id, id_equipamento=id_equipamento))
    db.commit()
    db.refresh(solicitacao)
    return detalhar_solicitacao(solicitacao, db)


@EmprestimoRouter.get("/solicitacoes")
def solicitacoes(usuario: UsuarioTabela = Depends(require_roles("comum", "gestor")),
                 db: Session = Depends(get_db)):
    consulta = select(SolicitacaoTabela).order_by(SolicitacaoTabela.id.desc())
    if papel_usuario(usuario, db) == "comum":
        consulta = consulta.where(SolicitacaoTabela.id_aluno == usuario.id)
    return [detalhar_solicitacao(s, db) for s in db.exec(consulta).all()]


@EmprestimoRouter.get("/solicitacoes/{id_solicitacao}")
def solicitacao_por_id(id_solicitacao: int,
        usuario: UsuarioTabela = Depends(require_roles("comum", "gestor")),
        db: Session = Depends(get_db)):
    solicitacao = db.get(SolicitacaoTabela, id_solicitacao)
    if solicitacao is None or (papel_usuario(usuario, db) == "comum" and solicitacao.id_aluno != usuario.id):
        raise HTTPException(404, "Solicitacao nao encontrada")
    return detalhar_solicitacao(solicitacao, db)


@EmprestimoRouter.post("/solicitacoes/{id_solicitacao}/aprovar",
                       dependencies=[Depends(require_roles("gestor"))])
def aprovar(id_solicitacao: int, db: Session = Depends(get_db)):
    solicitacao = db.exec(select(SolicitacaoTabela).where(
        SolicitacaoTabela.id == id_solicitacao).with_for_update()).first()
    if solicitacao is None:
        raise HTTPException(404, "Solicitacao nao encontrada")
    itens = db.exec(select(ItemSolicitacaoTabela).where(
        ItemSolicitacaoTabela.id_solicitacao == id_solicitacao).order_by(
            ItemSolicitacaoTabela.id_equipamento)).all()
    if not itens or any(i.status != "analise" for i in itens):
        raise HTTPException(409, "Solicitacao ja analisada ou sem itens")
    emprestado = status_por_nome(db, "emprestado", "em emprestimo")
    equipamentos = []
    for item in itens:
        equipamento = db.exec(select(EquipamentoTabela).where(
            EquipamentoTabela.id == item.id_equipamento).with_for_update()).first()
        validar_disponivel(equipamento, db)
        equipamentos.append(equipamento)
    for item, equipamento in zip(itens, equipamentos):
        item.status = "aprovado"
        equipamento.status_id = emprestado.id
        db.add(item)
        db.add(equipamento)
        db.add(EmprestimoTabela(item_solicitacao_id=item.id))
    db.commit()
    return detalhar_solicitacao(solicitacao, db)


@EmprestimoRouter.post("/solicitacoes/{id_solicitacao}/negar",
                       dependencies=[Depends(require_roles("gestor"))])
def negar(id_solicitacao: int, db: Session = Depends(get_db)):
    solicitacao = db.exec(select(SolicitacaoTabela).where(
        SolicitacaoTabela.id == id_solicitacao).with_for_update()).first()
    if solicitacao is None:
        raise HTTPException(404, "Solicitacao nao encontrada")
    itens = db.exec(select(ItemSolicitacaoTabela).where(
        ItemSolicitacaoTabela.id_solicitacao == id_solicitacao)).all()
    if not itens or any(i.status != "analise" for i in itens):
        raise HTTPException(409, "Solicitacao ja analisada ou sem itens")
    for item in itens:
        item.status = "negado"
        db.add(item)
    db.commit()
    return detalhar_solicitacao(solicitacao, db)


@EmprestimoRouter.get("/emprestimos")
def emprestimos(usuario: UsuarioTabela = Depends(require_roles("comum", "gestor")),
                db: Session = Depends(get_db)):
    consulta = select(EmprestimoTabela, EquipamentoTabela, UsuarioTabela).join(
        ItemSolicitacaoTabela, EmprestimoTabela.item_solicitacao_id == ItemSolicitacaoTabela.id).join(
        EquipamentoTabela, ItemSolicitacaoTabela.id_equipamento == EquipamentoTabela.id).join(
        SolicitacaoTabela, ItemSolicitacaoTabela.id_solicitacao == SolicitacaoTabela.id).join(
        UsuarioTabela, SolicitacaoTabela.id_aluno == UsuarioTabela.id)
    if papel_usuario(usuario, db) == "comum":
        consulta = consulta.where(UsuarioTabela.id == usuario.id)
    return [{**e.model_dump(), "equipamento": eq.nome, "solicitante": u.nome}
            for e, eq, u in db.exec(consulta).all()]


@EmprestimoRouter.post("/emprestimos/{id_emprestimo}/devolver",
                       dependencies=[Depends(require_roles("gestor"))])
def devolver(id_emprestimo: int, dados: DevolucaoEntrada, db: Session = Depends(get_db)):
    emprestimo = db.exec(select(EmprestimoTabela).where(
        EmprestimoTabela.id == id_emprestimo).with_for_update()).first()
    if emprestimo is None:
        raise HTTPException(404, "Emprestimo nao encontrado")
    if emprestimo.data_devolucao is not None:
        raise HTTPException(409, "Devolucao ja registrada")
    item = db.get(ItemSolicitacaoTabela, emprestimo.item_solicitacao_id)
    equipamento = db.exec(select(EquipamentoTabela).where(
        EquipamentoTabela.id == item.id_equipamento).with_for_update()).first()
    status = (status_por_nome(db, "disponivel") if dados.estado_na_devolucao == "Bom estado"
              else status_por_nome(db, "manutencao", "manutancao"))
    equipamento.status_id = status.id
    emprestimo.data_devolucao = datetime.now()
    emprestimo.estado_na_devolucao = dados.estado_na_devolucao
    emprestimo.observacoes = dados.observacoes
    db.add(equipamento)
    db.add(emprestimo)
    db.commit()
    db.refresh(emprestimo)
    return emprestimo
