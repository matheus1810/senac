import { selecionar } from "./interface.js";

// O backend também valida os papéis. Esta lista organiza a navegação da interface.
const PAGINAS_POR_PERFIL = {
    comum: [
        "usuario_dashboard.html",
        "usuario_solicitar_equipamento.html",
        "usuario_confirmar_solicitacao.html",
        "usuario_minhas_solicitacoes.html",
        "usuario_meus_emprestimos.html",
        "solicitacao_detalhe.html"
    ],
    gestor: [
        "dashboard.html", "solicitacoes.html", "solicitacao_detalhe.html",
        "emprestimos.html", "devolucao.html"
    ],
    administrador: [
        "dashboard.html", "equipamentos.html", "equipamento_form.html",
        "usuarios.html", "usuario_form.html", "papeis.html",
        "status_equipamentos.html", "almoxarifados.html"
    ]
};

const LINKS_POR_PERFIL = {
    comum: [
        ["usuario_solicitar_equipamento.html", "Solicitar equipamentos"],
        ["usuario_minhas_solicitacoes.html", "Minhas solicitações"],
        ["usuario_meus_emprestimos.html", "Meus empréstimos"]
    ],
    gestor: [
        ["solicitacoes.html", "Solicitações"],
        ["emprestimos.html", "Empréstimos"]
    ],
    administrador: [
        ["equipamentos.html", "Equipamentos"],
        ["usuarios.html", "Usuários"],
        ["almoxarifados.html", "Almoxarifados"],
        ["status_equipamentos.html", "Status"],
        ["papeis.html", "Papéis"]
    ]
};

export function paginaPublica(pagina) {
    return ["login.html", "index.html"].includes(pagina);
}

export function possuiToken() {
    return Boolean(sessionStorage.getItem("token"));
}

export function salvarToken(token) {
    sessionStorage.setItem("token", token);
}

export function limparSessao() {
    sessionStorage.clear();
}

export function encerrarSessao() {
    limparSessao();
    location.replace("login.html");
}

export function paginaInicial(usuario) {
    return usuario.papel === "comum" ? "usuario_dashboard.html" : "dashboard.html";
}

export function perfilReconhecido(usuario) {
    return Object.hasOwn(PAGINAS_POR_PERFIL, usuario.papel);
}

export function podeAcessarPagina(usuario, pagina) {
    return PAGINAS_POR_PERFIL[usuario.papel]?.includes(pagina) || false;
}

export function montarNavegacao(usuario, paginaAtual) {
    const links = [[paginaInicial(usuario), "Início"], ...LINKS_POR_PERFIL[usuario.papel]];
    selecionar(".sidebar nav").innerHTML = links.map(([endereco, rotulo]) => `
        <a class="nav-link ${endereco === paginaAtual ? "ativo" : ""}" href="${endereco}">${rotulo}</a>`
    ).join("");
    selecionar(".sidebar-footer").innerHTML =
        '<button type="button" class="nav-link" id="sair">Sair</button>';
    selecionar("#sair").onclick = encerrarSessao;
    selecionar(".perfil").textContent = `${usuario.nome} · ${usuario.papel}`;
}
