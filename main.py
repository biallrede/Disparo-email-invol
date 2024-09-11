from query import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tabulate import tabulate
import numpy as np
from datetime import datetime
from rotas import *
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
import threading

def dispara_email():
    df_clientes = consulta_clientes_invol()
    copia_df = df_clientes
    # Agrupa as faturas pelo 'id_cliente_servico'
    df = copia_df.fillna('Sem email cadastrado') 
    df = df.groupby(['nome_razaosocial','id_cliente_servico','email_principal'])
    grupos_clientes = df_clientes.groupby('id_cliente_servico')
    

    for id_cliente, grupo in grupos_clientes:
        # email = 'leidiane.rodrigues@allrede.com.br'
        email = grupo['email_principal'].iloc[0]
        nome_cliente = grupo['nome_razaosocial'].iloc[0]

        if email and email not in ["null", "None"]:
            # Cabeçalho do e-mail
            mensagem_texto = f'''
            <p>Prezado(a) Sr(a). {nome_cliente},</p>
            <p>Gostaríamos de informar que, devido à inadimplência, o contrato com a Allrede foi rescindido.</p>
            <p>Notamos que há uma ou mais faturas vencidas referentes ao seu serviço de internet que ainda não foram quitadas. Para evitar qualquer inconveniente, estamos oferecendo a oportunidade de regularizar o pagamento e evitar a negativação do seu nome.</p>
            <p><b>Detalhes do Débito:</b></p>
            '''

            # Gera a tabela com os detalhes das faturas do cliente
            mensagem = []

            for index, row in grupo.iterrows():
                nome = row['nome_razaosocial']
                valor = row['valor']
                n_fatura = row['nosso_numero']
                mensagem.append([nome, n_fatura, valor])

            tabela = tabulate(mensagem, 
                              headers=["Nome/Razão Social", "Nº da Fatura", "  Valor (R$)"], 
                              tablefmt='html',
                              colalign=("center", "center", "right"))

            mensagem_texto += tabela

            # Rodapé do e-mail
            mensagem_texto += '''
            <p>Pedimos que entre em contato conosco o mais breve possível para que possamos encontrar a melhor solução para a regularização do débito. Ressaltamos que, caso o pagamento não seja efetuado, o seu nome poderá ser negativado junto aos órgãos de proteção ao crédito.</p>
            <p>Estamos à disposição para esclarecer quaisquer dúvidas e oferecer opções de pagamento que se adequem à sua situação. Você pode nos contatar pelo telefone (61) 3060-1990 ou 0800 033 0307.</p>
            <p>Caso já tenha efetuado o pagamento, por favor, desconsidere esta mensagem. Se houver qualquer divergência nos dados ou se esta mensagem não for destinada a você, pedimos desculpas pelo transtorno e solicitamos que nos informe para que possamos corrigir a situação.</p>
            <p>Agradecemos a sua atenção e aguardamos o seu contato.</p>
            '''
            abrir_atendimento(id_cliente)
            # Envia o e-mail formatado em HTML
            enviar_email('Regularização de Pagamento - Evite Negativação', mensagem_texto, email)
    
    msg = '''<p> O BOT de envio de e-mail de negativação foi disparado para os seguintes clientes:</p>'''
    df = pd.DataFrame(df)
    df_correto = pd.DataFrame(df[0].tolist(), columns=['nome_razaosocial', 'codigo_cliente', 'email_principal'])
    df_novo = df_correto[['nome_razaosocial', 'email_principal']].copy()
    df_novo['status_email'] = np.where((df_novo['email_principal'] == 'Sem email cadastrado'), 'e-mail não enviado', 'e-mail enviado')
    df_html = df_novo.to_html(index=False)
    msg += df_html
    email_validacao = "amanda.lima@allrede.com.br,leidiane.rodrigues@allrede.com.br"
    enviar_email('BOT Evite Negativação',msg,email_validacao)
        
def abrir_atendimento(id_cliente_servico):
    data_hora_atual = datetime.now()
    dados = gera_dados_atendimento(id_cliente_servico,data_hora_atual)
    status = abre_atendimento(dados)
    return status

def enviar_email(assunto,mensagem,email):
    # Configurações do servidor SMTP
    MAIL_HOST = "mail.allrede.net.br"
    MAIL_PORT = 465
    MAIL_USERNAME = "naoresponda_allrede@allrede.net.br"
    MAIL_PASSWORD = "e=&fRXFjiBQT"

    # Configurações do e-mail
    MAIL_FROM_ADDRESS = "naoresponda_allrede@allrede.net.br"
    MAIL_FROM_NAME = "Allrede"
    MAIL_TO_ADDRESS = email
    MAIL_SUBJECT = assunto
    MAIL_BODY = mensagem

    # Criar a mensagem de e-mail
    mensagem = MIMEMultipart()
    mensagem["From"] = f"{MAIL_FROM_NAME} <{MAIL_FROM_ADDRESS}>"
    # Use split para obter uma lista de destinatários
    to_addresses = MAIL_TO_ADDRESS.split(',')
    mensagem["To"] = ', '.join(to_addresses)
    mensagem["Subject"] = MAIL_SUBJECT

    # Adicionar corpo ao e-mail
    mensagem.attach(MIMEText(MAIL_BODY, "html"))

    # Configurar conexão SMTP
    try:
        servidor_smtp = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
        servidor_smtp.login(MAIL_USERNAME, MAIL_PASSWORD)

        # Enviar e-mail
        servidor_smtp.sendmail(MAIL_FROM_ADDRESS, to_addresses, mensagem.as_string())

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

    finally:
        # Fechar a conexão com o servidor SMTP
        if servidor_smtp:
            servidor_smtp.quit()


scheduler = BackgroundScheduler()

def rotina1():
    dispara_email()
    

schedule.every().day.at("09:00").do(rotina1)
scheduler.start()

while (1 == 1):
    schedule.run_pending()
    threading.Event().wait(1)

