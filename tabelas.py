from datetime import date, datetime, time
from os import linesep
import sqlite3
import time
from cores import Cores as co
from sqlite3 import Error
from main import limpar
from random import randint

def inserir_tipo_usuario(conn): 
    try:
        c = conn.cursor()
        c.execute("INSERT INTO TIPOS_USUARIO (SIGLA_USUARIO,  DESCRICAO_USUARIO) VALUES ('TEL','Telefonista'), ('CLI', 'Cliente')")
        conn.commit()
    except Error as e:
        print(f"ERRO {e} na hora de inserir na tabela TIPOS_USARIOS")
        time.sleep(7)

def atualizar_avaliacao(conn): #Atualiza a avaliação de cordo com os chamados completos, que estão cadastrados no cpf do cliente
    try:
        c = conn.cursor()
        cpf = input("Informe seu CPF para acharmos seus chamados:\n")
        tarefa_cpf = (cpf,)
        c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
        l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
        av.NOTA_AVALIACAO, av.DATA_AVALIACAO
        FROM CHAMADO c INNER JOIN LOCAIS l
        ON c.ID_LOCAIS = l.ID_LOCAIS
        INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO
        INNER JOIN USUARIO u on u.ID_USUARIO = c.ID_USUARIO
        WHERE u.CPF = ? and c.STATUS_CHAMADO = "Completo" and av.NOTA_AVALIACAO = 'VAZIO';""", tarefa_cpf)
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
        if resultado:
            id_avaliacao = input("Informe o id do Chamado que dejesa avaliar:\n")
            avaliacao = int(input("Adicione a Avaliação: "))
            while avaliacao < 0 or avaliacao > 10:
                print(f"{co.WARNING}\nA nota deve ser entre 0 e 10\n{co.ENDC}")
                avaliacao = int(input("Adicione a Avaliação: "))

            data = datetime.today()
            tarefa_inserir_avaliacao = (avaliacao, data, id_avaliacao)
            c.execute("""UPDATE AVALIACAO
            SET NOTA_AVALIACAO=?,
            DATA_AVALIACAO=?
            WHERE ID_CHAMADO=?""", tarefa_inserir_avaliacao)
            conn.commit()
        else: 
            print(f"{co.WARNING}\nNão tem chamados para avaliar\n{co.ENDC}")
    except Error as e:
        print(f"ERRO {e} ao atualizar avaliação")
        time.sleep(7)
    else:
        if resultado:
            print(f"{co.BOLD}{co.OKGREEN}Inserção com sucesso.{co.ENDC}")
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
        else:
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def inserir_local(conn): #Chamada quando precisar inserir um novo chamado
    try:
        c = conn.cursor()
        print("Descrição como: Casa, Empresa, Hospital, etc..\n")
        descricao = input("Descrição: ") 
        while descricao == "": #Verirfica se a escrição foi preenchida
            print("Descrição inaválida!\n")
            descricao = input("Descrição: ") 
        
        rua = input("Rua: ")
        while rua == "": #Verirfica se a Rua foi preenchida
            print("Rua inaválida!\n")
            rua = input("Rua: ")

        numero = input("Número: ")
        while len(numero) <= 0 or len(numero) > 4 or int(numero) < 0: #Verirfica se a número foi preenchido de forma correta
            print("Número inválido!\n")
            numero = input("Número: ")
        numero = int(numero)

        complemento = input("Complemento: ")
        if complemento == "": #Caso não insira complemento, o sistema insere vazio
            complemento = "VAZIO"
        
        cep = input("Informe o CEP sem o hífen: ")
        while len(cep) == 0 and len(cep) > 8: #Verirfica se a CEP foi preenchido de forma correta
            print("\nCEP inválido!\n")
            cep = input("Informe o CEP: ")
        cep = int(cep)
        
        cidade = input("Cidade: ")
        while cidade == "": #Verirfica se a Cidade foi preenchida
            print("Cidade inaválida!\n")
            cidade = input("Cidade: ")
        
        estado = input("Informe a sigla do Estado: ").upper()
        while estado != "AC" and estado != "AL" and estado != "Ap" and estado != "AM" and estado != "BA" and estado != "CE" and estado != "ES" and estado != "GO" and estado != "MA" and estado != "MT" and estado != "MS" and estado != "MG" and estado != "PA" and estado != "PB" and estado != "PR" and estado != "PI" and estado != "PE" and estado != "RJ" and estado != "RN" and estado != "RS" and estado != "RO" and estado != "RR" and estado != "SC" and estado != "SP" and estado != "SE" and estado != "TO" and estado != "DF": #Verifica se o Estado existe
            print("Estado Inválido")
            estado = input("Informe a sigla do Estado: ").upper()

        ponto_referencia = input("Ponto de Referência: ")
        if ponto_referencia == "": #Caso não insira ponto de referência, o sistema insere vazio
            ponto_referencia = "VAZIO"
        tarefa_inserir = (descricao, cep, cidade, estado, rua, numero, complemento, ponto_referencia)
        c.execute("INSERT INTO LOCAIS (DESCRICAO_LOCAIS, CEP_LOCAIS, CIDADE_LOCAIS, ESTADO_LOCAIS, ENDERECO_LOCAIS, NUMERO_LOCAIS, COMPLEMENTO, PONTO_REFERENCIA) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", tarefa_inserir)
        c.execute("SELECT ID_LOCAIS FROM LOCAIS;")
        resultado = c.fetchall()
        for item in range(len(resultado)):
            resultado[item]
        conn.commit()
    except Error as e:
        print(f"Erro {e} na hora de inserir dados na tabela LOCAIS")
        time.sleep(7)
    else:
        print(f"{co.BOLD}{co.OKGREEN}Inserção com sucesso.{co.ENDC}")
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
        return resultado[item][0] #Devolve o Id que vai ser acrescentado no chamado para referênciar o endereço

def chamados_para_atualizar(conn): #Vizualiza os chamados para a atualização
    try:
        c = conn.cursor()
        c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
        l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
        av.NOTA_AVALIACAO, av.DATA_AVALIACAO
        FROM CHAMADO c INNER JOIN LOCAIS l
        ON c.ID_LOCAIS = l.ID_LOCAIS
        INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO""")
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
        conn.commit()
    except Error as e:
        print(f"ERRO {e} na hora de mostrar dados da tabela CHAMADO")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}Pressione <ENTER> para continuar ...{co.ENDC}")
        return resultado[item][0]  

