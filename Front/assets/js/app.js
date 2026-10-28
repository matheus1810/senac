// Ponto de entrada de todas as páginas. As funcionalidades ficam nos módulos abaixo.
import { requisitar } from "./api.js";
import { exibirLogin } from "./autenticacao.js";
import { exibirCadastroApoio } from "./cadastros.js";
import { exibirEquipamentos, exibirFormularioEquipamento } from "./equipamentos.js";
import { exibirEmprestimos, exibirFormularioDevolucao } from "./emprestimos.js";
import { escaparHtml, exibirMensagem, exibirTela } from "./interface.js";
import {
    encerrarSessao, montarNavegacao, paginaInicial, paginaPublica,
    perfilReconhecido, podeAcessarPagina, possuiToken
} from "./sessao.js";
import {
    exibirConfirmacaoSolicitacao, exibirDetalheSolicitacao, exibirSolicitacoes
} from "./solicitacoes.js";
import { exibirFormularioUsuario, exibirUsuarios } from "./usuarios.js";

async function iniciarAplicacao() {
    const paginaAtual = location.pathname.split("/").pop() || "index.html";
    if (paginaPublica(paginaAtual)) {
        exibirLogin();
        return;
    }
    if (!possuiToken()) {
        location.replace("login.html");
        return;
    }

    const usuario = await requisitar("/auth/me");
    if (!perfilReconhecido(usuario)) {
        encerrarSessao();
        return;
    }
    if (!podeAcessarPagina(usuario, paginaAtual)) {
        location.replace(paginaInicial(usuario));
        return;
    }
    montarNavegacao(usuario, paginaAtual);

    // Para encontrar o código de uma tela, procure seu arquivo HTML nesta lista.
    const paginas = {
        "equipamentos.html": () => exibirEquipamentos(),
        "usuario_solicitar_equipamento.html": () => exibirEquipamentos(true),
        "equipamento_form.html": exibirFormularioEquipamento,
        "usuario_confirmar_solicitacao.html": exibirConfirmacaoSolicitacao,
        "solicitacoes.html": () => exibirSolicitacoes(usuario),
        "usuario_minhas_solicitacoes.html": () => exibirSolicitacoes(usuario),
        "solicitacao_detalhe.html": () => exibirDetalheSolicitacao(usuario),
        "emprestimos.html": () => exibirEmprestimos(usuario),
        "usuario_meus_emprestimos.html": () => exibirEmprestimos(usuario),
        "devolucao.html": () => exibirFormularioDevolucao(usuario),
        "usuarios.html": exibirUsuarios,
        "usuario_form.html": exibirFormularioUsuario,
        "almoxarifados.html": () => exibirCadastroApoio(paginaAtual),
        "papeis.html": () => exibirCadastroApoio(paginaAtual),
        "status_equipamentos.html": () => exibirCadastroApoio(paginaAtual)
    };
    if (Object.hasOwn(paginas, paginaAtual)) {
        await paginas[paginaAtual]();
    } else {
        exibirTela("Início", `
            <section class="card">
                <h2>Olá, ${escaparHtml(usuario.nome)}</h2>
                <p>Use o menu para acessar as operações do perfil ${escaparHtml(usuario.papel)}.</p>
            </section>`);
    }
}

iniciarAplicacao().catch(erro => exibirMensagem(erro.message));
