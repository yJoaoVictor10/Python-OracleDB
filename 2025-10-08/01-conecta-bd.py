# se a linha abaixo não provoca erro, significa que a instalação deu certo
import oracledb

from getpass import getpass # função getpass pega senha sem mostrar no terminal

def main():
    print('Insira suas credenciais no BD Oracle da FIAP.')
    usuario = input('username: ')
    senha = getpass('senha: ')  # é como input, mas esconde o que estou digitando

    try:
        conexao = oracledb.connect(
            user = usuario,
            password = senha,
            dsn = 'oracle.fiap.com.br:1521/ORCL'
        )

        print('Consegui abrir conexão com o BD.')
        conexao.close()
    except:
        print('Não foi possível abrir conexão com o BD.')

if __name__ == '__main__':
    main()