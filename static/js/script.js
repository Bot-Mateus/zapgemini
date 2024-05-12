var intervalID;

// Função para enviar uma solicitação POST para desativar a função do robô no Flask
function desativarFuncao(username) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/desativar_funcao/" + username, true);  // Envia uma solicitação GET para desativar a função do robô
    xhr.send();
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                console.log(response.message);  // Exibe uma mensagem de sucesso no console (opcional)
            } else {
                console.error(response.message);  // Exibe uma mensagem de erro no console (opcional)
            }
        }
    };
}

// Função para enviar uma solicitação POST para o servidor Flask
function toggleAI() {
    var checkbox = document.getElementById("toggle-button");
    var username = checkbox.getAttribute("data-username");  // Obtém o nome de usuário do atributo data-username
    var ativo = checkbox.checked;  // Obtém o estado do botão de alternância (true/false)

    if (!ativo) {  // Se o botão estiver desligado
        desativarFuncao(username);  // Chama a função para desativar a função do robô
    } else {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/toggle_ai", true);  // Envia uma solicitação POST para ativar a função do robô
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ username: username, ativo: ativo }));  // Envia o estado do botão de alternância ao Flask
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Você pode adicionar qualquer lógica adicional aqui
            }
        };
    }
}

// Função para atualizar a imagem do QR Code
function updateQRCodeImage() {
    var username = "{{ username }}";
    var qrCodeImage = document.getElementById("qrCodeImage");
    qrCodeImage.src = "/static/qrcodes/gemini_screenshot_qr_code_regiao.png?" + new Date().getTime();
}

// Chamar a função de atualização a cada 5 segundos
setInterval(updateQRCodeImage, 5000); // 5000 milissegundos = 5 segundos