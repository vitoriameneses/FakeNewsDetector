function detectarFakeNews() {
    var text = document.getElementById("textInput").value;
    fetch('http://127.0.0.1:5000/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: 'texto da noticia' })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Este texto possui " + data.probability + "% de chance de ser fake news.";
    })
    .catch(error => console.error('Erro:', error));
}
/*
Quando a resposta da requisição é recebida, os dados são convertidos para JSON e o resultado é exibido na página HTML.

É importante notar que o servidor Flask precisa estar em execução para que a requisição seja processada corretamente.
*/