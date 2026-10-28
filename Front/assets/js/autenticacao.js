import { enviar, requisitar } from "./api.js";
import { configurarFormulario, montarCampo, selecionar } from "./interface.js";
import { limparSessao, paginaInicial, salvarToken } from "./sessao.js";

export function exibirLogin() {
    selecionar("main").innerHTML = `
        <header>
            <h1>Gestão de Equipamentos</h1>
            <p>Acesso ao sistema</p>
        </header>
        <form>
            ${montarCampo("email", "E-mail", "email", 'autocomplete="username"')}
            ${montarCampo("senha", "Senha", "password", 'autocomplete="current-password"')}
            <button type="submit" class="botao primario">Entrar</button>
        </form>`;

    configurarFormulario(selecionar("form"), async dadosFormulario => {
        limparSessao();
        const credenciais = Object.fromEntries(dadosFormulario);
        const resposta = await enviar("/login", credenciais);
        salvarToken(resposta.access_token);
        const usuario = await requisitar("/auth/me");
        location.assign(paginaInicial(usuario));
    });
}
