import { requisitar } from "./api.js";
import { exibirTela, montarCelula, montarTabela } from "./interface.js";

// Estas três páginas apenas consultam os cadastros de apoio.
const CADASTROS = {
    "almoxarifados.html": {
        caminho: "/almoxarifados", campo: "descricao", titulo: "Almoxarifados"
    },
    "papeis.html": {
        caminho: "/papeis", campo: "responsabilidade", titulo: "Papéis"
    },
    "status_equipamentos.html": {
        caminho: "/status-equipamento", campo: "status", titulo: "Status"
    }
};

export async function exibirCadastroApoio(pagina) {
    const cadastro = CADASTROS[pagina];
    const registros = await requisitar(cadastro.caminho);
    const linhas = registros.map(registro => `
        <tr>${montarCelula(registro.id)}${montarCelula(registro[cadastro.campo])}</tr>`);
    exibirTela(cadastro.titulo, montarTabela(["ID", "Descrição"], linhas));
}
