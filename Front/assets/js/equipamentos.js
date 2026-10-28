import { requisitar } from "./api.js";
import { alternarSelecao, estaSelecionado } from "./carrinho.js";
import {
    configurarFormulario, exibirTela, montarCampo, montarCelula,
    montarOpcoes, montarTabela, selecionar
} from "./interface.js";

function buscarNomeStatus(statusId, statusCadastrados) {
    return statusCadastrados.find(status => status.id === statusId)?.status || "";
}

function equipamentoDisponivel(statusId, statusCadastrados) {
    const nome = buscarNomeStatus(statusId, statusCadastrados);
    const nomeNormalizado = nome.normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
    return nomeNormalizado === "disponivel";
}

// Administrador gerencia o cadastro; aluno seleciona equipamentos para solicitar.
export async function exibirEquipamentos(permitirSelecao = false) {
    const [equipamentos, statusCadastrados, almoxarifados] = await Promise.all([
        requisitar("/equipamentos"),
        requisitar("/status-equipamento"),
        requisitar("/almoxarifados")
    ]);
    const titulo = permitirSelecao ? "Solicitar equipamentos" : "Equipamentos";
    const acaoPrincipal = permitirSelecao
        ? '<a class="botao primario" href="usuario_confirmar_solicitacao.html">Revisar solicitação</a>'
        : '<a class="botao primario" href="equipamento_form.html">Novo equipamento</a>';

    const linhas = equipamentos.map(equipamento => {
        const almoxarifado = almoxarifados.find(item => item.id === equipamento.id_almoxarifado);
        let acao = `<a href="equipamento_form.html?id=${equipamento.id}">Editar</a>`;
        if (permitirSelecao) {
            const disponivel = equipamentoDisponivel(equipamento.status_id, statusCadastrados);
            const rotulo = estaSelecionado(equipamento.id) ? "Remover" : "Selecionar";
            acao = disponivel
                ? `<button class="botao" data-add="${equipamento.id}">${rotulo}</button>`
                : "Indisponível";
        }
        return `
            <tr>
                ${montarCelula(equipamento.nome)}
                ${montarCelula(equipamento.numero_serie)}
                ${montarCelula(buscarNomeStatus(equipamento.status_id, statusCadastrados))}
                ${montarCelula(almoxarifado?.descricao)}
                <td>${acao}</td>
            </tr>`;
    });

    const tabela = montarTabela(["Nome", "Série", "Status", "Almoxarifado", "Ação"], linhas);
    exibirTela(titulo, `<div class="acoes">${acaoPrincipal}</div>${tabela}`);
    configurarSelecaoEquipamentos();
}

function configurarSelecaoEquipamentos() {
    document.querySelectorAll("[data-add]").forEach(botao => {
        botao.onclick = () => {
            const equipamentoId = Number(botao.dataset.add);
            alternarSelecao(equipamentoId);
            botao.textContent = estaSelecionado(equipamentoId) ? "Remover" : "Selecionar";
        };
    });
}

export async function exibirFormularioEquipamento() {
    const [statusCadastrados, almoxarifados] = await Promise.all([
        requisitar("/status-equipamento"), requisitar("/almoxarifados")
    ]);
    const equipamentoId = new URLSearchParams(location.search).get("id");
    const titulo = equipamentoId ? "Editar equipamento" : "Novo equipamento";
    exibirTela(titulo, `
        <form class="card form-card">
            <div class="form-grid">
                ${montarCampo("nome", "Nome", "text", 'maxlength="255"')}
                ${montarCampo("numero_serie", "Número de série", "text", 'maxlength="255"')}
                ${montarCampo("valor", "Valor", "number", 'min="0" max="999999.99" step="0.01"')}
                <div class="campo">
                    <label for="status_id">Status</label>
                    <select id="status_id" name="status_id" required>
                        ${montarOpcoes(statusCadastrados, "status")}
                    </select>
                </div>
                <div class="campo">
                    <label for="id_almoxarifado">Almoxarifado</label>
                    <select id="id_almoxarifado" name="id_almoxarifado" required>
                        ${montarOpcoes(almoxarifados, "descricao")}
                    </select>
                </div>
            </div>
            <button type="submit" class="botao primario">Salvar</button>
        </form>`);

    if (equipamentoId) {
        const equipamento = await requisitar(`/equipamento/${encodeURIComponent(equipamentoId)}`);
        const campos = ["nome", "numero_serie", "valor", "status_id", "id_almoxarifado"];
        for (const campo of campos) {
            selecionar(`[name="${campo}"]`).value = equipamento[campo];
        }
    }

    configurarFormulario(selecionar("form"), async dadosFormulario => {
        const dados = Object.fromEntries(dadosFormulario);
        dados.status_id = Number(dados.status_id);
        dados.id_almoxarifado = Number(dados.id_almoxarifado);
        const caminho = equipamentoId
            ? `/equipamento/${encodeURIComponent(equipamentoId)}`
            : "/equipamentos";
        await requisitar(caminho, {
            method: equipamentoId ? "PUT" : "POST",
            body: JSON.stringify(dados)
        });
        location.assign("equipamentos.html");
    });
}
