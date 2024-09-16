import psycopg2
import csv
from credentials import credenciais_banco

# Função para gerar o nome do arquivo com base no mês
def get_file_name(month):
    return f"relatorio_{month:02d}.csv"

# Função para gerar o relatório
def generate_monthly_report(month):
    # Configurações de conexão ao banco de dados
    cursor = credenciais_banco()

    # Query com filtro para o mês atual
    query = f"""
    SELECT 
        c.codigo_cliente,
        c.nome_razaosocial AS cliente,
        a.status,
        a.data_vencimento,
        a.data_pagamento::date,
        a.valor,
        a.valor_pago,
        d.descricao AS forma_cobranca
    FROM cobranca a
    LEFT JOIN cliente_servico b ON b.id_cliente_servico = a.id_cliente_servico	
    LEFT JOIN cliente c ON c.id_cliente = b.id_cliente	
    LEFT JOIN forma_cobranca d ON d.id_forma_cobranca = a.id_forma_cobranca
    WHERE a.id_forma_cobranca IN ('280','255','318')
    AND (a.status LIKE 'baixado_banco' OR a.status LIKE 'baixado_pix')
    AND EXTRACT(MONTH FROM a.data_pagamento) = {month};
    """
    
    # Executa a query
    cursor.execute(query)
    
    # Pega os resultados
    results = cursor.fetchall()

    # Colunas
    colnames = [desc[0] for desc in cursor.description]

    # Gera o nome do arquivo CSV
    file_name = get_file_name(month)

    # Escreve os resultados em um arquivo CSV
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(colnames)  # Escreve o cabeçalho
        writer.writerows(results)  # Escreve os dados

    print(f"Relatório do mês {month:02d} gerado com sucesso: {file_name}")

    # Fecha a conexão
    cursor.close()
    

# Meses que você quer extrair os relatórios
meses = [1, 2, 3, 4, 5, 9, 10, 11, 12]

# Gera o relatório para cada mês
for mes in meses:
    print('entrei no laço de repetição')
    generate_monthly_report(mes)