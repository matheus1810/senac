# Como encontrar as funcionalidades do JavaScript

O `app.js` é o ponto de entrada. Ele confere a sessão e escolhe a função da página
atual. A lista `paginas`, dentro dele, relaciona cada HTML à sua funcionalidade.

| Arquivo | Responsabilidade | Por onde começar |
| --- | --- | --- |
| `app.js` | Inicialização e escolha da página | `iniciarAplicacao()` |
| `autenticacao.js` | Formulário e envio do login com e-mail e senha | `exibirLogin()` |
| `sessao.js` | Token, saída, permissões por perfil e menu lateral | `PAGINAS_POR_PERFIL`, `montarNavegacao()` |
| `equipamentos.js` | Listagem, seleção, cadastro e edição de equipamentos | `exibirEquipamentos()`, `exibirFormularioEquipamento()` |
| `carrinho.js` | IDs dos equipamentos selecionados na sessão da aba | `alternarSelecao()`, `obterCarrinho()` |
| `solicitacoes.js` | Envio, listagem, detalhes, aprovação e rejeição | `exibirConfirmacaoSolicitacao()`, `exibirDetalheSolicitacao()` |
| `emprestimos.js` | Listagem dos empréstimos e registro da devolução | `exibirEmprestimos()`, `exibirFormularioDevolucao()` |
| `usuarios.js` | Listagem e cadastro de usuários | `exibirUsuarios()`, `exibirFormularioUsuario()` |
| `cadastros.js` | Consulta dos almoxarifados, papéis e status | `exibirCadastroApoio()` |
| `api.js` | Requisições HTTP, Bearer e erros retornados pela API | `requisitar()`, `enviar()` |
| `interface.js` | Montagem de HTML, mensagens e envio de formulários | `exibirTela()`, `configurarFormulario()` |

## Fluxo de uma página

1. O HTML carrega `app.js` com `type="module"`.
2. `iniciarAplicacao()` identifica o HTML e consulta `/auth/me` nas páginas privadas.
3. `sessao.js` confere o perfil e monta o menu.
4. A função da página consulta a API e prepara os dados e as linhas da tabela.
5. `interface.js` monta os campos, tabelas e mensagens.
6. Os eventos dos botões e formulários ficam junto da funcionalidade correspondente.

Exemplo: para mudar a aprovação de uma solicitação, abra `solicitacoes.js` e procure
`configurarAnaliseSolicitacao()`. Para mudar o endereço HTTP do login, veja
`autenticacao.js`. Para alterar quais páginas um gestor pode abrir, veja
`PAGINAS_POR_PERFIL` em `sessao.js` (o backend também verifica as permissões).

## Convenções para continuar o projeto

- Funções e variáveis usam nomes em português: `exibirEmprestimos`, `equipamentoId`.
- Campos enviados à API mantêm os nomes do backend, como `role_id` e `numero_serie`.
- `exibir...` prepara uma tela; `configurar...` conecta eventos a botões/formulários.
- Consultas HTTP passam por `api.js`. Cada funcionalidade conhece suas próprias rotas.
- Conteúdo vindo do servidor passa por `escaparHtml()` ou `montarCelula()` antes de
  entrar em HTML. Mensagens e nomes do perfil usam `textContent`.
- Dados de sessão mantêm as chaves `token` e `cart`, como na versão anterior.
- Não há variáveis globais de usuário. As funções que dependem do perfil recebem
  o objeto `usuario` como argumento.

Os módulos são nativos do navegador: não exigem npm, bundler ou instalação extra.
Abra as telas pelo FastAPI (`http://127.0.0.1:8001/`, se iniciado nessa porta),
pois imports de módulos precisam de um servidor HTTP. Não abra os HTMLs por `file://`.

Para verificar os fluxos existentes, dentro de `Projeto empresta`:

```bash
./.venv/Scripts/python.exe -m unittest discover -s tests -v
./.venv/Scripts/python.exe -B tests/browser_smoke.py
```

O segundo comando usa o Edge em modo invisível e um banco em memória, sem alterar
o banco de dados da aplicação.
