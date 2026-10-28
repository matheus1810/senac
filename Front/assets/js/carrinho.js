// Guarda apenas os IDs selecionados. O servidor confere a disponibilidade ao aprovar.
function lerCarrinho() {
    try {
        const itens = JSON.parse(sessionStorage.getItem("cart") || "[]");
        return Array.isArray(itens) ? itens : [];
    } catch {
        return [];
    }
}

let equipamentosSelecionados = lerCarrinho();

export function obterCarrinho() {
    return [...equipamentosSelecionados];
}

export function estaSelecionado(equipamentoId) {
    return equipamentosSelecionados.includes(equipamentoId);
}

export function alternarSelecao(equipamentoId) {
    equipamentosSelecionados = estaSelecionado(equipamentoId)
        ? equipamentosSelecionados.filter(id => id !== equipamentoId)
        : [...equipamentosSelecionados, equipamentoId];
    salvarCarrinho();
}

export function limparCarrinho() {
    equipamentosSelecionados = [];
    salvarCarrinho();
}

function salvarCarrinho() {
    sessionStorage.setItem("cart", JSON.stringify(equipamentosSelecionados));
}
