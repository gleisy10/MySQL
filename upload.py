import pandas as pd
import mysql.connector

# Configurações com banco de dados
db_config = {
    'host': 'localhost',  # Endereço do servidor MySQL
    'user': 'root',  # Nome do usuário do MySQL
    'password': 'Proz@2023',  # Senha do MySQL
    'database': 'db_alunos_proz'  # Nome do banco de dados
}

# Caminho do arquivo CSV
caminho_csv = r'c:\Users\LabInfo\Desktop\MySQL_PHP_gleisy\dados_ficticios - Copia.csv'

try:
    # Conectar ao banco de dados
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Criar a tabela (se não existir)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50),
            idade INT,
            disciplina VARCHAR(50),
            aprovado ENUM('Sim', 'Não')
        )
    """)
    connection.commit()  # Confirmar a criação da tabela

    # Ler o arquivo CSV
    arquivo_csv = pd.read_csv(caminho_csv)

    # Converter os dados do CSV para uma lista de tuplas
    dados_insercao = arquivo_csv.values.tolist()

    # Inserir os dados no banco de dados
    cursor.executemany("""
        INSERT INTO alunos (nome, idade, disciplina, aprovado)
        VALUES (%s, %s, %s, %s)
    """, dados_insercao)
    connection.commit()  # Confirmar a inserção dos dados

    print('Dados carregados no banco de dados!')

except mysql.connector.Error as erro:
    print(f"Erro: {erro}")

finally:
    if connection.is_connected():
        cursor.close()  # Fechar o cursor
        connection.close()  # Fechar a conexão
