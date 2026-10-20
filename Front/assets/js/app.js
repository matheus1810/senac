/* A interface e a API são servidas pela mesma aplicação em /ui. */
"use strict";
const $ = (s) => document.querySelector(s);
const escapeHTML = (v) => String(v ?? "")
    .replace(/[&<>"']/g, c => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    } [c]));
const page = location.pathname.split("/")
    .pop() || "index.html";
let user;
let cart = [];
try {
    cart = JSON.parse(sessionStorage.getItem("cart") || "[]");
} catch {
    /* carrinho vazio */
}
if (!Array.isArray(cart)) cart = [];
const saveCart = () => sessionStorage.setItem("cart", JSON.stringify(cart));

async function api(path, options = {}) {
    const token = sessionStorage.getItem("token");
    const response = await fetch(path, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token ? {
                Authorization: `Bearer ${token}`
            } : {}),
            ...options.headers
        }
    });
    const data = await response.json()
        .catch(() => ({}));
    if (!response.ok) {
        if (response.status === 401 && !["login.html", "index.html"].includes(page)) {
            sessionStorage.clear();
            location.replace("login.html");
        }
        throw new Error(typeof data.detail === "string" ? data.detail :
            "Confira os campos informados.");
    }
    return data;
}
const post = (path, body) => api(path, {
    method: "POST",
    body: JSON.stringify(body)
});

function message(text) {
    let box = $("#mensagem");
    if (!box) {
        box = document.createElement("p");
        box.id = "mensagem";
        box.setAttribute("role", "alert");
        ($("main") || document.body)
        .prepend(box);
    }
    box.textContent = text;
}

function formAction(form, action) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const button = form.querySelector('[type="submit"]');
        if (button) button.disabled = true;
        try {
            await action(new FormData(form));
        } catch (error) {
            message(error.message);
        } finally {
            if (button) button.disabled = false;
        }
    });
}

function table(headers, rows) {
    return `<div class="tabela-container"><table><thead><tr>${headers.map(h => `<th>${h}</th>`).join("")}</tr></thead>
        <tbody>${rows.length ? rows.join("") : `<tr><td colspan="${headers.length}">Nenhum registro encontrado.</td></tr>`}</tbody></table></div>`;
}
const td = value => `<td>${escapeHTML(value)}</td>`;
const options = (rows, label) => rows.map(r =>
        `<option value="${r.id}">${escapeHTML(r[label])}</option>`)
    .join("");
const field = (name, label, type = "text", extra = "") =>
    `<div class="campo"><label for="${name}">${label}</label><input id="${name}" name="${name}" type="${type}" required ${extra}></div>`;

function screen(title, content) {
    $("h1")
        .textContent = title;
    $("#conteudo")
        .innerHTML = content;
}

function home() {
    return user.papel === "comum" ? "usuario_dashboard.html" : "dashboard.html";
}

