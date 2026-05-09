from flask import Flask, request, jsonify
from flask_cors import CORS
from database import salvar_consulta, buscar_historico
from datetime import datetime

app = Flask(__name__)
CORS(app)

def calcular_cashback(valor_original, percentual_cupom, cliente_vip):
    if valor_original <= 0:
        raise ValueError("O valor original deve ser positivo.")
    if percentual_cupom < 0 or percentual_cupom > 100:
        raise ValueError("Percentual de desconto deve estar entre 0 e 100")
    
    desconto_cupom = valor_original * (percentual_cupom / 100)
    valor_final = valor_original - desconto_cupom
    
    percentual_cashback_base = 0.05
    cashback_base = valor_final * percentual_cashback_base
    
    limite_promocao = 500
    if valor_original > limite_promocao:
        cashback_com_promocao = cashback_base * 2
        aplicou_promocao = True
    else:
        cashback_com_promocao = cashback_base
        aplicou_promocao = False
    
    percentual_bonus_vip = 0.10
    if cliente_vip:
        cashback_final = cashback_com_promocao * (1 + percentual_bonus_vip)
        bonus_vip = cashback_final - cashback_com_promocao
    else:
        cashback_final = cashback_com_promocao
        bonus_vip = 0
    
    return {
        'valor_original': round(valor_original, 2),
        'desconto_cupom': round(desconto_cupom, 2),
        'valor_final': round(valor_final, 2),
        'cashback_base': round(cashback_base, 2),
        'aplicou_promocao': aplicou_promocao,
        'cashback_com_promocao': round(cashback_com_promocao, 2),
        'bonus_vip': round(bonus_vip, 2),
        'cashback_final': round(cashback_final, 2),
        'cliente_vip': cliente_vip
    }

@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        dados = request.json
        tipo_cliente = dados["tipo_cliente"]
        valor = float(dados["valor"])
        cupom = float(dados.get("cupom", 0))
        ip = request.remote_addr
        
        vip = (tipo_cliente.upper() == "VIP")
        resultado = calcular_cashback(valor, cupom, vip)
        
        salvar_consulta(ip, tipo_cliente, valor, resultado["cashback_final"]) 
        
        return jsonify({
            "sucesso": True,
            "cashback": resultado["cashback_final"],
            "detalhes": resultado
        })
    
    except ValueError as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400
    
    except Exception as e:
        return jsonify({"sucesso": False, "erro": "Erro interno no servidor"}), 500

@app.route("/historico", methods=["GET"])
def historico():
    try:
        ip = request.remote_addr
        consultas = buscar_historico(ip)
        
        return jsonify({
            "sucesso": True,
            "historico": consultas
        })
    
    except Exception as e:
        return jsonify({"sucesso": False, "erro": "Erro ao buscar histórico"}), 500

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "API Cashback rodando",
        "rotas_disponiveis": [
            "POST /calcular - Calcular cashback",
            "GET /historico - Buscar histórico do IP"
        ]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")