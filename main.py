import sqlite3
from sqlite3 import Error
import time
import schema
import tabelas
from cores import Cores as co

def limpar(): #Função para limpar a Tela
    import os
    from time import sleep
    
    def screen_clear():
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            _ = os.system('cls')
    
    sleep(1)
    screen_clear()

def menu_principal(): #Menu Principal
    selecao = ""  
    
    while selecao != 2 and selecao != 1 and selecao !=0:    
        print(55 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}{co.OKGREEN}\t\t\tMENU{co.ENDC}")
        print(55 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}1. Ambiante do Cliente{co.ENDC}")
        print(f"{co.BOLD}2. Ambiante do Telefonista{co.ENDC}")
        print(f"{co.BOLD}{co.FAIL}0. Sair{co.ENDC}")
        selecao = int(input("Selecione uma opção: "))
        if selecao != 1 and selecao != 2 and selecao != 0:
            print(f"\n\n{co.WARNING}Opção Inválida!{co.ENDC}\n\n")
            time.sleep(2)
            limpar()
    return selecao

def menu_cliente(): #Menu Cliente, que é apenas para adionar a avialção
    selecao = ""  
    
    while selecao != 2 and selecao != 1 and selecao !=0:    
        print(65 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}{co.OKGREEN}\t\t\tAMBIANTE CLIENTE{co.ENDC}")
        print(65 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}1. Adicionar avaliação{co.ENDC}")
        print(f"{co.BOLD}2. Ver Chamados {co.ENDC}")
        print(f"{co.BOLD}{co.FAIL}0. Voltar{co.ENDC}")
        selecao = int(input("Selecione uma opção: "))
        if selecao != 1 and selecao != 2 and selecao != 0:
            print(f"\n\n{co.WARNING}Opção Inválida!{co.ENDC}\n\n")
            time.sleep(2)
            limpar()
         
    return selecao

def menu_telefonista(): #Menu do Telefonista
    selecao = ""  
    
    while selecao != 2 and selecao != 1 and selecao !=0:    
        print(70 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}{co.OKGREEN}\t\t\tAMBIENTE TELEFONISTA{co.ENDC}")
        print(70 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}1. Chamados{co.ENDC}")
        print(f"{co.BOLD}2. Usuários{co.ENDC}")
        print(f"{co.BOLD}{co.FAIL}0. Voltar{co.ENDC}")
        selecao = int(input("Selecione uma opção: "))
        if selecao != 1 and selecao != 2 and selecao != 0:
            print(f"\n\n{co.WARNING}Opção Inválida!{co.ENDC}\n\n")
            time.sleep(2)
            limpar()
         
    return selecao

def sub_Menu(tabela): #Menu da Chamados ou Usuarios
    selecao_sub_menu = ""

    while selecao_sub_menu != 1 and selecao_sub_menu != 2 and selecao_sub_menu != 3 and selecao_sub_menu != 4 and selecao_sub_menu != 5 and selecao_sub_menu != 6 and selecao_sub_menu != 0:
        print(60 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}{co.OKGREEN}\t\t\tMENU {tabela}{co.ENDC}")
        print(60 * f"{co.OKGREEN}*{co.ENDC}")
        print(f"{co.BOLD}1. Novo {tabela}{co.ENDC}")
        print(f"{co.BOLD}2. Vizualizar {tabela}{co.ENDC}")
        print(f"{co.BOLD}3. Atualizar {tabela}{co.ENDC}")
        print(f"{co.BOLD}4. Excluir {tabela}{co.ENDC}")
        if tabela == "Chamados":  #Opção para quando escolher o Menu Chamado
            print(f"{co.BOLD}5. {tabela} em Aberto{co.ENDC}")

        print(f"{co.BOLD}{co.FAIL}0. Voltar{co.ENDC}")
        selecao_sub_menu = int(input("Selecione uma Opção: "))
        if selecao_sub_menu != 1 and selecao_sub_menu != 2 and selecao_sub_menu != 3 and selecao_sub_menu != 4 and selecao_sub_menu != 5 and selecao_sub_menu != 6 and selecao_sub_menu != 0:
            print(f"\n\n{co.WARNING}Opção Inválida!{co.ENDC}\n\n")
            time.sleep(2)
            limpar()

    return selecao_sub_menu

