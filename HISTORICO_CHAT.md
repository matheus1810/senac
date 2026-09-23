# Índice do histórico — Projeto Empresta

Último salvamento solicitado pelo aluno: **22/09/2026**.

Este arquivo é o ponto rápido de retomada. O diálogo detalhado fica separado por
dia na pasta [historico](historico/). Ao retomar o estudo, leia este índice,
depois o arquivo diário mais recente e confira o código atual antes de avaliar.

## Arquivos por dia

- [15/09/2026](historico/2026-09-15.md) — definição do projeto, modelagem SQL,
  decisões sobre empréstimos e revisão dos tipos das chaves.
- [22/09/2026](historico/2026-09-22.md) — rotas FastAPI, parâmetros, busca em
  listas, CRUD em memória, geração de IDs, ambiente virtual e separação de
  rotas/controllers. Pendente: mover o modelo de entrada para `entidades`.

Novos registros devem ser acrescentados ao arquivo correspondente à data da
interação. Em um novo dia, crie outro arquivo no formato `AAAA-MM-DD.md` e
adicione seu link aqui. O histórico só é salvo quando o aluno pedir.

## Resumo para retomar

### Acordo de ensino

- A IA atua como professora: explica, pergunta, dá pistas graduais e revisa.
- O aluno decide e escreve o código; a IA não entrega a solução completa.
- O histórico é alterado somente quando o aluno pedir explicitamente.
- O material do professor serve como referência; a modelagem própria do Projeto
  Empresta orienta as entidades e regras da API.
- Antes de avaliar uma tentativa, confira o arquivo atual. O histórico descreve
  versões anteriores e não substitui essa leitura.

### Decisões de modelagem preservadas

- Uma solicitação pode ter vários itens.
- Cada equipamento solicitado gera seu próprio empréstimo.
- Nova retirada exige nova solicitação e novo item.
- Cada item pode ter zero ou um empréstimo.
- `emprestimos.item_solicitacao_id` permanece `NOT NULL UNIQUE`.
- As chaves primárias e estrangeiras foram padronizadas como `INT`.
- O SQL foi revisado por leitura, mas não executado em um banco.

### Progresso atual da API

- O aluno implementou e relatou testes bem-sucedidos de GET, POST, PUT e DELETE
  em memória, incluindo 404, atualização conferida pelo GET e exclusão.
- O POST usa o maior ID presente na lista + 1, calculado depois do laço.
  O aluno testou exclusão seguida de cadastro e relatou que, ao esvaziar a
  lista, os novos IDs começam em 1 e 2. IDs excluídos ainda podem ser reutilizados.
- `Projeto empresta/app/main.py` é o ponto de entrada atual. Contém `/`,
  `/saudacao`, POST, PUT, DELETE e a classe `EquipamentoEntrada(nome: str)`.
- `app/routes/SobreRoutes.py` define `SobreRouter` e `/sobre`.
- `app/routes/EquipamentoRoutes.py` define `EquipamentoRouter`, a listagem e
  a consulta por ID. Na consulta, chama o controller, verifica `resultado is
  None`, lança 404 ou retorna o equipamento. O aluno informou que testou.
- `app/controllers/EquipamentoController.py` contém a única lista compartilhada,
  `buscar_equipamentos()` e `buscar_equipamento_por_id(id_equipamento: int)`.
  A busca retorna o item ou `None` depois do laço.
- O `main.py` importa e registra os dois routers com `include_router` e ainda
  importa a lista do controller para as operações que não foram separadas.
- O aluno explicou que importar o router não basta: `include_router` registra
  suas rotas na aplicação.
- Ambiente virtual: `.venv`. A pasta `app` agora guarda código, não o ambiente.
  O aluno confirmou a execução após mover o `main.py`, orientada com
  `fastapi dev app/main.py` a partir de `Projeto empresta`.
- O material do professor está nesta cópia em `ProgramadorWebSenac_Backend/`,
  sem duplicação. O `main.py` do professor fica em `ProjetoBase/app/main.py`.
  Há caminhos antigos no `AGENTS.md`; conferir os arquivos, sem reorganizar Git.
- A IA verificou os arquivos por leitura; os testes da API foram relatados pelo
  aluno. A IA não executou API ou SQL. Os dados ainda desaparecem ao reiniciar.

### Regras de negócio confirmadas, ainda não implementadas

- Equipamento já usado em solicitação deve manter cadastro e ID para preservar
  o histórico; pode ser marcado como indisponível.
- Equipamento indisponível continua nas consultas, mas não pode entrar em novas
  solicitações. O aluno confirmou ambas as regras.
- O DELETE atual ainda remove fisicamente da lista. As regras acima são decisões
  para implementação futura, não comportamento já garantido.
- O SQL usa `equipamentos.status_id` ligado a `status_equipamentos`. Foi proposto
  representar os status em memória, mas o aluno priorizou a divisão de pastas.
  Esse exercício permanece pendente; nenhum status foi acrescentado ao código.

### Ponto exato de retomada

O aluno pediu para deixar a próxima etapa para amanhã e salvar o histórico.
As duas rotas GET de equipamentos já estão separadas e o 404 foi recuperado.

**Próximo desafio proposto, ainda não realizado:** criar
`Projeto empresta/app/entidades/models.py`, mover para ele a classe
`EquipamentoEntrada` e o import de `BaseModel`, e importar a classe no `main.py`.
Na conferência do salvamento, a pasta `entidades` ainda não existe e a classe
continua no `main.py`. Depois será trabalhada a separação do POST entre rota e
controller. Não executar essas mudanças pelo aluno.

**Última pergunta pendente:** “Como fica esse novo import no `main.py`?”
O aluno ainda não respondeu nem demonstrou essa alteração. Retomar pela tentativa
dele e pela verificação de que a API continua iniciando.

## Sincronização

Os arquivos de histórico acompanham o repositório somente quando incluídos em
commit e enviados por push. O aluno realiza essa sincronização quando desejar.

