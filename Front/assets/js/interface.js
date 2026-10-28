// Funções de apresentação compartilhadas pelas telas. Não consultam o banco/API.
export function selecionar(seletor) {
    return document.querySelector(seletor);
}

export function escaparHtml(valor) {
    const caracteres = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    };
    return String(valor ?? "").replace(/[&<>"']/g, caractere => caracteres[caractere]);
}

export function exibirMensagem(texto) {
    let caixa = selecionar("#mensagem");
    if (!caixa) {
        caixa = document.createElement("p");
        caixa.id = "mensagem";
        caixa.setAttribute("role", "alert");
        const recipiente = selecionar("main") || document.body;
        recipiente.prepend(caixa);
    }
    caixa.textContent = texto;
}

// Padroniza o envio: impede recarregar a página, desabilita o botão e mostra erros.
export function configurarFormulario(formulario, aoEnviar) {
    formulario.addEventListener("submit", async evento => {
        evento.preventDefault();
        const botao = formulario.querySelector('[type="submit"]');
        if (botao) botao.disabled = true;
        try {
            await aoEnviar(new FormData(formulario));
        } catch (erro) {
            exibirMensagem(erro.message);
        } finally {
            if (botao) botao.disabled = false;
        }
    });
}

export function montarTabela(cabecalhos, linhas) {
    const titulos = cabecalhos.map(titulo => `<th>${titulo}</th>`).join("");
    const conteudo = linhas.length
        ? linhas.join("")
        : `<tr><td colspan="${cabecalhos.length}">Nenhum registro encontrado.</td></tr>`;
    return `
        <div class="tabela-container">
            <table>
                <thead><tr>${titulos}</tr></thead>
                <tbody>${conteudo}</tbody>
            </table>
        </div>`;
}

export function montarCelula(valor) {
    return `<td>${escaparHtml(valor)}</td>`;
}

export function montarOpcoes(registros, campoDescricao) {
    return registros.map(registro => `
        <option value="${registro.id}">${escaparHtml(registro[campoDescricao])}</option>`
    ).join("");
}

export function montarCampo(nome, rotulo, tipo = "text", atributos = "") {
    return `
        <div class="campo">
            <label for="${nome}">${rotulo}</label>
            <input id="${nome}" name="${nome}" type="${tipo}" required ${atributos}>
        </div>`;
}

export function exibirTela(titulo, conteudo) {
    selecionar("h1").textContent = titulo;
    selecionar("#conteudo").innerHTML = conteudo;
}
