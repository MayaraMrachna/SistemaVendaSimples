import tkinter as tk
from tkinter import messagebox
import sqlite3

# Criando a janela principal
root = tk.Tk()
root.title("Loja de Produtos InfoTech")
root.geometry("500x700")

# Criando framesx'
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

frame_middle = tk.Frame(root)
frame_middle.pack(pady=10)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=20)

# Adicionando elementos na parte superior
tk.Label(frame_top, text="Nome do Produto:").grid(row=0, column=0)
entry_nome = tk.Entry(frame_top)
entry_nome.grid(row=0, column=1)

tk.Label(frame_top, text="Preço:").grid(row=1, column=0)
entry_preco = tk.Entry(frame_top)
entry_preco.grid(row=1, column=1)

# Função para cadastrar produto
def cadastrar():
    nome = entry_nome.get()
    preco = entry_preco.get()
    if nome and preco:
        conn = sqlite3.connect("loja.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, float(preco)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado!")
        entry_nome.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        atualizar_lista()
    else:
        messagebox.showerror("Erro", "Preencha todos os campos!")

tk.Button(frame_top, text="Cadastrar", command=cadastrar).grid(row=2, columnspan=2, pady=10)

# Campo de busca
tk.Label(frame_middle, text="Buscar Produto:").grid(row=0, column=0)
entry_busca = tk.Entry(frame_middle)
entry_busca.grid(row=0, column=1)

def buscar_produto():
    termo = entry_busca.get().lower()
    lista_produtos.delete(0, tk.END)
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco FROM produtos WHERE LOWER(nome) LIKE ?", ('%' + termo + '%',))
    produtos = cursor.fetchall()
    conn.close()
    for produto in produtos:
        lista_produtos.insert(tk.END, f"{produto[0]} - {produto[1]} - R$ {produto[2]:.2f}")

tk.Button(frame_middle, text="Buscar", command=buscar_produto).grid(row=0, column=2)

# Lista de produtos
lista_produtos = tk.Listbox(frame_bottom, width=50, height=10)
lista_produtos.pack()

# Função para atualizar a lista de produtos
def atualizar_lista():
    lista_produtos.delete(0, tk.END)
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    for produto in produtos:
        lista_produtos.insert(tk.END, f"{produto[0]} - {produto[1]} - R$ {produto[2]:.2f}")

# Função para registrar venda
def registrar_venda():
    selecionado = lista_produtos.curselection()
    if selecionado:
        produto_info = lista_produtos.get(selecionado[0]).split(" - ")
        produto_id = produto_info[0]  # Pegando o ID do produto

        conn = sqlite3.connect("loja.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vendas (produto_id) VALUES (?)", (produto_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
    else:
        messagebox.showerror("Erro", "Selecione um produto para vender!")

tk.Button(frame_bottom, text="Registrar Venda", command=registrar_venda).pack(pady=10)

# Função para exibir relatório de vendas
def exibir_relatorio():
    relatorio = tk.Toplevel(root)
    relatorio.title("Relatório de Vendas")
    relatorio.geometry("400x300")

    lista_vendas = tk.Listbox(relatorio, width=50, height=10)
    lista_vendas.pack(pady=10)

    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("SELECT v.id, p.nome, p.preco FROM vendas v INNER JOIN produtos p ON v.produto_id = p.id")
    vendas = cursor.fetchall()
    conn.close()

    if not vendas:
        lista_vendas.insert(tk.END, "Nenhuma venda registrada.")
    else:
        for venda in vendas:
            lista_vendas.insert(tk.END, f"Venda {venda[0]} - {venda[1]} - R$ {venda[2]:.2f}")

tk.Button(frame_bottom, text="Relatório de Vendas", command=exibir_relatorio).pack(pady=10)

def excluir_produto():
    selecionado = lista_produtos.curselection()
    if selecionado:
        produto_info = lista_produtos.get(selecionado[0]).split(" - ")
        produto_id = produto_info[0]

        conn = sqlite3.connect("loja.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Produto excluído!")
        atualizar_lista()
    else:
        messagebox.showerror("Erro", "Selecione um produto para excluir!")

tk.Button(frame_bottom, text="Excluir Produto", command=excluir_produto).pack(pady=5)

def excluir_venda():
    selecionado = lista_vendas.curselection()
    if selecionado:
        venda_info = lista_vendas.get(selecionado[0]).split(" - ")
        venda_id = venda_info[0]

        conn = sqlite3.connect("loja.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas WHERE id=?", (venda_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Venda excluída!")
        exibir_relatorio()
    else:
        messagebox.showerror("Erro", "Selecione uma venda para excluir!")

tk.Button(frame_bottom, text="Excluir Venda", command=excluir_venda).pack(pady=5)

def editar_preco():
    selecionado = lista_produtos.curselection()
    if selecionado:
        produto_info = lista_produtos.get(selecionado[0]).split(" - ")
        produto_id = produto_info[0]
        
        novo_preco = tk.simpledialog.askfloat("Editar Preço", "Digite o novo preço:")
        if novo_preco is not None:
            conn = sqlite3.connect("loja.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE produtos SET preco=? WHERE id=?", (novo_preco, produto_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Preço atualizado!")
            atualizar_lista()
    else:
        messagebox.showerror("Erro", "Selecione um produto para editar!")

tk.Button(frame_bottom, text="Editar Preço", command=editar_preco).pack(pady=5)

atualizar_lista()

root.mainloop()
