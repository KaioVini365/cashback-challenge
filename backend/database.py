from dotenv import load_dotenv
load_dotenv()


import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime


def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'cashback_dbb'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'sua_senha_aqui'),
        'port': os.getenv('DB_PORT', '5432')
    }


def conectar_banco():
    try:
        config = get_db_config()
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco: {e}")
        raise


def criar_tabela():
    """
    estrututura da tabela:
    -id
    -ip
    -tipo_cliente: VIP ou CUPOM
    -valor_compra
    -cashback
    -data_hora: quando foi feita a consulta
    """
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        sql_criar_tabela = """
        CREATE TABLE IF NOT EXISTS consultas(
            id SERIAL PRIMARY KEY,
            ip VARCHAR(50) NOT NULL,
            tipo_cliente VARCHAR(10) NOT NULL,
            valor_compra DECIMAL(10, 2) NOT NULL,
            cashback DECIMAL(10, 2) NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(sql_criar_tabela)
        conn.commit()
        print("Tabela 'consultas' criada")

    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def salvar_consulta(ip, tipo_cliente, valor_compra, cashback):
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        sql_inserir = """
        INSERT INTO consultas (ip, tipo_cliente, valor_compra, cashback)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """

        cursor.execute(sql_inserir, (ip, tipo_cliente, valor_compra, cashback))
        consulta_id = cursor.fetchone()[0]

        conn.commit()
        print(f"✅ Consulta #{consulta_id} salva com sucesso!")
        return consulta_id

    except Exception as e:
        print(f"Erro ao salvar consulta: {e}")
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def buscar_historico(ip):
    conn = conectar_banco()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        sql_buscar = """
        SELECT
            id,
            tipo_cliente,
            valor_compra,
            cashback,
            data_hora
        FROM consultas
        WHERE ip = %s
        ORDER BY data_hora DESC;
        """
        cursor.execute(sql_buscar, (ip,))
        consultas = cursor.fetchall()

        resultado = []
        for consulta in consultas:
            resultado.append({
                'id': consulta['id'],
                'tipo_cliente': consulta['tipo_cliente'],
                'valor_compra': float(consulta['valor_compra']),
                'cashback': float(consulta['cashback']),
                'data_hora': consulta['data_hora'].strftime('%d/%m/%Y %H:%M:%S')
            })

        print(f"✅ {len(resultado)} consultas encontradas para IP {ip}")
        return resultado

    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Inicializando banco de dados...")
    criar_tabela()
    print("Banco de dados pronto")