def vizualizar_usuarios(conn, tipo):
    try:
        c = conn.cursor()
        c.execute(f"SELECT u.ID_USUARIO, u.NOME, u.IDADE, u.CPF, t.SIGLA_USUARIO FROM USUARIO u inner join TIPOS_USUARIO t on u.SIGLA_USUARIO = t.SIGLA_USUARIO WHERE u.SIGLA_USUARIO = '{tipo}';")
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<3} {:<15} {:<10} {:<15} {:<15}".format("ID", "Nome", "Idade", "CPF", "Sigla"))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<3} {:<15} {:<10} {:<15} {:<15}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4]))
        conn.commit()   
    except Error as e:
        print(f"ERRO {e} na hora de mostrar dados da tabela USUARIO")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def vizualizar_chamados_cliente(conn): #Chamados com o cpf do cliente 
    try:
        c = conn.cursor()
        cpf = input("Informe seu CPF para acharmos seus chamados:\n")
        tarefa_cpf = (cpf,)
        c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
        l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
        av.NOTA_AVALIACAO, av.DATA_AVALIACAO
        FROM CHAMADO c INNER JOIN LOCAIS l
        ON c.ID_LOCAIS = l.ID_LOCAIS
        INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO
        INNER JOIN USUARIO u on u.ID_USUARIO = c.ID_USUARIO
        WHERE u.CPF = ?""", tarefa_cpf)
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
    except Error as e:
        print(f"ERRO {e} ao atualizar avaliação")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def vizualizar_chamados_incompletos(conn): #Vizuaiza chamados incompletos
    try:
        c = conn.cursor()
        c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL, l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO
        FROM CHAMADO c INNER JOIN LOCAIS l
        ON c.ID_LOCAIS = l.ID_LOCAIS
        WHERE c.STATUS_CHAMADO = "Incompleto";""")
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo local", "Cidade", "Rua", "Número", "Complemento"))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11]))
        conn.commit()
    except Error as e:
        print(f"ERRO {e} na hora de mostar chamados concluidos CHAMADO")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
        return resultado[item][0]

