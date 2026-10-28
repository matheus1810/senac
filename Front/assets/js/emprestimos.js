import { enviar, requisitar } from "./api.js";
import {
    configurarFormulario, escaparHtml, exibirTela,
    montarCelula, montarTabela, selecionar
} from "./interface.js";

export async function exibirEmprestimos(usuario) {
    const emprestimos = await requisitar("/emprestimos");
    const titulo = usuario.papel === "comum" ? "Meus empréstimos" : "Empréstimos";
    const linhas = emprestimos.map(emprestimo => {
        const dataEmprestimo = new Date(emprestimo.data_emprestimo).toLocaleString("pt-BR");
        const dataDevolucao = emprestimo.data_devolucao
            ? new Date(emprestimo.data_devolucao).toLocaleString("pt-BR")
            : "Em aberto";
        const podeDevolver = usuario.papel === "gestor" && !emprestimo.data_devolucao;
        const acao = podeDevolver
            ? `<a href="devolucao.html?id=${emprestimo.id}">Registrar devolução</a>`
            : escaparHtml(emprestimo.estado_na_devolucao);
        return `
            <tr>
                ${montarCelula(emprestimo.id)}
                ${montarCelula(emprestimo.equipamento)}
                ${montarCelula(emprestimo.solicitante)}
                ${montarCelula(dataEmprestimo)}
                ${montarCelula(dataDevolucao)}
                <td>${acao}</td>
            </tr>`;
    });
    const cabecalhos = ["Número", "Equipamento", "Solicitante", "Empréstimo", "Devolução", "Ação"];
    exibirTela(titulo, montarTabela(cabecalhos, linhas));
}

export async function exibirFormularioDevolucao(usuario) {
    const emprestimoId = new URLSearchParams(location.search).get("id");
    if (!emprestimoId) {
        await exibirEmprestimos(usuario);
        return;
    }
    const emprestimo = (await requisitar("/emprestimos"))
        .find(item => String(item.id) === emprestimoId);
    if (!emprestimo || emprestimo.data_devolucao) {
        throw new Error("Empréstimo não encontrado ou já devolvido.");
    }
    exibirTela(`Devolução #${emprestimo.id}`, `
        <section class="card">
            <p>${escaparHtml(emprestimo.equipamento)} · ${escaparHtml(emprestimo.solicitante)}</p>
            <form>
                <div class="campo">
                    <label for="estado_na_devolucao">Estado na devolução</label>
                    <select id="estado_na_devolucao" name="estado_na_devolucao">
                        <option>Bom estado</option>
                        <option>Com avarias</option>
                        <option>Necessita manutenção</option>
                    </select>
                </div>
                <div class="campo">
                    <label for="observacoes">Observações</label>
                    <textarea id="observacoes" name="observacoes" maxlength="255"></textarea>
                </div>
                <button type="submit" class="botao primario">Confirmar devolução</button>
            </form>
        </section>`);

    configurarFormulario(selecionar("form"), async dadosFormulario => {
        await enviar(`/emprestimos/${emprestimo.id}/devolver`, Object.fromEntries(dadosFormulario));
        location.assign("emprestimos.html");
    });
}
