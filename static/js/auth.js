// Manipular cookie de autenticação
window.onload = function() {
    const authCookie = document.cookie.split('; ')
            .find(row => row.startsWith('Authorization='));
            
        if (!authCookie) {
            window.location.replace('/app/login.html');
        }
};

// Adicionar cookie de autenticação no header da requisição
document.body.addEventListener('htmx:configRequest', function(event) {
    const authCookie = document.cookie.split('; ')
        .find(row => row.startsWith('Authorization='));
    
    if (authCookie) {
        const token = authCookie.split('=')[1];
        event.detail.headers['Authorization'] = token;
    }
});