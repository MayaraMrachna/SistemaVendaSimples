import sqlite3

# Criando conexão com o banco
conn = sqlite3.connect("loja.db")
cursor = conn.cursor()

# Criando tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
""")
print("Banco de dados criado e as tabelas foram geradas corretamente!")
conn.commit()
conn.close()


