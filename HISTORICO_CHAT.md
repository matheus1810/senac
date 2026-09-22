# Índice do histórico — Projeto Empresta

Último salvamento solicitado pelo aluno: **22/09/2026**.

Este arquivo é o ponto rápido de retomada. O diálogo detalhado fica separado por
dia na pasta [historico](historico/). Ao retomar o estudo, leia este índice,
depois o arquivo diário mais recente e confira o código atual antes de avaliar.

## Arquivos por dia

- [15/09/2026](historico/2026-09-15.md) — definição do projeto, modelagem SQL,
  decisões sobre empréstimos e revisão dos tipos das chaves.
- [22/09/2026](historico/2026-09-22.md) — rotas FastAPI, parâmetros, busca em
  listas, respostas 404, listagem, cadastro POST e início da atualização PUT.

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

O aluno implementou e informou sucesso nos testes de:

- parâmetro de consulta em `GET /saudacao`, com valor padrão;
- `GET /sobre`;
- `GET /equipamentos`, usando uma lista compartilhada em memória;
- `GET /equipamento/{id_equipamento}`, com validação de inteiro e erro 404;
- modelo Pydantic `EquipamentoEntrada`, atualmente com `nome: str`;
- `POST /equipamentos`, com geração simples de ID, inclusão na lista, retorno
  do registro criado e código `201 Created`;
- validação 422 quando o corpo obrigatório não é enviado.

O aluno compreendeu que os registros em memória desaparecem quando a API
reinicia, pois ainda não há persistência em banco.

### Ponto exato de retomada

O aluno começou `PUT /equipamento/{id_equipamento}`. Na versão conferida de
`Projeto empresta/main.py`, a função:

- recebe o ID pelo caminho e `dados: EquipamentoEntrada` pelo corpo;
- percorre a lista;
- altera `item["nome"]` e retorna o item quando encontra o ID;
- possui o tratamento 404 apenas comentado;
- ainda não foi registrado como testado.

Próximo desafio: ativar o 404 depois do `for` e testar um ID existente e um
inexistente. Não entregar a função completa; retomar pela tentativa do aluno.

A expressão `len(equipamentos) + 1` atende ao exercício atual, mas poderá
repetir IDs quando houver exclusão. Tratar isso na etapa de DELETE.

## Sincronização

Os arquivos de histórico acompanham o repositório somente quando incluídos em
commit e enviados por push. O aluno realiza essa sincronização quando desejar.

