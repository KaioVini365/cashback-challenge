const API_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', function() {
   carregarHistorico();
      const form = document.getElementById('formCashback');

   form.addEventListener('submit',function(e){
    e.preventDefault();
    calcularCashback();
   })
});


async function calcularCashback() {

    const tipoCliente = document.getElementById('tipoCliente').value;
    const valor = parseFloat(document.getElementById('valor').value);
    const cupom = parseFloat(document.getElementById('cupom').value);


    const dados = {

        tipo_cliente: tipoCliente,
        valor: valor,
        cupom: cupom

    };


    try{

        const response = await fetch(`${API_URL}/calcular`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const resultado = await response.json();

        if (resultado.sucesso) {
            exibirResultado(resultado.detalhes);
            carregarHistorico();
        }else {
            alert('Erro: ' + resultado.erro);
        }

    } catch (error) {
        alert('Erro ao conectar com a API: ');
 
    }

}

function exibirResultado(detalhes) {
    document.getElementById('valorOriginal').textContent = detalhes.valor_original.toFixed(2);
    document.getElementById('descontoCupom').textContent = detalhes.desconto_cupom.toFixed(2);
    document.getElementById('valorFinal').textContent = detalhes.valor_final.toFixed(2);
    document.getElementById('cashbackFinal').textContent = detalhes.cashback_final.toFixed(2);

    const divResultado = document.getElementById('resultado');
    divResultado.classList.remove('hidden');

}

async function carregarHistorico() {
    try {
        const response = await fetch(`${API_URL}/historico`);
        const resultado = await response.json();

        const mensagem = document.getElementById('mensagemHistorico');
        const tabela = document.getElementById('tabelaHistorico');

        if (resultado.sucesso && resultado.historico.length > 0) {
            mensagem.classList.add('hidden');
            tabela.classList.remove('hidden');

            const tbody = document.getElementById('corpoHistorico');
            tbody.innerHTML = '';

            resultado.historico.forEach(function(consulta) {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${consulta.data_hora}</td>
                    <td>${consulta.tipo_cliente}</td>
                    <td>$R$ ${consulta.valor_compra.toFixed(2)}</td>
                    <td>$R$ ${consulta.cashback.toFixed(2)}</td>
            `;
            
            tbody.appendChild(tr);
            

            });
            
        } else {
            mensagem.textContent = 'Nenhuma consulta registrada ainda.';

}

} catch (error) {
        console.error('Erro:', error);
}

            }
