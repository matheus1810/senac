# Índice do histórico — Projeto Empresta

Último salvamento solicitado pelo aluno: **25/09/2026**.

Este arquivo é o ponto rápido de retomada. O diálogo detalhado fica separado por
dia na pasta [historico](historico/). Ao retomar o estudo, leia este índice,
depois o arquivo diário mais recente e confira o código atual antes de avaliar.

## Arquivos por dia

- [15/09/2026](historico/2026-09-15.md) — definição do projeto, modelagem SQL,
  decisões sobre empréstimos e revisão dos tipos das chaves.
- [22/09/2026](historico/2026-09-22.md) — rotas FastAPI, parâmetros, busca em
  listas, CRUD em memória, geração de IDs, ambiente virtual e separação de
  rotas/controllers. A transferência do modelo era pendente naquele dia.
- [25/09/2026](historico/2026-09-25.md) — CRUD de status, erros de controller e
  listas, vínculo por `status_id` e validação de existência. Pendente: distinguir
  equipamento inexistente de status inexistente no PUT.

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

- `Projeto empresta/app/main.py` cria a aplicação e registra os dois routers.
  Os CRUDs de equipamentos e status estão separados entre rotas e controller.
- `app/entidades/models.py` contém `EquipamentoEntrada(nome: str, status_id: int)`
  e `EquipamentoStatus(status: str)`. A antiga transferência do modelo foi feita.
- O cadastro de equipamento valida a existência do status e guarda `status_id`.
  A rota retorna 201 no sucesso e 404 com mensagem de status quando recebe `None`.
  O aluno confirmou os testes de cadastro e consulta, incluindo status inválido.
- O PUT de equipamento valida o status, mas os dois motivos de falha retornam
  `None`. A rota sempre informa equipamento não encontrado. Esse é o problema atual.
- O PUT ainda altera apenas `nome`, sem guardar o novo `status_id`. Os dois
  equipamentos iniciais também ainda não têm esse campo. Trabalhar depois da
  distinção dos erros, sem resolver esses pontos pelo aluno.
- O aluno relatou testes de listagem, busca, cadastro, atualização e exclusão de
  status. Corrigiu chamada do controller errado (`AttributeError` em `.nome`),
  conflito de nomes da rota/controller e remoção na lista errada (`ValueError`).
- **Ressalva:** apesar do relato de 404 ao repetir DELETE de status, a rota salva
  retorna diretamente o controller, sem tratar `None`. Não considerar esse 404
  implementado. GET por ID e PUT de status têm 404, mas ainda dizem “Equipamento”.
- O POST usa maior ID atual + 1; IDs excluídos ainda podem ser reutilizados.
  Os dados estão em memória e desaparecem ao reiniciar.
- Ambiente virtual: `.venv`. Comando de execução usado: `fastapi dev app/main.py`
  dentro de `Projeto empresta`. Reiniciar resolveu a ausência da rota de status
  em `/docs`, segundo o aluno; a causa exata de carregamento não foi comprovada.
- A IA conferiu os arquivos por leitura. Os testes foram relatados pelo aluno;
  a IA não executou API ou SQL. Conferir caminhos atuais do material do professor.

### Regras de negócio confirmadas, ainda não implementadas

- Equipamento já usado em solicitação deve manter cadastro e ID para preservar
  o histórico; pode ser marcado como indisponível.
- Equipamento indisponível continua nas consultas, mas não pode entrar em novas
  solicitações. O aluno confirmou ambas as regras.
- O DELETE atual ainda remove fisicamente da lista. As regras acima são decisões
  para implementação futura, não comportamento já garantido.
- O vínculo por `status_id` agora existe no cadastro em memória. A exclusão de
  status ainda não verifica referências de equipamentos; essa regra não foi
  discutida nesta conversa. Não presumir integridade automática.

### Ponto exato de retomada

O aluno observou que o PUT devolve a mesma mensagem para equipamento inexistente
e status inexistente. Ambos os caminhos devolvem `None` no controller.

A IA propôs devolver uma tupla com resultado e motivo da falha, recebida na rota
como `resultado, erro = atualizarEquipamentoController(id_equipamento, dados)`.
Todos os caminhos precisariam devolver esse par; sucesso poderia usar erro `None`.
**É apenas uma proposta didática: ainda não foi implementada nem escolhida de
forma definitiva pelo aluno.** A IA reconheceu que a orientação anterior de usar
somente `None` era insuficiente para distinguir os motivos.

**Última pergunta pendente:** “Como você escreveria o retorno do caso ‘status não
encontrado’ usando esse par?”

O aluno respondeu que faria depois e pediu um novo arquivo de histórico de hoje.
Retomar pela tentativa dele, explicando a tupla se necessário. Não preencher os
retornos nem alterar a API pelo aluno. O diário de 25/09 contém os detalhes e os
limites das verificações.

## Sincronização

Os arquivos de histórico acompanham o repositório somente quando incluídos em
commit e enviados por push. O aluno realiza essa sincronização quando desejar.

