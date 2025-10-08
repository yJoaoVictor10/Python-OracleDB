import oracledb
from getpass import getpass

SERVIDOR = 'oracle.fiap.com.br'
PORTA = 1521
SERVICO = 'ORCL'

def abre_conexao(usuario, senha):
    conexao = oracledb.connect(
        user = usuario,
        password = senha,
        dsn = f'{SERVIDOR}:{PORTA}/{SERVICO}'
    )
    return conexao

def faz_queries(cursor, conexao):
    tabela = 'DDD_REMEDIOS'
    query = f'SELECT * FROM {tabela}'
    
    cursor.execute(query) # envia a query SQL para o banco de dados.
     
    for linha in cursor:
        print(linha)


def main():
    print('Insira suas credenciais no BD Oracle da FIAP.')
    usuario = input('username: ')
    senha = getpass('senha: ')  # é como input, mas esconde o que estou digitando

    conexao = abre_conexao(usuario, senha)
    
    print('Programa abriu conexão com o Banco de Dados.')
    cursor = conexao.cursor() # objeto usado para executar comandos SQL
    faz_queries(cursor, conexao) 
    
    
    cursor.close()
    conexao.close()
    print('Programa fechou a conexão e está encerrando.')

if __name__ == '__main__':
    main()