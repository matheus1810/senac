# Empresta

API FastAPI e interface HTML/CSS/JavaScript. As entidades seguem o arquivo
`drawSQL-mysql-export-2026-09-15.sql`: `usuario`, `papeis`, `almoxarifado`,
`equipamentos`, `status_equipamentos`, `solicitacao`, `item_solicitacao` e `emprestimos`.

| Perfil em `papeis.responsabilidade` | Operações |
| --- | --- |
| Aluno / Usuário comum | Solicitar equipamentos disponíveis; consultar suas solicitações e empréstimos |
| Gestor | Analisar, aprovar ou rejeitar solicitações; registrar devoluções |
| Administrador | Cadastrar e editar equipamentos; cadastrar usuários e atribuir um dos papéis |

As permissões são verificadas no servidor consultando o papel atual no banco.
O administrador não herda as operações do gestor ou do usuário comum.

## Executar no PowerShell

Execute a partir desta pasta (`Projeto empresta`):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Configure o `.env` usando `.env.example` como referência, preservando suas credenciais.
O banco MySQL informado em `db_name` precisa existir. Para gerar a chave JWT:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

O SQL original pode ser importado em um banco vazio. O comando abaixo também cria
as tabelas ausentes, prepara os papéis, os status e o almoxarifado inicial e solicita
os dados do primeiro administrador. Ele não apaga tabelas nem altera colunas existentes:

```powershell
.\.venv\Scripts\python.exe app\inicializar.py
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir app --reload
```

Acesse **http://127.0.0.1:8000/**. Abra as telas por esse endereço, para que interface
e API sejam servidas juntas. A documentação da API está em `/docs`.

Se os usuários existentes têm senhas em texto puro, converta-as explicitamente antes
de fazer login:

```powershell
.\.venv\Scripts\python.exe app\inicializar.py --migrar-senhas
```

As senhas novas são salvas como hash Argon2. Não há senha padrão ou cadastro público.
Depois do primeiro acesso, o administrador pode cadastrar contas de Aluno e Gestor
pela tela de usuários.

## Fluxo de uso

1. Administrador: cadastrar os usuários e os equipamentos com status Disponível.
2. Aluno: selecionar equipamentos, revisar e enviar a solicitação.
3. Gestor: abrir a solicitação e aprovar ou rejeitar. A aprovação cria um registro de
   empréstimo para cada item e muda o equipamento para Emprestado, em uma transação.
4. Gestor: abrir Empréstimos e registrar a devolução. Bom estado libera o equipamento;
   avarias ou necessidade de manutenção mudam seu status para Manutenção.

Datas de solicitação, empréstimo e devolução são registradas pelo servidor. Os dados
de finalidade da solicitação e prazo previsto não são coletados, pois não existem
no SQL original. Itens usam os estados `analise`, `aprovado` e `negado` do ENUM.
Equipamentos com empréstimo ativo não podem ser editados. A aprovação usa bloqueios
de linhas no MySQL para impedir empréstimos simultâneos do mesmo equipamento.

## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes usam SQLite em memória com chaves estrangeiras habilitadas e substituem a
dependência de banco da API. Não acessam o MySQL do `.env`. Cobrem permissões,
autenticação, privacidade dos registros, persistência, conflitos, aprovação atômica,
devoluções e validação dos campos. Os bloqueios concorrentes de linhas precisam de
verificação específica com MySQL; SQLite não implementa `SELECT FOR UPDATE`.

Para verificar as telas com Microsoft Edge instalado no Windows:

```powershell
.\.venv\Scripts\python.exe -B tests\browser_smoke.py
```

Esse teste abre o navegador em modo invisível com perfil temporário e percorre login
dos três perfis, cadastro, solicitação, aprovação e devolução. Também usa SQLite em
memória, com uma conexão por requisição para suportar as consultas paralelas da interface.