def vizualizar_chamados_completo(conn): #Chamados concluidos
    try:
        c = conn.cursor()
        c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
        l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
        av.NOTA_AVALIACAO, av.DATA_AVALIACAO
        FROM CHAMADO c INNER JOIN LOCAIS l
        ON c.ID_LOCAIS = l.ID_LOCAIS
        INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO
        WHERE c.STATUS_CHAMADO = "Completo";""")
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<2} {:<15} {:<5} {:<5} {:<10} {:<8} {:<15} {:<15} {:<10} {:<10} {:<25} {:<5} {:<2} {:<5}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Nome Cli.", "Tipo local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", "Data Avaliação"))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<2} {:<15} {:<5} {:<5} {:<10} {:<8} {:<15} {:<15} {:<10} {:<10} {:<25} {:<5} {:<2} {:<5} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13], resultado[item][14]))
        conn.commit()
    except Error as e:
        print(f"ERRO {e} na hora de mostar chamados concluidos CHAMADO")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def vizualizar_local_chamado(conn): #Para Vizualizar Locais na hora de atualizar local do chamado
    try:
        c = conn.cursor()
        c.execute("""SELECT l.ID_LOCAIS, c.ID_CHAMADO, l.DESCRICAO_LOCAIS, l.CEP_LOCAIS, l.CIDADE_LOCAIS, l.ESTADO_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO, l.PONTO_REFERENCIA
        FROM LOCAIS l INNER JOIN CHAMADO c ON c.ID_LOCAIS = l.ID_LOCAIS;""")
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<3} {:<3} {:<15} {:<11} {:<20} {:<4} {:<20} {:<4} {:<2} {:<10}".format("ID", "ID Chamados", "Tipo", "CEP", "Cidade", "Estado", "Rua", "Número", "Complemento", "Referência"))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<3} {:<3} {:<15} {:<15} {:<20} {:<4} {:<20} {:<4} {:<2} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9]))
        conn.commit()
    except Error as e:
        print(f"ERRO {e} na hora de mostrar local da tabela CHAMADO")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
        return resultado[item][0]
        
def vizualizar_local(conn): #Para Vizualizar Locais na hora de atualizar local do chamado
    try:
        c = conn.cursor()
        c.execute("""SELECT DRECRICAO_LOCAIS, CEP_LOCAIS, CIDADE_LOCAIS, ESTADO_LOCAIS, ENDERECO_LOCAIS, NUMERO_LOCAIS, COPLEMENTO_LOCAIS, PONTO_REFERENCIA FROM LOCAIS;""")
        resultado = c.fetchall()
        print(f"{co.BOLD}{co.OKGREEN}")
        print("{:<6} {:<6} {:<15} {:<5} {:<5} {:<10} {:<8} {:<8}".format("Descrição", "CEP", "Cidade", "Estado.", "Rua", "Número", "Complemento", "Ponto Referência"))
        print(f"{co.ENDC} ")
        for item in range(len(resultado)):
            print("{:<6} {:<6} {:<15} {:<5} {:<5} {:<10} {:<8} {:<8}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8]))
        conn.commit()
    except Error as e:
        print(f"ERRO {e} na hora de mostrar dados da tabela LOCAIS")
        time.sleep(7)
    else:
        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def inserir(conn, tabela): #Opcao inserir no Sub Menu
    if tabela == "Usuario":
        try:
            c = conn.cursor()
            nome_usuario = input("Informe o Nome:")
            while nome_usuario == "": #Verifica se o nome foi digitado
                print("Nome inválido!!")
                nome_usuario = input("\nInforme o Nome:")
        
            idade_usuario = input("Informe a Idade: ")
            while len(str(idade_usuario)) == 0 or int(idade_usuario) <= 0 or int(idade_usuario) > 100: #Verifica se a idade foi digitada de forma correta
                print("Idade inválida!!") 
                idade_usuario = input("\nInforme a Idade: ")
            idade_usuario = int(idade_usuario)

            cpf_valido = False
            while cpf_valido != True: #Verifica se o CPF é valido
                cpf = input("Entre com seu CPF com ponto e hífen: ")

                while len(cpf) < 14: #Verifica o tamanho do cpf
                    print("\nO CPF que foi informado, não segue o padrão pedido\n")
                    cpf = input("Entre com seu CPF com ponto e hífen: ")

                while cpf[3] != "." and cpf[7] != "." and cpf[11] != "-": 
                    if cpf[3] and cpf[7] != "." and cpf[11] != "-":
                        print("O cpf que foi informado, não segue o padrão pedido")
                    
                    cpf = input("Digite o cpf novamente: ")

                list(cpf)
                carac = int(cpf[0])
                carac1 = int(cpf[1])
                carac2 = int(cpf[2])
                carac3 = int(cpf[4])
                carac4 = int(cpf[5])
                carac5 = int(cpf[6])
                carac6 = int(cpf[8])
                carac7 = int(cpf[9])
                carac8 = int(cpf[10])

                valid1 = int(cpf[12])
                valid2 = int(cpf[13])

                soma1 = carac *10 + carac1 *9 + carac2 *8 + carac3 *7 + carac4 *6 + carac5 *5 + carac6 *4 + carac7 *3 + carac8 *2
                result1 = soma1 * 10 %11

                soma2 = carac *11 + carac1 *10 + carac2 *9 + carac3 *8 + carac4 *7 + carac5 *6 + carac6 *5 + carac7 *4 + carac8 *3 + result1 *2
                result2 = soma2 *10 %11

                if result1 == 10:
                    result1 = 0

                if result2 == 10:
                    result2 = 0

                if result1 != valid1 and result2 != valid2:
                    print(f"O cpf {cpf} não é válido!")
                    cpf_valido = False
                else:
                    cpf_valido = True

            sigla_usuario = input("Infrme se é Cliente ou Telefonista: ")
            sigla_usuario = sigla_usuario[0:3].upper()
            tarefa_inserir_usuario = (nome_usuario, idade_usuario, cpf, sigla_usuario)
            c.execute("INSERT INTO USUARIO (NOME, IDADE, CPF, SIGLA_USUARIO) VALUES (?, ?, ?, ?)", (tarefa_inserir_usuario))
            c.execute("SELECT ID_USUARIO FROM USUARIO;")
            resultado = c.fetchall()
            for item in range(len(resultado)):
                resultado[item]
            conn.commit()
        except Error as e:
            print(f"ERRO {e} na hora de inserir na tabela USUARIO")
            time.sleep(7)
        else:
            print(f"{co.BOLD}{co.OKGREEN}Inserção com sucesso.{co.ENDC}")
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
            return resultado[item][0]
    else: 
        try:
            c = conn.cursor()
            descricao_chamado = input("O que está acontecendo?\n")
            while descricao_chamado == "": #Verifica se a descrição foi preenchida
                print("\nDescrição inválida!\n")
                descricao_chamado = input("O que está acontecendo?\n")

            data_solicitacao = date.today() #Adiciona a data atual
            id_local = inserir_local(conn)
            print("1. Cadastrar novo cliente\n2. Usar um existente\n\n")
            resposta_para_usuario = int(input("escolha a opção: "))
            
            if resposta_para_usuario == 1:
                id_usuario = inserir(conn, "Usuario")
            else:
                vizualizar_usuarios(conn, "CLI")
                id_usuario = input("Qual o Id do usuário a cadastrar: ")

            vizualizar_usuarios(conn, "TEL")
            id_tel = input("Informe o Id do Telefonista: ")
            c.execute(f"SELECT NOME FROM USUARIO  SIGLA_USUARIO = 'TEL' AND ID_USUARIO = {id_tel};") #Pega o Nome do Telefonista
            resultado_tel = c.fetchall()
            for x in range(len(resultado_tel)):
                resultado_tel[x]
            nome_tel = resultado_tel[x][0]

            dt_conclusao = "VAZIO"
            status = "Incompleto"
            acoes = "VAZIO"
            tarefa_inserir_chamado = (descricao_chamado, data_solicitacao, id_local, id_usuario, nome_tel, dt_conclusao, acoes, status)
            c.execute("INSERT INTO CHAMADO (DESCRICAO_CHAMADO, DATA_SOLICITACAO, ID_LOCAIS, ID_USUARIO, NOME_TEL, DATA_CONCLUSAO, ACOES_REALIZADAS, STATUS_CHAMADO) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", tarefa_inserir_chamado)
            c.execute("SELECT ID_CHAMADO FROM CHAMADO;")
            resultado = c.fetchall()
            for item in range(len(resultado)):
                resultado[item]
            id_para_avaliacao = resultado[item][0]
            data_avaliacao = "VAZIO"
            nota = "VAZIO"
            tarefa_inserir_avaliacao = (nota, data_avaliacao, id_para_avaliacao)
            c.execute("INSERT INTO AVALIACAO (NOTA_AVALIACAO, DATA_AVALIACAO, ID_CHAMADO) VALUES (?, ?, ?)", tarefa_inserir_avaliacao)
            conn.commit()
        except Error as e:
            print(e)
            time.sleep(7)
        else:
            print(f"{co.BOLD}{co.OKGREEN}Inserção com sucesso.{co.ENDC}")
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def vizualizar(conn, tabela): #Opção vizualizar no sub menu
    if tabela == "Usuario":    
        try:
            c = conn.cursor()
            c.execute("SELECT u.ID_USUARIO, u.NOME, u.IDADE, u.CPF, t.SIGLA_USUARIO FROM USUARIO u inner join TIPOS_USUARIO t on u.SIGLA_USUARIO = t.SIGLA_USUARIO;")
            resultado = c.fetchall()
            print(f"{co.BOLD}{co.OKGREEN}")
            print("{:<3} {:<15} {:<10} {:<15} {:<15}".format("ID", "Nome", "Idade", "CPF", "Sigla"))
            print(f"{co.ENDC} ")
            for item in range(len(resultado)):
                print("{:<3} {:<15} {:<10} {:<15} {:<15}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4]))
            conn.commit()
        except Error as e:
            print(f"ERRO {e} na hora de mostrar dados da tabela USUARIO")
            time.sleep(7)
        else:
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
    else:
        op_vizualizacao = input("Quer vizualizar os chamados, sem avaliação, com nota maior ou menor que 5?\nOu pressione Enter para ver todos os Chamados.\n").upper()
        op_vizualizacao = op_vizualizacao[0:3]

        if op_vizualizacao == "MAI": #Mostra Chamdos avaiados com a nota maior que 5
            try:
                c = conn.cursor()
                c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
                l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
                av.NOTA_AVALIACAO, av.DATA_AVALIACAO
                FROM CHAMADO c INNER JOIN LOCAIS l
                ON c.ID_LOCAIS = l.ID_LOCAIS
                INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO WHERE NOTA_AVALIACAO > 5 AND STATUS_CHAMADO = 'Completo' AND NOTA_AVALIACAO <> 'VAZIO';""")
                resultado = c.fetchall()
                print(f"{co.BOLD}{co.OKGREEN}")
                print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
                print(f"{co.ENDC} ")
                for item in range(len(resultado)):
                    print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
                conn.commit()
            except Error as e:
                print(f"ERRO {e} na hora de mostrar dados da tabela CHAMADO")
                time.sleep(7)
            else:
                input(f"{co.BOLD}{co.OKBLUE}Pressione <ENTER> para continuar ...{co.ENDC}")

        elif op_vizualizacao == "MEN": #Mostra Chamados avaliados com a nota menor que ou igual 5
            try:
                c = conn.cursor()
                c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
                l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
                av.NOTA_AVALIACAO, av.DATA_AVALIACAO
                FROM CHAMADO c INNER JOIN LOCAIS l
                ON c.ID_LOCAIS = l.ID_LOCAIS
                INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO WHERE NOTA_AVALIACAO <= 5 AND c.STATUS_CHAMADO = 'Completo';""")
                resultado = c.fetchall()
                print(f"{co.BOLD}{co.OKGREEN}")
                print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
                print(f"{co.ENDC} ")
                for item in range(len(resultado)):
                    print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
                conn.commit()
            except Error as e:
                print(f"ERRO {e} na hora de mostrar dados da tabela CHAMADO")
                time.sleep(7)
            else:
                input(f"{co.BOLD}{co.OKBLUE}Pressione <ENTER> para continuar ...{co.ENDC}")   
                    
        elif op_vizualizacao == "SEM": #Mostra Chamados sem Avaliação
            try:
                c = conn.cursor()
                c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
                l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
                av.NOTA_AVALIACAO, av.DATA_AVALIACAO
                FROM CHAMADO c INNER JOIN LOCAIS l
                ON c.ID_LOCAIS = l.ID_LOCAIS
                INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO WHERE NOTA_AVALIACAO = 'VAZIO' AND c.STATUS_CHAMADO = 'Completo'""")
                resultado = c.fetchall()
                print(f"{co.BOLD}{co.OKGREEN}")
                print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
                print(f"{co.ENDC} ")
                for item in range(len(resultado)):
                    print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
                conn.commit()
            except Error as e:
                print(f"ERRO {e} na hora de mostrar dados da tabela CHAMADO")
                time.sleep(7)
            else:
                input(f"{co.BOLD}{co.OKBLUE}Pressione <ENTER> para continuar ...{co.ENDC}")
            
        else:
            try: #Mostra chamados 
                c = conn.cursor()
                c.execute("""SELECT c.ID_CHAMADO, c.DESCRICAO_CHAMADO, c.DATA_CONCLUSAO, c.DATA_SOLICITACAO, c.ACOES_REALIZADAS, c.STATUS_CHAMADO, c.NOME_TEL,
                l.DESCRICAO_LOCAIS, l.CIDADE_LOCAIS, l.ENDERECO_LOCAIS, l.NUMERO_LOCAIS, l.COMPLEMENTO,
                av.NOTA_AVALIACAO, av.DATA_AVALIACAO
                FROM CHAMADO c INNER JOIN LOCAIS l
                ON c.ID_LOCAIS = l.ID_LOCAIS
                INNER JOIN AVALIACAO av on av.ID_CHAMADO = c.ID_CHAMADO""")
                resultado = c.fetchall()
                print(f"{co.BOLD}{co.OKGREEN}")
                print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format("ID", "Descrição", "Data Con.", "Data Soli.", "Ações", "Status", "Nome Tel.", "Tipo Local", "Cidade", "Rua", "Número", "Complemento", "Avaliação", ))
                print(f"{co.ENDC} ")
                for item in range(len(resultado)):
                    print("{:<2} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<7} {:<12} {:<10}".format(resultado[item][0], resultado[item][1], resultado[item][2], resultado[item][3], resultado[item][4], resultado[item][5], resultado[item][6], resultado[item][7], resultado[item][8], resultado[item][9], resultado[item][10], resultado[item][11], resultado[item][12], resultado[item][13]))
                conn.commit()
            except Error as e:
                print(f"ERRO {e} na hora de mostrar dados da tabela CHAMADO")
                time.sleep(7)
            else:
                input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
    
