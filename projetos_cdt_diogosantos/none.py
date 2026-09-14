
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
from faker import Faker
from datetime import datetime

# ==========================================
# CONFIGURACOES
# ==========================================

NOME_LOJA = "BRASIL CAMISAS"
ARQUIVO_JSON = "configuracao.json"
BANCO_DADOS = "loja_camisas.db"

fake = Faker("pt_BR")

# ==========================================
# TIMES DO BRASILEIRAO 2026
# ==========================================

times = [
    "Athletico-PR",
    "Atletico-MG",
    "Bahia",
    "Botafogo",
    "Chapecoense",
    "Corinthians",
    "Coritiba",
    "Cruzeiro",
    "Flamengo",
    "Fluminense",
    "Gremio",
    "Internacional",
    "Mirassol",
    "Palmeiras",
    "Red Bull Bragantino",
    "Remo",
    "Santos",
    "Sao Paulo",
    "Vasco",
    "Vitoria"
]

# ==========================================
# PRECOS DAS CAMISAS
# ==========================================

precos = {
    time: 120.00 + (i * 5)
    for i, time in enumerate(times)
}

# ==========================================
# BANCO DE DADOS SQLITE
# ==========================================

conexao = sqlite3.connect(BANCO_DADOS)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    total REAL NOT NULL,
    data TEXT NOT NULL
)
""")

conexao.commit()

# ==========================================
# INSERIR PRODUTOS
# ==========================================

cursor.execute("SELECT COUNT(*) FROM produtos")
quantidade_produtos = cursor.fetchone()[0]

if quantidade_produtos == 0:
    for time in times:
        cursor.execute(
            "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
            ("Camisa " + time, precos[time])
        )

    conexao.commit()

# ==========================================
# JSON
# ==========================================

configuracao = {
    "nome_loja": NOME_LOJA,
    "categoria": "Camisas de Times Brasileiros",
    "quantidade_times": len(times),
    "times": times
}

with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
    json.dump(
        configuracao,
        arquivo,
        ensure_ascii=False,
        indent=4
    )

# ==========================================
# JANELA PRINCIPAL
# ==========================================

janela = tk.Tk()
janela.title(NOME_LOJA)
janela.geometry("1000x700")
janela.minsize(850, 600)

# ==========================================
# FUNDO METADE BRANCO E METADE VERMELHO
# ==========================================

fundo = tk.Canvas(
    janela,
    highlightthickness=0,
    bd=0
)

fundo.pack(fill="both", expand=True)

def desenhar_fundo(event=None):
    fundo.delete("fundo")

    largura = janela.winfo_width()
    altura = janela.winfo_height()

    metade = largura // 2

    fundo.create_rectangle(
        0,
        0,
        metade,
        altura,
        fill="white",
        outline="",
        tags="fundo"
    )

    fundo.create_rectangle(
        metade,
        0,
        largura,
        altura,
        fill="#c62828",
        outline="",
        tags="fundo"
    )

fundo.bind("<Configure>", desenhar_fundo)

# ==========================================
# FRAME PRINCIPAL
# ==========================================

conteudo = tk.Frame(
    fundo,
    bg="white",
    padx=15,
    pady=10
)

janela.update_idletasks()

fundo.create_window(
    0,
    0,
    anchor="nw",
    window=conteudo,
    width=janela.winfo_width() // 2,
    height=janela.winfo_height(),
    tags="conteudo"
)

def ajustar_conteudo(event=None):
    largura = janela.winfo_width()
    altura = janela.winfo_height()

    fundo.itemconfig(
        "conteudo",
        width=largura // 2,
        height=altura
    )

fundo.bind("<Configure>", ajustar_conteudo, add="+")

# ==========================================
# CARRINHO
# ==========================================

carrinho = []

# ==========================================
# FUNCOES
# ==========================================

def atualizar_total():
    total = sum(
        item["subtotal"]
        for item in carrinho
    )

    label_total.config(
        text=f"Total: R$ {total:.2f}"
    )


def atualizar_carrinho():
    lista_carrinho.delete(
        *lista_carrinho.get_children()
    )

    for item in carrinho:
        lista_carrinho.insert(
            "",
            "end",
            values=(
                item["produto"],
                item["quantidade"],
                f"R$ {item['subtotal']:.2f}"
            )
        )

    atualizar_total()


def adicionar_carrinho():
    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Aviso",
            "Selecione uma camisa."
        )
        return

    item = tabela.item(selecionado[0])
    valores = item["values"]

    produto = valores[1]
    preco = float(valores[2])

    try:
        quantidade = int(
            campo_quantidade.get()
        )

        if quantidade <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Digite uma quantidade valida."
        )
        return

    subtotal = preco * quantidade

    carrinho.append({
        "produto": produto,
        "quantidade": quantidade,
        "subtotal": subtotal
    })

    atualizar_carrinho()

    messagebox.showinfo(
        "Sucesso",
        "Camisa adicionada ao carrinho!"
    )


def remover_carrinho():
    selecionado = lista_carrinho.selection()

    if not selecionado:
        messagebox.showwarning(
            "Aviso",
            "Selecione um item do carrinho."
        )
        return

    indice = lista_carrinho.index(
        selecionado[0]
    )

    carrinho.pop(indice)

    atualizar_carrinho()


def finalizar_pedido():
    if not carrinho:
        messagebox.showwarning(
            "Aviso",
            "O carrinho esta vazio."
        )
        return

    nome_cliente = campo_cliente.get().strip()

    if nome_cliente == "":
        messagebox.showwarning(
            "Aviso",
            "Digite o nome do cliente."
        )
        return

    total = sum(
        item["subtotal"]
        for item in carrinho
    )

    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    cursor.execute(
        """
        INSERT INTO pedidos
        (cliente, total, data)
        VALUES (?, ?, ?)
        """,
        (nome_cliente, total, data)
    )

    conexao.commit()

    messagebox.showinfo(
        "Pedido finalizado",
        f"Cliente: {nome_cliente}\n"
        f"Total: R$ {total:.2f}\n"
        f"Data: {data}\n\n"
        "Obrigado pela compra!"
    )

    carrinho.clear()

    atualizar_carrinho()


def gerar_cliente():
    nome = fake.name()
    email = fake.email()

    campo_cliente.delete(
        0,
        tk.END
    )

    campo_cliente.insert(
        0,
        nome
    )

    cursor.execute(
        """
        INSERT INTO clientes
        (nome, email)
        VALUES (?, ?)
        """,
        (nome, email)
    )

    conexao.commit()

    messagebox.showinfo(
        "Cliente gerado",
        f"Nome: {nome}\n"
        f"Email: {email}"
    )


def mostrar_pedidos():
    janela_pedidos = tk.Toplevel(janela)

    janela_pedidos.title(
        "Historico de Pedidos"
    )

    janela_pedidos.geometry(
        "650x400"
    )

    tabela_pedidos = ttk.Treeview(
        janela_pedidos,
        columns=(
            "id",
            "cliente",
            "total",
            "data"
        ),
        show="headings"
    )

    tabela_pedidos.heading(
        "id",
        text="ID"
    )

    tabela_pedidos.heading(
        "cliente",
        text="Cliente"
    )

    tabela_pedidos.heading(
        "total",
        text="Total"
    )

    tabela_pedidos.heading(
        "data",
        text="Data"
    )

    tabela_pedidos.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    cursor.execute(
        """
        SELECT id, cliente, total, data
        FROM pedidos
        ORDER BY id DESC
        """
    )

    pedidos = cursor.fetchall()

    for pedido in pedidos:
        tabela_pedidos.insert(
            "",
            "end",
            values=(
                pedido[0],
                pedido[1],
                f"R$ {pedido[2]:.2f}",
                pedido[3]
            )
        )


def fechar_programa():
    conexao.close()
    janela.destroy()


# ==========================================
# TITULO
# ==========================================

titulo = tk.Label(
    conteudo,
    text="BRASIL CAMISAS",
    font=("Arial", 24, "bold"),
    bg="white",
    fg="#b71c1c"
)

titulo.pack(pady=10)

subtitulo = tk.Label(
    conteudo,
    text="Loja de Camisas de Times Brasileiros",
    font=("Arial", 12),
    bg="white",
    fg="#333333"
)

subtitulo.pack(pady=5)

# ==========================================
# AREA DE PRODUTOS
# ==========================================

frame_produtos = tk.LabelFrame(
    conteudo,
    text="Camisas disponiveis",
    font=("Arial", 11, "bold"),
    bg="white",
    padx=8,
    pady=8
)

frame_produtos.pack(
    fill="both",
    expand=True,
    pady=8
)

tabela = ttk.Treeview(
    frame_produtos,
    columns=(
        "numero",
        "produto",
        "preco"
    ),
    show="headings",
    height=8
)

tabela.heading(
    "numero",
    text="Numero"
)

tabela.heading(
    "produto",
    text="Camisa"
)

tabela.heading(
    "preco",
    text="Preco"
)

tabela.column(
    "numero",
    width=70,
    anchor="center"
)

tabela.column(
    "produto",
    width=300
)

tabela.column(
    "preco",
    width=120,
    anchor="center"
)

tabela.pack(
    side="left",
    fill="both",
    expand=True
)

barra = ttk.Scrollbar(
    frame_produtos,
    orient="vertical",
    command=tabela.yview
)

barra.pack(
    side="right",
    fill="y"
)

tabela.configure(
    yscrollcommand=barra.set
)

cursor.execute(
    "SELECT id, nome, preco FROM produtos"
)

produtos = cursor.fetchall()

for produto in produtos:
    tabela.insert(
        "",
        "end",
        values=(
            produto[0],
            produto[1],
            f"{produto[2]:.2f}"
        )
    )

# ==========================================
# AREA DE COMPRA
# ==========================================

frame_compra = tk.Frame(
    conteudo,
    bg="white"
)

frame_compra.pack(
    pady=5
)

tk.Label(
    frame_compra,
    text="Quantidade:",
    bg="white",
    font=("Arial", 11)
).grid(
    row=0,
    column=0,
    padx=5
)

campo_quantidade = tk.Entry(
    frame_compra,
    width=8
)

campo_quantidade.insert(
    0,
    "1"
)

campo_quantidade.grid(
    row=0,
    column=1,
    padx=5
)

botao_adicionar = tk.Button(
    frame_compra,
    text="Adicionar ao Carrinho",
    command=adicionar_carrinho,
    bg="#b71c1c",
    fg="white",
    font=("Arial", 10, "bold")
)

botao_adicionar.grid(
    row=0,
    column=2,
    padx=10
)

# ==========================================
# CARRINHO
# ==========================================

frame_carrinho = tk.LabelFrame(
    conteudo,
    text="Carrinho de Compras",
    font=("Arial", 11, "bold"),
    bg="white",
    padx=8,
    pady=8
)

frame_carrinho.pack(
    fill="x",
    pady=5
)

lista_carrinho = ttk.Treeview(
    frame_carrinho,
    columns=(
        "produto",
        "quantidade",
        "subtotal"
    ),
    show="headings",
    height=3
)

lista_carrinho.heading(
    "produto",
    text="Produto"
)

lista_carrinho.heading(
    "quantidade",
    text="Quantidade"
)

lista_carrinho.heading(
    "subtotal",
    text="Subtotal"
)

lista_carrinho.pack(
    fill="x",
    expand=True
)

botao_remover = tk.Button(
    frame_carrinho,
    text="Remover Item",
    command=remover_carrinho,
    bg="#c62828",
    fg="white"
)

botao_remover.pack(
    pady=5
)

label_total = tk.Label(
    frame_carrinho,
    text="Total: R$ 0.00",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#b71c1c"
)

label_total.pack(
    pady=5
)

# ==========================================
# CLIENTE E FINALIZACAO
# ==========================================

frame_final = tk.Frame(
    conteudo,
    bg="white"
)

frame_final.pack(
    pady=8
)

tk.Label(
    frame_final,
    text="Nome do Cliente:",
    bg="white",
    font=("Arial", 11)
).grid(
    row=0,
    column=0,
    padx=5
)

campo_cliente = tk.Entry(
    frame_final,
    width=25
)

campo_cliente.grid(
    row=0,
    column=1,
    padx=5
)

botao_cliente = tk.Button(
    frame_final,
    text="Gerar Cliente Faker",
    command=gerar_cliente,
    bg="#7d3c98",
    fg="white"
)

botao_cliente.grid(
    row=0,
    column=2,
    padx=5
)

botao_finalizar = tk.Button(
    frame_final,
    text="Finalizar Pedido",
    command=finalizar_pedido,
    bg="#229954",
    fg="white",
    font=("Arial", 11, "bold")
)

botao_finalizar.grid(
    row=1,
    column=1,
    pady=10
)

botao_historico = tk.Button(
    frame_final,
    text="Historico de Pedidos",
    command=mostrar_pedidos,
    bg="#34495e",
    fg="white"
)

botao_historico.grid(
    row=1,
    column=2,
    pady=10
)

# ==========================================
# ENCERRAMENTO
# ==========================================

janela.protocol(
    "WM_DELETE_WINDOW",
    fechar_programa
)

janela.mainloop()