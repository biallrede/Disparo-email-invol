from dotenv import load_dotenv
import os 
import requests
import json
from query import consulta_token

def gera_dados_atendimento(id_cliente_servico,data_hora_atual):
    df_token = consulta_token()
    token = str(df_token.loc[0,'token'])
    print('token:',token)
    rota = "https://api.allrede.hubsoft.com.br"
    url = f"{rota}/api/v1/atendimento/iniciar"
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {token}"}
    payload = json.dumps({
                "id_cliente_servico": f"{id_cliente_servico}"
            })
    
    response = requests.post(url, headers=headers, data=payload)
    print('response:',response)
    if response.status_code == 200:
        dados = response.json()
        id_atendimento = ''
        id_cliente_servico = ''
        descricao = ''
        nome = ''
        telefone = ''
        email = ''
        id_tipo_atendimento = ''
        id_atendimento_status = ''
        abrir_os = ''
        nome_contato = ''
        descricao_abertura = ''
        descricao_fechamento = ''
        telefone_contato =  ''
        
        cliente_servico = dados['atendimento']['cliente_servico']
        nome = cliente_servico["cliente"]["nome_razaosocial"]
        id_atendimento = dados['atendimento']['id_atendimento']
        id_cliente_servico = dados['atendimento']["id_cliente_servico"]
        descricao = "Resolvido"
        telefone = dados['atendimento']["telefone_contato"]
        telefone_contato = telefone
        email = dados['atendimento']["email_contato"]
        id_tipo_atendimento = 6752
        id_atendimento_status = 3
        id_motivo_fechamento_atendimento = 773
        abrir_os = "false"
        nome_contato = dados['atendimento']["nome_contato"]
        descricao_abertura = f'Enviado e-mail de negativação para o cliente: {nome}\n ID Cliente Serviço: {id_cliente_servico} na data e hora: {data_hora_atual}, através do bot de envio de e-mail de negativação.'
        descricao_fechamento = f'Enviado e-mail de negativação para o cliente: {nome}\n ID Cliente Serviço: {id_cliente_servico} na data e hora: {data_hora_atual}, através do bot de envio de e-mail de negativação.'
        
        dados_rota = {
            "id_atendimento": id_atendimento,
            "id_cliente_servico": id_cliente_servico,
            "nome": nome,
            "telefone": telefone,
            "telefone_contato": telefone_contato,
            "email": email,
            "tipo_atendimento":{
                "id_tipo_atendimento": id_tipo_atendimento,
                "id_tipo_atendimento_pai": 'null', 
                "descricao": "04.04 ANALISE-CCI"
            },
            "atendimento_status":
            {
                "id_atendimento_status": id_atendimento_status, 
                "descricao": descricao,
                "prefixo": "resolvido"
            },
            "motivo_fechamento_atendimento":
            {
                "id_motivo_fechamento_atendimento": id_motivo_fechamento_atendimento,
                "descricao": "Notificação de pagamento enviada"
            },
            
            "abrir_os": abrir_os,
            "nome_contato": nome_contato,
            "descricao_abertura": descricao_abertura,
            "descricao_fechamento": descricao_fechamento,
            "cliente_servico": cliente_servico,
            
        }
        return dados_rota
    
def abre_atendimento(dados):
    df_token = consulta_token()
    token = str(df_token.loc[0,'token'])
    rota = "https://api.allrede.hubsoft.com.br"
    url = f"{rota}/api/v1/atendimento"
    dados_json = json.dumps(dados).replace("'", '"')
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {token}"}
    
    
    response = requests.post(url, headers=headers, data=dados_json)
   
    return response.text