def excluir(conn, tabela): #Função Excluir
    if tabela == "Usuario":
        try:
            c = conn.cursor()
            vizualizar(conn, tabela)
            id_excluir = int(input("\n\nInforme o ID do Usúario a excluir: "))
            tarefa_excluir = (id_excluir,)
            c.execute("DELETE FROM USUARIO WHERE ID_USUARIO=?;", tarefa_excluir)
            conn.commit()
        except Error as e:
            print(f"ERRO {e} na hora de excluir um usuário da tabela USUARIO")
            time.sleep(7)
        else:
            print(f"{co.BOLD}{co.OKGREEN}Exclusão com sucesso{co.ENDC}")
            input(f"{co.BOLD}{co.OKBLUE}Pressione <ENTER> para continuar ...{co.ENDC}")
    else:
        try:
            c = conn.cursor()
            vizualizar_chamados_completo(conn)
            id_excluir = int(input("\n\nInforme o ID do Chamado a excluir: "))
            tarefa_excluir = (id_excluir,)
            c.execute("DELETE FROM CHAMADO WHERE ID_CHAMADO=?;", tarefa_excluir)
            conn.commit()
        except Error as e:
            print(f"ERRO {e} na hora de excluir um chamado da tabela CHAMADO")
            time.sleep(7)
        else:
            print(f"{co.BOLD}{co.OKGREEN}\nExclusão com sucesso{co.ENDC}")
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

