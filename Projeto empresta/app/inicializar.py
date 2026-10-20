"""Preparação explícita do banco e do primeiro administrador; nunca executada ao iniciar a API."""
import argparse
from datetime import date
from getpass import getpass

from sqlmodel import SQLModel, Session, select
from db.db import engine
from entidades.models import PapelTabela, StatusEquipamentoTabela, AlmoxarifadoTabela, UsuarioTabela
from core.security import cria_hash_senha, pwd_context


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--migrar-senhas", action="store_true",
                        help="Converte senhas legadas em texto puro para Argon2")
    args = parser.parse_args()
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        for nome in ("Aluno", "Gestor", "Administrador"):
            if not db.exec(select(PapelTabela).where(PapelTabela.responsabilidade == nome)).first():
                db.add(PapelTabela(responsabilidade=nome))
        for nome in ("Disponível", "Emprestado", "Manutenção", "Indisponível"):
            if not db.exec(select(StatusEquipamentoTabela).where(StatusEquipamentoTabela.status == nome)).first():
                db.add(StatusEquipamentoTabela(status=nome))
        if not db.exec(select(AlmoxarifadoTabela)).first():
            db.add(AlmoxarifadoTabela(descricao="Central"))
        db.commit()
        if args.migrar_senhas:
            for usuario in db.exec(select(UsuarioTabela)).all():
                if pwd_context.identify(usuario.senha) is None:
                    usuario.senha = cria_hash_senha(usuario.senha)
                    db.add(usuario)
            db.commit()
            print("Senhas legadas convertidas.")
        papel = db.exec(select(PapelTabela).where(PapelTabela.responsabilidade == "Administrador")).first()
        if db.exec(select(UsuarioTabela).where(UsuarioTabela.role_id == papel.id)).first():
            print("Banco preparado. Ja existe um administrador.")
            return
        print("Cadastre o primeiro administrador:")
        nome = input("Nome: ").strip()
        email = input("E-mail: ").strip()
        cpf = input("CPF: ").strip()
        nascimento = date.fromisoformat(input("Nascimento (AAAA-MM-DD): ").strip())
        senha = getpass("Senha: ")
        if not nome or not email or not cpf or not senha or senha != getpass("Repita a senha: "):
            raise SystemExit("Dados invalidos ou senhas diferentes. Administrador nao cadastrado.")
        if db.exec(select(UsuarioTabela).where(
                (UsuarioTabela.email == email) | (UsuarioTabela.cpf == cpf))).first():
            raise SystemExit("E-mail ou CPF ja cadastrado. Use outro ou ajuste o papel do usuario existente.")
        db.add(UsuarioTabela(role_id=papel.id, nome=nome, email=email, cpf=cpf,
                            data_nascimento=nascimento, senha=cria_hash_senha(senha)))
        db.commit()
        print("Administrador cadastrado.")


if __name__ == "__main__":
    main()
