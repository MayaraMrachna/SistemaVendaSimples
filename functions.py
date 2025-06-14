import sqlite3

# Função para cadastrar um produto
def cadastrar_produto(nome, preco):
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()
    print(f"Produto '{nome}' cadastrado!")

# Função para registrar uma venda
def registrar_venda(produto_id):
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vendas (produto_id) VALUES (?)", (produto_id,))
    conn.commit()
    conn.close()
    print("Venda registrada!")

# Função para consultar compras realizadas
def consultar_compras():
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("SELECT v.id, p.nome, p.preco FROM vendas v INNER JOIN produtos p ON v.produto_id = p.id")
    compras = cursor.fetchall()
    conn.close()

    if not compras:
        print("Nenhuma compra registrada.")
    else:
        print("Compras realizadas:")
        for compra in compras:
            print(f"- {compra[1]}: R$ {compra[2]:.2f}")

# Testando diretamente
if __name__ == "__main__":
    cadastrar_produto("Teclado", 120.00)
    consultar_compras() 