def atualizar(conn, tabela): #Atualizar
    if tabela == "Usuario": #Atualizar Dados na tabela Usuario
        vizualizar(conn, tabela)
        opcao_atualizar = None
        while opcao_atualizar != "NOM" and opcao_atualizar != "IDA" and opcao_atualizar != "CPF" and opcao_atualizar != "SIG":
            opcao_atualizar = input("Qual dado quer atualizar?\n").upper()
            opcao_atualizar = opcao_atualizar[0:3]

            if opcao_atualizar == "NOM": #Atualizar Nome
                try:
                    c = conn.cursor()
                    limpar()
                    vizualizar(conn, tabela)
                    id_atualizar = int(input("\n\nInforme o Id do Nome a atualizar: "))
                    nome_atualizar = input("\nNovo Nome: ").title()
                    tarefa_atualizar_nome = (nome_atualizar, id_atualizar)
                    c.execute("UPDATE USUARIO SET NOME=? WHERE ID_USUARIO=?;", tarefa_atualizar_nome)
                    conn.commit()
                except Error as e:
                    print(f"ERRO {e} na hora de atualizar o nome da tebela USUARIO")
                    time.sleep(7)
                else:
                    print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                    input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

            elif opcao_atualizar == "IDA": #Atualizar Idade
                try:
                    c = conn.cursor()
                    limpar()
                    vizualizar(conn, tabela)
                    id_atualizar = int(input("\n\nInforme o Id da Idade a atualizar: "))
                    nome_atualizar = input("\nNova Idade: ").title()
                    tarefa_atualizar_nome = (nome_atualizar, id_atualizar)
                    c.execute("UPDATE USUARIO SET IDADE=? WHERE ID_USUARIO=?;", tarefa_atualizar_nome)
                    conn.commit()
                except Error as e:
                    print(f"ERRO {e} na hora de atualizar a Idade da tabela USUARIO")
                    time.sleep(7)
                else:
                    print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                    input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

            elif opcao_atualizar == "CPF": #Atualizar CPF
                try:
                    c = conn.cursor()
                    limpar()
                    vizualizar(conn, tabela)
                    id_atualizar = int(input("\n\nInforme o Id do CPF a atualizar: "))
                    cpf_valido = False
                    while cpf_valido != True: #Verifica se o CPF é valido
                        cpf = input("Entre com o novo CPF com ponto e hífen: ")

                        while len(cpf) < 14:
                            print("\nO CPF que foi informado, não segue o padrão pedido\n")
                            cpf = input("Entre com seu CPF com ponto e hífen: ")

                        while cpf[3] != "." and cpf[7] != "." and cpf[11] != "-": 
                            if cpf[3] and cpf[7] != "." and cpf[11] != "-":
                                print("O cpf que foi informado, não segue o padrão pedido")
                            
                            cpf = input("Digite o cpf novamente: ")
                            
                        list(cpf)  

                        carac = int(cpf[0])
                        carac1 = int(cpf[1])
                        carac2 = int(cpf[2])
                        carac3 = int(cpf[4])
                        carac4 = int(cpf[5])
                        carac5 = int(cpf[6])
                        carac6 = int(cpf[8])
                        carac7 = int(cpf[9])
                        carac8 = int(cpf[10])

                        valid1 = int(cpf[12])
                        valid2 = int(cpf[13])

                        soma1 = carac *10 + carac1 *9 + carac2 *8 + carac3 *7 + carac4 *6 + carac5 *5 + carac6 *4 + carac7 *3 + carac8 *2
                        result1 = soma1 * 10 %11

                        soma2 = carac *11 + carac1 *10 + carac2 *9 + carac3 *8 + carac4 *7 + carac5 *6 + carac6 *5 + carac7 *4 + carac8 *3 + result1 *2
                        result2 = soma2 *10 %11

                        if result1 == 10:
                            result1 = 0

                        if result2 == 10:
                            result2 = 0

                        if result1 != valid1 and result2 != valid2:
                            print(f"O cpf {cpf} não é válido!")
                            cpf_valido = False
                        else:
                            cpf_valido = True
                    
                    tarefa_atualizar_nome = (cpf, id_atualizar)
                    c.execute("UPDATE USUARIO SET CPF=? WHERE ID_USUARIO=?;", tarefa_atualizar_nome)
                    conn.commit()
                except Error as e:
                    print(f"ERRO {e} na hora de atualizar o CPF da tabela USUARIO")
                    time.sleep(7)
                else:
                    print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                    input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")

            elif opcao_atualizar == "SIG": #Atualizar Sigla
                try:
                    c = conn.cursor()
                    limpar()
                    vizualizar(conn, tabela)
                    id_atualizar = int(input("\n\nInforme o Id da Sigla a atualizar: "))
                    nome_atualizar = input("\nNova Sigla: ").title()
                    tarefa_atualizar_nome = (nome_atualizar, id_atualizar)
                    c.execute("UPDATE USUARIO SET SIGLA_USUARIO=? WHERE ID_USUARIO=?;", tarefa_atualizar_nome)
                    conn.commit()
                except Error as e:
                    print(f"ERRO {e} na hora de atualizar a Sigla da tabela USUARIO")
                    time.sleep(7)
                else:
                    print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                    input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
    
            else:
                print(f"{co.BOLD}{co.WARNING}\nOpção Inválida\n{co.ENDC}")

    else: #Atualizar Dados na Tabela Chamado
        chamados_para_atualizar(conn) 
        opcao_atualizar = None
        while opcao_atualizar != "DES" and opcao_atualizar != "ACA" and opcao_atualizar != "DAT" and opcao_atualizar != "LOC":
            opcao_atualizar = input("Qual dado quer atualizar?\n").upper()
            opcao_atualizar = opcao_atualizar[0:3]

            if opcao_atualizar == "DES": #Atualizar Descrição
                try:
                    c = conn.cursor()
                    id_atualizar = int(input("Informe qual o ID da descrição a atualizar: "))
                    retorno_id = chamados_para_atualizar(conn)
                    for x in range(1, retorno_id + 1): #Valida se o ID escolhido existe ou não
                        if x == id_atualizar:
                            descricao_atualizar = input("\nNova Descrição: ").title()
                            tarefa_atualizar_descricao = (descricao_atualizar, id_atualizar)
                            c.execute("UPDATE CHAMADO SET DESCRICAO_CHAMADO=? WHERE ID_CHAMADO=?;", tarefa_atualizar_descricao)
                            conn.commit()
                            saida = "SIM"

                except Error as e:
                    print(f"ERRO {e} na hora de atualizar a descrição da tabela CHAMADO")
                    time.sleep(7)
                else:
                    if saida == "SIM":
                        print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
                    else:
                         print(f"{co.BOLD}{co.WARNING}\nID não existe\n{co.ENDC}")

            elif opcao_atualizar == "AÇA" or opcao_atualizar == "ACA": #Atualizar Acões
                try:
                    c = conn.cursor()
                    id_atualizar = int(input("Informe qual o ID da descrição a atualizar: "))
                    retorno_id = chamados_para_atualizar(conn)
                    for x in range(1, retorno_id + 1): #Valida se o ID escolhido existe ou não
                        if x == id_atualizar:
                            acao_atualizar = input("\nNova Ação: ").title()
                            tarefa_atualizar_acao = (acao_atualizar, id_atualizar)
                            c.execute("UPDATE CHAMADO SET ACOES_REALIZADAS=? WHERE ID_CHAMADO=?;", tarefa_atualizar_acao)
                            conn.commit()
                            saida = "SIM"

                except Error as e:
                    print(f"ERRO {e} na hora de atualizar a ação da tabela CHAMADO")
                    time.sleep(7)
                else:
                    if saida == "SIM":
                        print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
                    else:
                         print(f"{co.BOLD}{co.WARNING}\nID não existe\n{co.ENDC}")

            elif opcao_atualizar == "DAT": #Atualizar Data de Conclusão
                try:
                    c = conn.cursor()
                    id_atualizar = int(input("Informe qual o ID da descrição a atualizar: "))
                    retorno_id = chamados_para_atualizar(conn)
                    for x in range(1, retorno_id + 1): #Valida se o ID escolhido existe ou não
                        if x == id_atualizar:
                            data_atualizar = input("\nNova Data: ")
                            tarefa_atualizar_data = (data_atualizar, id_atualizar)
                            c.execute("UPDATE CHAMADO SET DATA_CONCLUSAO =? WHERE ID_CHAMADO=?;", tarefa_atualizar_data)
                            conn.commit()
                            saida = "SIM"
                    
                except Error as e:
                    print(f"ERRO {e} na hora de atualizar a Data de Conclusão da tabela CHAMADO")
                    time.sleep(7)
                else:
                    if saida == "SIM":
                        print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
                    else:
                         print(f"{co.BOLD}{co.WARNING}\nID não existe\n{co.ENDC}")

            elif opcao_atualizar == "LOC": #Atulaizar Local
                try:
                    c = conn.cursor()
                    id_atualizar = int(input("\n\nInforme o Id do Local a atualizar: "))
                    retorno_id = vizualizar_local_chamado(conn)
                    for x in range(1, retorno_id + 1): #Valida se o ID escolhido existe ou não
                        if x == id_atualizar:
                            limpar()
                            vizualizar_local_chamado(conn)
                            dado_atualizar = None
                            while dado_atualizar != "DES" and dado_atualizar != "CEP" and dado_atualizar != "CID" and dado_atualizar != "EST" and dado_atualizar != "END" and dado_atualizar != "NUM" and dado_atualizar != "COM" and dado_atualizar != "PON":
                                dado_atualizar = input("Qual dado dejesa atualizar?\n").upper() #Escolhe qual coluna vai atualizar
                                dado_atualizar = dado_atualizar[0:3]

                                if dado_atualizar == "DES":
                                    nome_coluna = "DESCRICAO_LOCAIS"
                                    dado_atualizar_local = input("Nova Descrição: ")
                                elif dado_atualizar =="CEP":
                                    nome_coluna = "CEP_LOCAIS"
                                    dado_atualizar_local = input("Novo CEP: ")
                                elif dado_atualizar =="CID":
                                    nome_coluna = "CIDADE_LOCAIS"
                                    dado_atualizar_local = input("Nova Cidade: ")
                                elif dado_atualizar =="EST":
                                    nome_coluna = "ESTADO_LOCAIS"
                                    dado_atualizar_local = input("Novo Estado: ")
                                elif dado_atualizar =="END":
                                    nome_coluna = "ENDERECO_LOCAIS"
                                    dado_atualizar_local = input("Nova Rua: ")
                                elif dado_atualizar =="NUM":
                                    nome_coluna = "NUMERO_LOCAIS"
                                    dado_atualizar_local = input("Novo Número: ")
                                elif dado_atualizar =="COM":
                                    nome_coluna = "COMPLEMENTO_LOCAIS"
                                    dado_atualizar_local = input("Novo Complemento: ")
                                elif dado_atualizar =="PON":
                                    nome_coluna = "PONTO_REFERENCIA"
                                    dado_atualizar_local = input("Nova Referência: ")
                                else:
                                    print(f"{co.BOLD}{co.WARNING}\nOpção Inválida\n{co.ENDC}")

                            tarefa_atualizar = (dado_atualizar_local, id_atualizar)
                            c.execute(f"UPDATE LOCAIS SET {nome_coluna}=? WHERE ID_LOCAIS=?;", tarefa_atualizar)
                            conn.commit()
                            saida = "SIM"

                except Error as e:
                    print(f"ERRO {e} na hora de atualizar a Local da tabela CHAMADO")
                    time.sleep(7)
                else:
                    if saida == "SIM":
                        print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
                        input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
                    else:
                        print(f"{co.BOLD}{co.WARNING}\nID não existe\n{co.ENDC}")
            
            elif opcao_atualizar == "STA":
                print(f"{co.BOLD}{co.WARNING}\nPara Atualizar o Status Entre na opçaõ 5 do Menu de Chamados !{co.ENDC}")
                input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
            else:
                print(f"{co.BOLD}{co.WARNING}\nOpção Inválida\n{co.ENDC}")

def atulizar_status(conn):
    try:
        limpar()
        retorno_id = vizualizar_chamados_incompletos(conn)
        resposta = input("Realmente vai Fechar um chamado?\n").upper()
        if resposta == "SIM":
            c = conn.cursor()
            id = input("Qual o id do Status a atualizar?\n")
            acoes = input("Quais ações foram executadas?\n")
            status = "Completo"
            data_hoje = date.today()
            tarefa_atualizar_status = (acoes, status, data_hoje, id)
            c.execute("""UPDATE CHAMADO 
            SET
            ACOES_REALIZADAS=?,
            STATUS_CHAMADO=?,
            DATA_CONCLUSAO=?
            WHERE ID_CHAMADO=? """, tarefa_atualizar_status)
            conn.commit()
        else:
            pass
    except Error as e:
        print(f"ERRO {e} na hora de atualizar status da tabela CHAMADO")
        time.sleep(7)
    else:
        if resposta == "SIM":
            print(f"{co.BOLD}{co.OKGREEN}\nAtualização com sucesso{co.ENDC}")
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")
        else:
            input(f"{co.BOLD}{co.OKBLUE}\nPressione <ENTER> para continuar ...{co.ENDC}")