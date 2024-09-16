import pyodbc
import psycopg2

# para rodar no linux
def credenciais_banco():
    conn = psycopg2.connect(
                        host ='134.65.24.116',
                        port = '9432',
                        database='hubsoft',
                        user='erick_leitura',
                        password='73f4cc9b2667d6c44d20d1a0d612b26c5e1763c2'
                        )
   
    return conn.cursor()

# para rodar no windows 
# def credenciais_banco():
#     conn = pyodbc.connect('Driver={PostgreSQL ODBC Driver(UNICODE)};'
#                         'Server=134.65.24.116;'
#                         'Port=9432;'
#                         'Database=hubsoft;'
#                         'Uid=erick_leitura;'
#                         'Pwd=73f4cc9b2667d6c44d20d1a0d612b26c5e1763c2;')
    
#     return conn

# para rodar no linux
def credenciais_banco_token():
# Configuração da conexão com o banco de dados
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'Server=187.121.151.19;' 
        'Database=DB_BASE;'
        'UID=user_allnexus;'
        'PWD=uKl041xn8HIw0WF;'
        'TrustServerCertificate=yes;'
    )
    return conn

# para rodar no windows
# def credenciais_banco_token():
# # Configuração da conexão com o banco de dados
#     conn = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'Server=187.121.151.19;' 
#         'Database=DB_BASE;'
#         'UID=user_allnexus;'
#         'PWD=uKl041xn8HIw0WF;'
#     )
#     return conn