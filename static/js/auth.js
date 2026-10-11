// A sessão é um cookie HttpOnly: o JavaScript não lê nem reenvia — o navegador
// já o inclui sozinho em toda requisição para o mesmo site.
// Para saber se a sessão ainda é válida, perguntamos à API.

function protegePagina() {
    fetch('/api/session')
        .then(function (resposta) {
            if (resposta.status === 401) {
                window.location.replace('/app/login.html');
            }
        })
        .catch(function () {
            // sem rede: mantém a página como está
        });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', protegePagina);
} else {
    protegePagina();
}

// Se alguma requisição do HTMX voltar com 401, a sessão expirou: volta ao login
document.body.addEventListener('htmx:responseError', function (event) {
    if (event.detail.xhr.status === 401) {
        window.location.replace('/app/login.html');
    }
});
