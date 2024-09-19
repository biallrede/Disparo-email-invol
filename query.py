import pandas as pd 
from credentials import *

def consulta_clientes_invol():
    conn = credenciais_banco()
    query = '''
                SELECT 
                D.codigo_cliente
                ,D.nome_razaosocial
                ,D.email_principal
                ,A.id_cliente_servico
                ,B.descricao AS motivo_cancelamento
                ,E.id_fatura
                ,E.nosso_numero
                ,E.valor
                ,E.data_vencimento
                ,E.ativo = true as status_fatura
                ,A.data_cancelamento::date
            --	  ,C.observacao
            FROM cliente_servico A 

            LEFT JOIN motivo_cancelamento B ON B.id_motivo_cancelamento = A.id_motivo_cancelamento
            LEFT JOIN protocolo_cancelamento C ON C.id_cliente_servico = A.id_cliente_servico
            LEFT JOIN cliente D ON D.id_cliente = A.id_cliente
            LEFT JOIN fatura E ON E.id_cliente_servico = A.id_cliente_servico
            WHERE A.data_habilitacao NOTNULL 							-- Serviço Habilitado
            AND A.id_servico_status IN (9, 30)						-- Status 'Cancelado', 'Cancelado Sem Retirada'
            AND B.gera_grafico = true									-- Motivo de Cancelamento Válido
            AND B.id_motivo_cancelamento IN (20, 42, 474)				-- Apenas Cancelamentos Involuntários
            AND A.id_servico NOT IN (5165, 8134, 4179, 4219, 9451)	-- Aluguel de Porta, Locação de Infraestrutura, Rede Neutra  
            --AND A.data_cancelamento::date between '2024-09-01' and '2024-09-12'
			AND A.data_cancelamento::date = CURRENT_DATE - interval '1 day'
            AND E.ativo = true 
            AND E.data_pagamento isnull 
                '''
    
    df = pd.read_sql(query,conn)
    conn.close()

    return df

def consulta_clientes_invol_seg():
    conn = credenciais_banco()
    query = '''
                SELECT 
                D.codigo_cliente
                ,D.nome_razaosocial
                ,D.email_principal
                ,A.id_cliente_servico
                ,B.descricao AS motivo_cancelamento
                ,E.id_fatura
                ,E.nosso_numero
                ,E.valor
                ,E.data_vencimento
                ,E.ativo = true as status_fatura
                ,A.data_cancelamento::date
            --	  ,C.observacao
            FROM cliente_servico A 

            LEFT JOIN motivo_cancelamento B ON B.id_motivo_cancelamento = A.id_motivo_cancelamento
            LEFT JOIN protocolo_cancelamento C ON C.id_cliente_servico = A.id_cliente_servico
            LEFT JOIN cliente D ON D.id_cliente = A.id_cliente
            LEFT JOIN fatura E ON E.id_cliente_servico = A.id_cliente_servico
            WHERE A.data_habilitacao NOTNULL 							-- Serviço Habilitado
            AND A.id_servico_status IN (9, 30)						-- Status 'Cancelado', 'Cancelado Sem Retirada'
            AND B.gera_grafico = true									-- Motivo de Cancelamento Válido
            AND B.id_motivo_cancelamento IN (20, 42, 474)				-- Apenas Cancelamentos Involuntários
            AND A.id_servico NOT IN (5165, 8134, 4179, 4219, 9451)	-- Aluguel de Porta, Locação de Infraestrutura, Rede Neutra  
            AND A.data_cancelamento::date between (CURRENT_DATE - interval '3 day') and (CURRENT_DATE - interval '1 day') 
            AND E.ativo = true 
            AND E.data_pagamento isnull 
                '''
    
    df = pd.read_sql(query,conn)
    conn.close()

    return df

def consulta_clientes_invol_feriado_outros_dias():
    conn = credenciais_banco()
    query = '''
                SELECT 
                D.codigo_cliente
                ,D.nome_razaosocial
                ,D.email_principal
                ,A.id_cliente_servico
                ,B.descricao AS motivo_cancelamento
                ,E.id_fatura
                ,E.nosso_numero
                ,E.valor
                ,E.data_vencimento
                ,E.ativo = true as status_fatura
                ,A.data_cancelamento::date
            --	  ,C.observacao
            FROM cliente_servico A 

            LEFT JOIN motivo_cancelamento B ON B.id_motivo_cancelamento = A.id_motivo_cancelamento
            LEFT JOIN protocolo_cancelamento C ON C.id_cliente_servico = A.id_cliente_servico
            LEFT JOIN cliente D ON D.id_cliente = A.id_cliente
            LEFT JOIN fatura E ON E.id_cliente_servico = A.id_cliente_servico
            WHERE A.data_habilitacao NOTNULL 							-- Serviço Habilitado
            AND A.id_servico_status IN (9, 30)						-- Status 'Cancelado', 'Cancelado Sem Retirada'
            AND B.gera_grafico = true									-- Motivo de Cancelamento Válido
            AND B.id_motivo_cancelamento IN (20, 42, 474)				-- Apenas Cancelamentos Involuntários
            AND A.id_servico NOT IN (5165, 8134, 4179, 4219, 9451)	-- Aluguel de Porta, Locação de Infraestrutura, Rede Neutra  
            AND A.data_cancelamento::date = (CURRENT_DATE - interval '1 day') 
            AND E.ativo = true 
            AND E.data_pagamento isnull 
                '''
    
    df = pd.read_sql(query,conn)
    conn.close()

    return df

def consulta_clientes_invol_feriado_seg():
    conn = credenciais_banco()
    query = '''
                SELECT 
                D.codigo_cliente
                ,D.nome_razaosocial
                ,D.email_principal
                ,A.id_cliente_servico
                ,B.descricao AS motivo_cancelamento
                ,E.id_fatura
                ,E.nosso_numero
                ,E.valor
                ,E.data_vencimento
                ,E.ativo = true as status_fatura
                ,A.data_cancelamento::date
            --	  ,C.observacao
            FROM cliente_servico A 

            LEFT JOIN motivo_cancelamento B ON B.id_motivo_cancelamento = A.id_motivo_cancelamento
            LEFT JOIN protocolo_cancelamento C ON C.id_cliente_servico = A.id_cliente_servico
            LEFT JOIN cliente D ON D.id_cliente = A.id_cliente
            LEFT JOIN fatura E ON E.id_cliente_servico = A.id_cliente_servico
            WHERE A.data_habilitacao NOTNULL 							-- Serviço Habilitado
            AND A.id_servico_status IN (9, 30)						-- Status 'Cancelado', 'Cancelado Sem Retirada'
            AND B.gera_grafico = true									-- Motivo de Cancelamento Válido
            AND B.id_motivo_cancelamento IN (20, 42, 474)				-- Apenas Cancelamentos Involuntários
            AND A.id_servico NOT IN (5165, 8134, 4179, 4219, 9451)	-- Aluguel de Porta, Locação de Infraestrutura, Rede Neutra  
            AND A.data_cancelamento::date between (CURRENT_DATE - interval '3 day') and CURRENT_DATE 
            AND E.ativo = true 
            AND E.data_pagamento isnull 
                '''
    
    df = pd.read_sql(query,conn)
    conn.close()

    return df

def consulta_token():
    conn = credenciais_banco_token()
    query = '''
            select token from API_TOKEN_HUBSOFT
            '''
    df = pd.read_sql(query,conn)
    return df