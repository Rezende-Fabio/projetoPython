from os import error
import sqlite3
from sqlite3 import Error


def criar_tabelas():
    
    conn = sqlite3.connect("Projeto_LP2")
    c = conn.cursor()

    try: #Criando a tabela Tipos Usuarios
        c.execute("""
        CREATE TABLE IF NOT EXISTS TIPOS_USUARIO (
        SIGLA_USUARIO TEXT(3) NOT NULL primary key,
        DESCRICAO_USUARIO TEXT(50));
        """)
    except Error as e:
        print(f"ERRO {e} na Tabela TIPOS_USUARIO ")

    try: #Criando a tabea Usuario
        c.execute("""
        CREATE TABLE IF NOT EXISTS USUARIO (
        ID_USUARIO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOME TEXT(45) NOT NULL,
        IDADE INTEGER NOT NULL,
        CPF INTEGER NOT NULL,
        SIGLA_USUARIO TEXT(3) NOT NULL,
        FOREIGN KEY (SIGLA_USUARIO) REFERENCES TIPOS_USUARIO(SIGLA_USUARIO));
        """)
    except Error as e:
        print(f"ERRO {e} na Tabela USUARIO")
        
    try: #Criando a tabela Locais 
        c.execute("""
        CREATE TABLE IF NOT EXISTS LOCAIS (
        ID_LOCAIS INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        DESCRICAO_LOCAIS TEXT(50) NOT NULL,
        CEP_LOCAIS INTEGER(8) NOT NULL,
        CIDADE_LOCAIS TEXT(45) NOT NULL,
        ESTADO_LOCAIS TEXT(2) NOT NULL,
        ENDERECO_LOCAIS TEXT(75) NOT NULL,
        NUMERO_LOCAIS INTEGER(4) NOT NULL,
        COMPLEMENTO TEXT(3),
        PONTO_REFERENCIA TEXT);
        """)
    except Error as e:
        print(f"ERRO {e} na Tabela LOCAIS")

    try: #Criando a tabela Chamado
        c.execute("""
        CREATE TABLE IF NOT EXISTS CHAMADO (
        ID_CHAMADO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        DESCRICAO_CHAMADO TEXT(100) NOT NULL,
        DATA_SOLICITACAO DATE NOT NULL,
        DATA_CONCLUSAO DATE,
        ACOES_REALIZADAS TEXT(100),
        STATUS_CHAMADO TEXT(15),
        ID_LOCAIS INTEGER NOT NULL,
        ID_USUARIO INTEGER NOT NULL,
        NOME_TEL TEXT(25),
        FOREIGN KEY(ID_LOCAIS) REFERENCES LOCAIS(ID_LOCAIS),
        FOREIGN KEY(ID_USUARIO) REFERENCES USUARIO(ID_USUARIO));
        """)
    except Error as e:
        print(f"ERRO {e} na Tabela CHAMADO")

    try: #Criando a tabela Avaliação
        c.execute("""
        CREATE TABLE IF NOT EXISTS AVALIACAO (
        ID_AVALIACAO INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        NOTA_AVALIACAO INTEGER NOT NULL,
        DATA_AVALIACAO DATE NOT NULL,
        ID_CHAMADO INTEGER NOT NULL,
        FOREIGN KEY(ID_CHAMADO) REFERENCES CHAMADO(ID_CHAMADO));
        """)
    except Error as e:
        print(f"ERRO {e} na Tabela AVALIACAO")

       