function navigation() {
    const links = user.papel === "comum" ? [
        ["usuario_solicitar_equipamento.html", "Solicitar equipamentos"],
        ["usuario_minhas_solicitacoes.html", "Minhas solicitações"],
        ["usuario_meus_emprestimos.html", "Meus empréstimos"]
    ] : user.papel === "gestor" ? [
        ["solicitacoes.html", "Solicitações"],
        ["emprestimos.html", "Empréstimos"]
    ] : [
        ["equipamentos.html", "Equipamentos"],
        ["usuarios.html", "Usuários"],
        ["almoxarifados.html", "Almoxarifados"],
        ["status_equipamentos.html", "Status"],
        ["papeis.html", "Papéis"]
    ];
    $(".sidebar nav")
        .innerHTML = [
            [home(), "Início"], ...links
        ].map(([url, label]) =>
            `<a class="nav-link ${url === page ? "ativo" : ""}" href="${url}">${label}</a>`)
        .join("");
    $(".sidebar-footer")
        .innerHTML = '<button type="button" class="nav-link" id="sair">Sair</button>';
    $("#sair")
        .onclick = () => {
            sessionStorage.clear();
            location.replace("login.html");
        };
    $(".perfil")
        .textContent = `${user.nome} · ${user.papel}`;
}
async function login() {
    const main = $("main");
    main.innerHTML = `<header><h1>Gestão de Equipamentos</h1><p>Acesso ao sistema</p></header>
        <form>${field("email", "E-mail", "email", 'autocomplete="username"')}
        ${field("senha", "Senha", "password", 'autocomplete="current-password"')}
        <button type="submit" class="botao primario">Entrar</button></form>`;
    formAction($("form"), async data => {
        sessionStorage.clear();
        const token = await post("/login", Object.fromEntries(data));
        sessionStorage.setItem("token", token.access_token);
        user = await api("/auth/me");
        location.assign(home());
    });
}
async function equipments(selectable = false) {
    const [rows, statuses, warehouses] = await Promise.all([api("/equipamentos"), api(
        "/status-equipamento"), api("/almoxarifados")]);
    const status = id => statuses.find(s => s.id === id)
        ?.status || "";
    const available = id => status(id)
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim() === "disponivel";
    screen(selectable ? "Solicitar equipamentos" : "Equipamentos", `<div class="acoes">${selectable ?
        '<a class="botao primario" href="usuario_confirmar_solicitacao.html">Revisar solicitação</a>' :
        '<a class="botao primario" href="equipamento_form.html">Novo equipamento</a>'}</div>` +
        table(["Nome", "Série", "Status", "Almoxarifado", "Ação"], rows.map(eq => `<tr>${td(eq.nome)}${td(eq.numero_serie)}${td(status(eq.status_id))}
        ${td(warehouses.find(w => w.id === eq.id_almoxarifado)?.descricao)}<td>${selectable ?
            (available(eq.status_id) ? `<button class="botao" data-add="${eq.id}">${cart.includes(eq.id) ? "Remover" : "Selecionar"}</button>` : "Indisponível") :
            `<a href="equipamento_form.html?id=${eq.id}">Editar</a>`}</td></tr>`)));
    document.querySelectorAll("[data-add]")
        .forEach(button => button.onclick = () => {
            const id = Number(button.dataset.add);
            cart = cart.includes(id) ? cart.filter(v => v !== id) : [...cart, id];
            saveCart();
            button.textContent = cart.includes(id) ? "Remover" : "Selecionar";
        });
}
async function equipmentForm() {
    const [statuses, warehouses] = await Promise.all([api("/status-equipamento"), api(
        "/almoxarifados")]);
    const id = new URLSearchParams(location.search)
        .get("id");
    screen(id ? "Editar equipamento" : "Novo equipamento", `<form class="card form-card"><div class="form-grid">
        ${field("nome", "Nome", "text", 'maxlength="255"')}${field("numero_serie", "Número de série", "text", 'maxlength="255"')}
        ${field("valor", "Valor", "number", 'min="0" max="999999.99" step="0.01"')}
        <div class="campo"><label for="status_id">Status</label><select id="status_id" name="status_id" required>${options(statuses, "status")}</select></div>
        <div class="campo"><label for="id_almoxarifado">Almoxarifado</label><select id="id_almoxarifado" name="id_almoxarifado" required>${options(warehouses, "descricao")}</select></div>
        </div><button type="submit" class="botao primario">Salvar</button></form>`);
    if (id) {
        const eq = await api(`/equipamento/${encodeURIComponent(id)}`);
        for (const key of ["nome", "numero_serie", "valor", "status_id", "id_almoxarifado"]) $(
                `[name="${key}"]`)
            .value = eq[key];
    }
    formAction($("form"), async data => {
        const body = Object.fromEntries(data);
        body.status_id = Number(body.status_id);
        body.id_almoxarifado = Number(body.id_almoxarifado);
        await api(id ? `/equipamento/${encodeURIComponent(id)}` : "/equipamentos", {
            method: id ? "PUT" : "POST",
            body: JSON.stringify(body)
        });
        location.assign("equipamentos.html");
    });
}
async function confirmRequest() {
    const rows = (await api("/equipamentos"))
        .filter(eq => cart.includes(eq.id));
    screen("Confirmar solicitação", table(["Equipamento", "Série"], rows.map(eq =>
            `<tr>${td(eq.nome)}${td(eq.numero_serie)}</tr>`)) +
        `<form><button type="submit" class="botao primario" ${rows.length ? "" : "disabled"}>Enviar solicitação</button></form>`
    );
    formAction($("form"), async () => {
        await post("/solicitacoes", {
            equipamento_ids: rows.map(eq => eq.id)
        });
        cart = [];
        saveCart();
        location.assign("usuario_minhas_solicitacoes.html");
    });
}
async function requests() {
    const rows = await api("/solicitacoes");
    screen(user.papel === "comum" ? "Minhas solicitações" : "Solicitações", table(["Número",
            "Solicitante", "Data", "Itens", "Ação"
        ],
        rows.map(s =>
            `<tr>${td(s.id)}${td(s.solicitante)}${td(new Date(s.data_solicitacao).toLocaleString("pt-BR"))}
        ${td(s.itens.map(i => `${i.equipamento}: ${i.status}`).join(", "))}<td><a href="solicitacao_detalhe.html?id=${s.id}">Ver detalhes</a></td></tr>`
        )));
}
async function requestDetail() {
    const id = new URLSearchParams(location.search)
        .get("id");
    if (!id) {
        await requests();
        return;
    }
    const s = await api(`/solicitacoes/${encodeURIComponent(id)}`);
    screen(`Solicitação #${s.id}`,
        `<section class="card"><p>Solicitante: ${escapeHTML(s.solicitante)}</p></section>` +
        table(["Equipamento", "Status"], s.itens.map(i =>
            `<tr>${td(i.equipamento)}${td(i.status)}</tr>`)) +
        (user.papel === "gestor" && s.itens.every(i => i.status === "analise") ?
            '<div class="acoes"><button class="botao" data-decision="negar">Rejeitar</button><button class="botao primario" data-decision="aprovar">Aprovar</button></div>' :
            ""));
    document.querySelectorAll("[data-decision]")
        .forEach(button => button.onclick = async () => {
            button.disabled = true;
            try {
                await post(`/solicitacoes/${s.id}/${button.dataset.decision}`);
                await requestDetail();
            } catch (error) {
                message(error.message);
                button.disabled = false;
            }
        });
}
async function loans() {
    const rows = await api("/emprestimos");
    screen(user.papel === "comum" ? "Meus empréstimos" : "Empréstimos", table(["Número",
            "Equipamento", "Solicitante", "Empréstimo", "Devolução", "Ação"
        ],
        rows.map(e =>
            `<tr>${td(e.id)}${td(e.equipamento)}${td(e.solicitante)}${td(new Date(e.data_emprestimo).toLocaleString("pt-BR"))}
        ${td(e.data_devolucao ? new Date(e.data_devolucao).toLocaleString("pt-BR") : "Em aberto")}<td>${user.papel === "gestor" && !e.data_devolucao ?
            `<a href="devolucao.html?id=${e.id}">Registrar devolução</a>` : escapeHTML(e.estado_na_devolucao)}</td></tr>`
        )));
}
async function returnForm() {
    const id = new URLSearchParams(location.search)
        .get("id");
    if (!id) {
        await loans();
        return;
    }
    const loan = (await api("/emprestimos"))
        .find(e => String(e.id) === id);
    if (!loan || loan.data_devolucao) throw new Error(
        "Empréstimo não encontrado ou já devolvido.");
    screen(`Devolução #${loan.id}`,
        `<section class="card"><p>${escapeHTML(loan.equipamento)} · ${escapeHTML(loan.solicitante)}</p>
        <form><div class="campo"><label for="estado_na_devolucao">Estado na devolução</label><select id="estado_na_devolucao" name="estado_na_devolucao">
        <option>Bom estado</option><option>Com avarias</option><option>Necessita manutenção</option></select></div>
        <div class="campo"><label for="observacoes">Observações</label><textarea id="observacoes" name="observacoes" maxlength="255"></textarea></div>
        <button type="submit" class="botao primario">Confirmar devolução</button></form></section>`
    );
    formAction($("form"), async data => {
        await post(`/emprestimos/${loan.id}/devolver`, Object.fromEntries(data));
        location.assign("emprestimos.html");
    });
}
async function users() {
    const rows = await api("/usuarios");
    screen("Usuários",
        '<div class="acoes"><a class="botao primario" href="usuario_form.html">Novo usuário</a></div>' +
        table(["Nome", "E-mail", "CPF"], rows.map(u =>
            `<tr>${td(u.nome)}${td(u.email)}${td(u.cpf)}</tr>`)));
}
async function userForm() {
    const roles = await api("/papeis");
    screen("Novo usuário", `<form class="card form-card"><div class="form-grid">
        ${field("nome", "Nome")}${field("data_nascimento", "Data de nascimento", "date")}${field("email", "E-mail", "email")}
        ${field("cpf", "CPF")}${field("senha", "Senha", "password", 'autocomplete="new-password"')}
        <div class="campo"><label for="role_id">Papel</label><select id="role_id" name="role_id" required>${options(roles, "responsabilidade")}</select></div></div>
        <button class="botao primario" type="submit">Cadastrar</button></form>`);
    formAction($("form"), async data => {
        const body = Object.fromEntries(data);
        body.role_id = Number(body.role_id);
        await post("/usuarios", body);
        location.assign("usuarios.html");
    });
}
async function start() {
    if (["login.html", "index.html"].includes(page)) {
        await login();
        return;
    }
    if (!sessionStorage.getItem("token")) {
        location.replace("login.html");
        return;
    }
    user = await api("/auth/me");
    const permissions = {
        comum: ["usuario_dashboard.html", "usuario_solicitar_equipamento.html",
            "usuario_confirmar_solicitacao.html", "usuario_minhas_solicitacoes.html",
            "usuario_meus_emprestimos.html", "solicitacao_detalhe.html"
        ],
        gestor: ["dashboard.html", "solicitacoes.html", "solicitacao_detalhe.html",
            "emprestimos.html", "devolucao.html"
        ],
        administrador: ["dashboard.html", "equipamentos.html", "equipamento_form.html",
            "usuarios.html", "usuario_form.html", "papeis.html",
            "status_equipamentos.html", "almoxarifados.html"
        ]
    };
    if (!permissions[user.papel]) {
        sessionStorage.clear();
        location.replace("login.html");
        return;
    }
    if (!permissions[user.papel].includes(page)) {
        location.replace(home());
        return;
    }
    navigation();
    const routes = {
        "equipamentos.html": () => equipments(),
        "usuario_solicitar_equipamento.html": () => equipments(true),
        "equipamento_form.html": equipmentForm,
        "usuario_confirmar_solicitacao.html": confirmRequest,
        "solicitacoes.html": requests,
        "usuario_minhas_solicitacoes.html": requests,
        "solicitacao_detalhe.html": requestDetail,
        "emprestimos.html": loans,
        "usuario_meus_emprestimos.html": loans,
        "devolucao.html": returnForm,
        "usuarios.html": users,
        "usuario_form.html": userForm
    };
    if (routes[page]) await routes[page]();
    else if (["almoxarifados.html", "papeis.html", "status_equipamentos.html"].includes(page)) {
        const [path, label] = {
            "almoxarifados.html": ["/almoxarifados", "descricao"],
            "papeis.html": ["/papeis", "responsabilidade"],
            "status_equipamentos.html": ["/status-equipamento", "status"]
        } [page];
        const rows = await api(path);
        screen({
            descricao: "Almoxarifados",
            responsabilidade: "Papéis",
            status: "Status"
        } [label], table(["ID", "Descrição"], rows.map(r =>
            `<tr>${td(r.id)}${td(r[label])}</tr>`)));
    } else screen("Início",
        `<section class="card"><h2>Olá, ${escapeHTML(user.nome)}</h2><p>Use o menu para acessar as operações do perfil ${escapeHTML(user.papel)}.</p></section>`
    );
}
start()
    .catch(error => message(error.message));