def criando_conexao(): #Crinando conexão com o banco de dados
    conn = None
    try:
        conn = sqlite3.connect("Projeto_LP2")
        conn.execute("PRAGMA foreing_key = ON")
        return conn

    except Error as e:
        print(e)

if __name__ == "__main__":
    schema.criar_tabelas()
    nome_banco = criando_conexao()
    #tabelas.inserir_tipo_usuario(nome_banco) #Usar só uma vez
    limpar()
    op_menu_principal = menu_principal()
    while op_menu_principal !=0:    
        
        if op_menu_principal == 2: #Sub Menu Telefonista
            limpar()
            opcao = menu_telefonista() #Escolha do menu seguinte se ai ser o menu de chamados ou usuários
            while opcao != 0:
                if opcao == 1: 
                    limpar()
                    tabela = "Chamados"
                elif opcao == 2:
                    limpar()
                    tabela = "Usuario"
                
                op_sub_menu = sub_Menu(tabela)
                limpar()
                while op_sub_menu != 0: #Sub Menu Chamdos ou Usuario
                    if op_sub_menu == 1: #Area para abrir um novo chamado ou usuário
                        print(25 * f"{co.OKGREEN}*{co.ENDC}", f"{co.BOLD}{co.OKGREEN}Inserir Novo {tabela}{co.ENDC}", 25 * f"{co.OKGREEN}*{co.ENDC}", "\n\n")
                        tabelas.inserir(nome_banco, tabela)
                    elif op_sub_menu == 2: #Area Vizualizar dados dos chamados ou dos usuários
                        tabelas.vizualizar(nome_banco, tabela)
                    elif op_sub_menu == 3: #Area para atualizar dados dos chamados ou dos usuários
                        print(25 * f"{co.OKGREEN}*{co.ENDC}", f"{co.BOLD}{co.OKGREEN}Atualizar {tabela}{co.ENDC}", 25 * f"{co.OKGREEN}*{co.ENDC}", "\n\n")
                        tabelas.atualizar(nome_banco, tabela)
                    elif op_sub_menu == 4: #Area para excluir chamados ou usuários
                        print(25 * f"{co.OKGREEN}*{co.ENDC}", f"{co.BOLD}{co.OKGREEN}Excluir {tabela}{co.ENDC}", 25 * f"{co.OKGREEN}*{co.ENDC}", "\n\n")
                        tabelas.excluir(nome_banco, tabela)
                    elif op_sub_menu == 5: #Area para fechar os chamados que foram concluidos
                        print(25 * f"{co.OKGREEN}*{co.ENDC}", f"{co.BOLD}{co.OKGREEN}Fechar {tabela}{co.ENDC}", 25 * f"{co.OKGREEN}*{co.ENDC}", "\n\n")
                        tabelas.atulizar_status(nome_banco)
                    else:
                        print("Opção Inválida!")
                    
                    limpar()
                    op_sub_menu = sub_Menu(tabela)
                    limpar()
                
                opcao = menu_telefonista()
                limpar()
            
            limpar()
            op_menu_principal = menu_principal()

        else: #Sub Menu Clientes 
            limpar()
            op_menu_cliente = menu_cliente()
            while op_menu_cliente != 0:    
                
                if op_menu_cliente == 1: #Area para inserir avaliações dos chamados dos clientes. 
                    limpar()
                    tabelas.atualizar_avaliacao(nome_banco)
                elif op_menu_cliente == 2: #Area para vizualizar todos os chamados dos clientes.
                    limpar()
                    tabelas.vizualizar_chamados_cliente(nome_banco)
                
                limpar()
                op_menu_cliente = menu_cliente()

            limpar()
            op_menu_principal = menu_principal()  

    else:
        print(f"{co.WARNING}SAINDO.......{co.ENDC}")
    