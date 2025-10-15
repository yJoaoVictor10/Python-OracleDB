'''
Esse programa não supõe a existência da tabela Estudantes.

Se ela não existe, será criada pelo próprio programa abaixo. (Ver lógica no main)
'''

'''
Exercícios:

1. Melhorar a organização do main criando funções separadas para:
    - A lógica de verificação e criação da tabela
    - O menu

2. Modificar os prints para atingir uma melhor legibilidade do programa.
'''

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

def mostra_resultados_query(cursor):
    # fetchall retorna resultados da última query na forma de lista
    resultados = cursor.fetchall()
    
    print('\n')
    
    # Se a última query não teve resultado, printa uma mensagem especial
    if resultados == []:
        print('Não foram encontrados dados correspondentes a essa busca.')
    
    else:
        for res in resultados:
            print(res)
    
    print('------------------------\n') 
    

def mostra_todos_dados(cursor):
    cursor.execute('SELECT * FROM ESTUDANTES')
    mostra_resultados_query(cursor)
    

def mostra_resultados_busca(cursor, nome_procurar):
    query = 'SELECT * FROM ESTUDANTES WHERE nome = :nome'
    cursor.execute(query, {'nome' : nome_procurar})
    
    mostra_resultados_query(cursor)

def mostra_resultados_busca_rm(cursor, rm):
    query = 'SELECT * FROM ESTUDANTES WHERE rm = :rm'
    cursor.execute(query, {'rm' : rm})
    
    mostra_resultados_query(cursor)

def insere_novo_dado(conexao, cursor):
    print('Insira as informações para inserção no BD:')
    dicionario_dados = {
        'id' : int(input('ID: ')),
        'rm' : input('RM: '),
        'nome' : input('nome: '),
        'curso' : input('curso: '),
        'turma' : input('turma: ')
    }
    
    query = '''
    INSERT INTO ESTUDANTES (id, rm, nome, curso, turma)
    VALUES (:id, :rm, :nome, :curso, :turma)
    '''
    
    cursor.execute(query, dicionario_dados)
    conexao.commit() # necessário após fazer modificações na tabela
    
def remove_por_id(conexao, cursor, id_para_remover):
    query = 'DELETE FROM ESTUDANTES WHERE id = :id'
    cursor.execute(query, {'id' : id_para_remover})
    
    # rowcount conta o número de linhas afetadas na última query
    linhas_afetadas = cursor.rowcount
    
    if linhas_afetadas == 0:
        print('Não foi removido nenhum dado.')
        print('Provavelmente o ID é inexistente.')
        
    else:
        print('Remoção executada.')
        conexao.commit()

# Retorna True, se a tabela existe no Banco de Dados; retorna False caso contrário
def existe_tabela(cursor, nome_tabela):
    query = 'SELECT table_name FROM user_tables WHERE table_name = :nome'
    
    cursor.execute(query, {'nome' : nome_tabela})
    resultados = cursor.fetchall()
    
    # Se a tabela existe, a query terá 1 resultado. Senão, terá zero resultado.
    if len(resultados) == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    print('Insira suas credenciais no BD Oracle da FIAP.')
    usuario = input('username: ')
    senha = getpass('senha: ')  # é como input, mas esconde o que estou digitando

    conexao = abre_conexao(usuario, senha)
    print('Programa abriu conexão com o Banco de Dados.')
    
    cursor = conexao.cursor()
    
    if existe_tabela(cursor, 'ESTUDANTES'):
        print('A tabela ESTUDANTES foi encontrada. Prosseguindo.')
    else:
        print('A tabela ESTUDANTES não existe! Criando...')
        
        query_cria = '''
        CREATE TABLE ESTUDANTES (
            id NUMBER PRIMARY KEY,
            rm VARCHAR(10),
            nome VARCHAR(100),
            curso VARCHAR(100),
            turma VARCHAR(20)
        )
        '''
        cursor.execute(query_cria)
        
        print('Tabela criada. Prosseguindo.')

    em_execução = True
    while em_execução:
        print('Escolha uma opção:')
        print('0 - Encerrar programa')
        print('1 - Mostrar todos os dados da tabela')
        print('2 - Procurar estudante por nome')
        print('3 - Procurar estudante por RM')
        print('4 - Inserir novo dado na tabela')
        print('5 - Remover estudante por ID')
        print('6 - Destruir a tabela inteira')

        try:
            opcao = int(input())
        except:
            opcao = 0 # se der erro trato como opção de sair
        
        if opcao == 0:
            em_execução = False

        elif opcao == 1:
            mostra_todos_dados(cursor)
        
        elif opcao == 2:
            nome = input('Qual nome procurar na tabela? ')
            mostra_resultados_busca(cursor, nome)
        
        elif opcao == 3:
            rm = input('Qual RM procurar na tabela? ')
            mostra_resultados_busca_rm(cursor, rm)
        
        elif opcao == 4:
            insere_novo_dado(conexao, cursor)
        
        elif opcao == 5:
            try:
                id = int(input('Qual ID remover? '))
            except:
                print('ID inválido. Deve ser número.')
            
            remove_por_id(conexao, cursor, id)
        
        # Opção que eu não colocaria no programa normalmente.
        # Só está aqui para testarmos a criação da tabela depois!
        elif opcao == 6:
            confirmacao = input('Certeza que quer destruir a tabela? (S/N) ')
            if confirmacao == 'S':
                cursor.execute('DROP TABLE ESTUDANTES')
                conexao.commit()
                print('Tabela destruída. O programa será encerrado!')
                
                # Se a tabela é destruída, faz pouco sentido a execução continuar!
                em_execução = False
            
    
    print('Programa está encerrando...')
    cursor.close()
    conexao.close()
    print('Programa encerrado.')