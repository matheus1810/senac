import { encerrarSessao, paginaPublica } from "./sessao.js";

// Todas as chamadas HTTP passam por aqui. A API está na mesma origem da interface.
export async function requisitar(caminho, opcoes = {}) {
    const token = sessionStorage.getItem("token");
    const resposta = await fetch(caminho, {
        ...opcoes,
        headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
            ...opcoes.headers
        }
    });
    const dados = await resposta.json().catch(() => ({}));

    if (!resposta.ok) {
        const pagina = location.pathname.split("/").pop() || "index.html";
        if (resposta.status === 401 && !paginaPublica(pagina)) {
            encerrarSessao();
        }
        const mensagem = typeof dados.detail === "string"
            ? dados.detail
            : "Confira os campos informados.";
        throw new Error(mensagem);
    }

    return dados;
}

export function enviar(caminho, dados) {
    return requisitar(caminho, {
        method: "POST",
        body: JSON.stringify(dados)
    });
}
