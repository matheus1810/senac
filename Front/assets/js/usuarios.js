import { enviar, requisitar } from "./api.js";
import {
    configurarFormulario, exibirTela, montarCampo, montarCelula,
    montarOpcoes, montarTabela, selecionar
} from "./interface.js";

export async function exibirUsuarios() {
    const usuarios = await requisitar("/usuarios");
    const linhas = usuarios.map(usuario => `
        <tr>${montarCelula(usuario.nome)}${montarCelula(usuario.email)}${montarCelula(usuario.cpf)}</tr>`);
    exibirTela("Usuários", `
        <div class="acoes">
            <a class="botao primario" href="usuario_form.html">Novo usuário</a>
        </div>
        ${montarTabela(["Nome", "E-mail", "CPF"], linhas)}`);
}

export async function exibirFormularioUsuario() {
    const papeis = await requisitar("/papeis");
    exibirTela("Novo usuário", `
        <form class="card form-card">
            <div class="form-grid">
                ${montarCampo("nome", "Nome")}
                ${montarCampo("data_nascimento", "Data de nascimento", "date")}
                ${montarCampo("email", "E-mail", "email")}
                ${montarCampo("cpf", "CPF")}
                ${montarCampo("senha", "Senha", "password", 'autocomplete="new-password"')}
                <div class="campo">
                    <label for="role_id">Papel</label>
                    <select id="role_id" name="role_id" required>
                        ${montarOpcoes(papeis, "responsabilidade")}
                    </select>
                </div>
            </div>
            <button class="botao primario" type="submit">Cadastrar</button>
        </form>`);

    configurarFormulario(selecionar("form"), async dadosFormulario => {
        const dados = Object.fromEntries(dadosFormulario);
        dados.role_id = Number(dados.role_id);
        await enviar("/usuarios", dados);
        location.assign("usuarios.html");
    });
}
