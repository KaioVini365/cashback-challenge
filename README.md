# 💰 Sistema de Cashback API

Um sistema full-stack leve e eficiente para cálculo e registro de cashback. Este projeto foi desenvolvido para demonstrar habilidades sólidas em **Desenvolvimento Web, Integração de APIs e Banco de Dados**, simulando uma regra de negócio real de varejo.

## Principais Funcionalidades
- **Cálculo Dinâmico:** Algoritmo que calcula cashbacks com base em regras de negócio (limites de promoção, cupons e bônus para clientes VIP).
- **API RESTful:** Backend construído com Python e Flask, lidando com requisições POST e GET de forma estruturada e com tratamento de erros.
- **Persistência de Dados:** Histórico de transações salvo em um banco de dados relacional (PostgreSQL), rastreando IP, valores e datas.
- **Interface Reativa:** Frontend em Vanilla JS (Fetch API) consumindo os endpoints do backend.

## Regras de Negócio
- Cálculo de Cashback

`Cashback Base: 5% sobre o valor final da compra (após descontos)
Promoção: Dobro do cashback para compras acima de R$ 500,00
Bônus VIP: Clientes VIP recebem 10% adicional sobre o cashback calculado`

## Tecnologias Utilizadas
- **Backend:** Python, Flask, Flask-CORS
- **Banco de Dados:** PostgreSQL, psycopg2
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Boas Práticas:** Variáveis de ambiente (.env), separação de responsabilidades (Rotas vs Banco de Dados).

## Como executar o projeto localmente

1. Clone o repositório:
`git clone https://github.com/seu-usuario/seu-repositorio.git`

2. Instale as dependências do Python:
`pip install flask flask-cors psycopg2-binary python-dotenv`

3. Configure as credenciais do seu banco de dados em um arquivo `.env` baseado no `database.py`.

4. Crie a tabela e inicie a API:
`python database.py`
`python app.py`

5. Abra o arquivo `index.html` no seu navegador.