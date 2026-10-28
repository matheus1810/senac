import { enviar, requisitar } from "./api.js";
import { limparCarrinho, obterCarrinho } from "./carrinho.js";
import {
    configurarFormulario, escaparHtml, exibirMensagem, exibirTela,
    montarCelula, montarTabela, selecionar
} from "./interface.js";

export async function exibirConfirmacaoSolicitacao() {
    const selecionados = obterCarrinho();
    const equipamentos = (await requisitar("/equipamentos"))
        .filter(equipamento => selecionados.includes(equipamento.id));
    const linhas = equipamentos.map(equipamento => `
        <tr>${montarCelula(equipamento.nome)}${montarCelula(equipamento.numero_serie)}</tr>`);
    const tabela = montarTabela(["Equipamento", "Série"], linhas);
    exibirTela("Confirmar solicitação", `
        ${tabela}
        <form>
            <button type="submit" class="botao primario" ${equipamentos.length ? "" : "disabled"}>
                Enviar solicitação
            </button>
        </form>`);

    configurarFormulario(selecionar("form"), async () => {
        await enviar("/solicitacoes", {
            equipamento_ids: equipamentos.map(equipamento => equipamento.id)
        });
        limparCarrinho();
        location.assign("usuario_minhas_solicitacoes.html");
    });
}

export async function exibirSolicitacoes(usuario) {
    const solicitacoes = await requisitar("/solicitacoes");
    const titulo = usuario.papel === "comum" ? "Minhas solicitações" : "Solicitações";
    const linhas = solicitacoes.map(solicitacao => {
        const data = new Date(solicitacao.data_solicitacao).toLocaleString("pt-BR");
        const itens = solicitacao.itens.map(item => `${item.equipamento}: ${item.status}`).join(", ");
        return `
            <tr>
                ${montarCelula(solicitacao.id)}
                ${montarCelula(solicitacao.solicitante)}
                ${montarCelula(data)}
                ${montarCelula(itens)}
                <td><a href="solicitacao_detalhe.html?id=${solicitacao.id}">Ver detalhes</a></td>
            </tr>`;
    });
    exibirTela(titulo, montarTabela(["Número", "Solicitante", "Data", "Itens", "Ação"], linhas));
}

export async function exibirDetalheSolicitacao(usuario) {
    const solicitacaoId = new URLSearchParams(location.search).get("id");
    if (!solicitacaoId) {
        await exibirSolicitacoes(usuario);
        return;
    }
    const solicitacao = await requisitar(`/solicitacoes/${encodeURIComponent(solicitacaoId)}`);
    const linhas = solicitacao.itens.map(item => `
        <tr>${montarCelula(item.equipamento)}${montarCelula(item.status)}</tr>`);
    const podeAnalisar = usuario.papel === "gestor"
        && solicitacao.itens.every(item => item.status === "analise");
    const acoes = podeAnalisar ? `
        <div class="acoes">
            <button class="botao" data-decision="negar">Rejeitar</button>
            <button class="botao primario" data-decision="aprovar">Aprovar</button>
        </div>` : "";

    exibirTela(`Solicitação #${solicitacao.id}`, `
        <section class="card"><p>Solicitante: ${escaparHtml(solicitacao.solicitante)}</p></section>
        ${montarTabela(["Equipamento", "Status"], linhas)}
        ${acoes}`);
    configurarAnaliseSolicitacao(solicitacao.id, usuario);
}

function configurarAnaliseSolicitacao(solicitacaoId, usuario) {
    document.querySelectorAll("[data-decision]").forEach(botao => {
        botao.onclick = async () => {
            botao.disabled = true;
            try {
                const decisao = botao.dataset.decision;
                await enviar(`/solicitacoes/${solicitacaoId}/${decisao}`);
                await exibirDetalheSolicitacao(usuario);
            } catch (erro) {
                exibirMensagem(erro.message);
                botao.disabled = false;
            }
        };
    });
}
