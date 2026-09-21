import os
import ssl
import json
import random
import sqlite3
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from faker import Faker
    fake = Faker("pt_BR")
except ImportError:
    fake = None


# =====================================================
# CONFIGURAÇÕES DA LOJA E DADOS DOS TIMES
# =====================================================

NOME_LOJA = "Nação dos Mantos - Automação"
BANCO = "loja_camisas.db"
PASTA_ESCUDOS = "escudos"
PRECO_PERSONALIZACAO = 20.00
TAXA_ENTREGA = 10.00

# Dicionário completo com os 20 times e URLs CDN estáveis (PNGs transparentes em HD)
times_dados = {
    "Athletico-PR": {
        "preco": 149.90, "sigla": "CAP", "cor": "#c62828", "arquivo": "athletico-pr.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/athletico-pr.png"
    },
    "Atletico-MG": {
        "preco": 159.90, "sigla": "CAM", "cor": "#212121", "arquivo": "atletico-mg.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/atletico-mg.png"
    },
    "Bahia": {
        "preco": 139.90, "sigla": "BAH", "cor": "#1565c0", "arquivo": "bahia.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/bahia.png"
    },
    "Botafogo": {
        "preco": 149.90, "sigla": "BOT", "cor": "#111111", "arquivo": "botafogo.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/botafogo.png"
    },
    "Chapecoense": {
        "preco": 119.90, "sigla": "CHA", "cor": "#2e7d32", "arquivo": "chapecoense.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/chapecoense.png"
    },
    "Corinthians": {
        "preco": 169.90, "sigla": "COR", "cor": "#212121", "arquivo": "corinthians.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/corinthians.png"
    },
    "Coritiba": {
        "preco": 129.90, "sigla": "CFC", "cor": "#388e3c", "arquivo": "coritiba.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/coritiba.png"
    },
    "Cruzeiro": {
        "preco": 159.90, "sigla": "CRU", "cor": "#1565c0", "arquivo": "cruzeiro.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/cruzeiro.png"
    },
    "Flamengo": {
        "preco": 179.90, "sigla": "FLA", "cor": "#b71c1c", "arquivo": "flamengo.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/flamengo.png"
    },
    "Fluminense": {
        "preco": 159.90, "sigla": "FLU", "cor": "#00695c", "arquivo": "fluminense.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/fluminense.png"
    },
    "Gremio": {
        "preco": 159.90, "sigla": "GRE", "cor": "#0277bd", "arquivo": "gremio.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/gremio.png"
    },
    "Internacional": {
        "preco": 159.90, "sigla": "INT", "cor": "#d32f2f", "arquivo": "internacional.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/internacional.png"
    },
    "Mirassol": {
        "preco": 119.90, "sigla": "MIR", "cor": "#f9a825", "arquivo": "mirassol.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/mirassol.png"
    },
    "Palmeiras": {
        "preco": 179.90, "sigla": "PAL", "cor": "#1b5e20", "arquivo": "palmeiras.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/palmeiras.png"
    },
    "Red Bull Bragantino": {
        "preco": 139.90, "sigla": "RBB", "cor": "#d32f2f", "arquivo": "bragantino.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/red-bull-bragantino.png"
    },
    "Remo": {
        "preco": 119.90, "sigla": "REM", "cor": "#283593", "arquivo": "remo.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/remo.png"
    },
    "Santos": {
        "preco": 149.90, "sigla": "SAN", "cor": "#212121", "arquivo": "santos.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/santos.png"
    },
    "Sao Paulo": {
        "preco": 169.90, "sigla": "SPFC", "cor": "#c62828", "arquivo": "sao-paulo.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/sao-paulo.png"
    },
    "Vasco": {
        "preco": 159.90, "sigla": "VAS", "cor": "#212121", "arquivo": "vasco.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/vasco.png"
    },
    "Vitoria": {
        "preco": 129.90, "sigla": "VIT", "cor": "#c62828", "arquivo": "vitoria.png",
        "url": "https://cdn.jsdelivr.net/gh/vitorfs/hex-bot@master/public/logos/vitoria.png"
    }
}

times = list(times_dados.keys())

if not os.path.exists(PASTA_ESCUDOS):
    os.makedirs(PASTA_ESCUDOS)


# =====================================================
# FUNÇÃO DE DOWNLOAD ROBUSTA
# =====================================================

def baixar_escudos_automaticamente():
    contexto_ssl = ssl._create_unverified_context()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    for time, info in times_dados.items():
        caminho_local = os.path.join(PASTA_ESCUDOS, info["arquivo"])
        
        # Faz o download caso o arquivo não exista ou esteja corrompido/zerado (< 200 bytes)
        if not os.path.exists(caminho_local) or os.path.getsize(caminho_local) < 200:
            try:
                req = urllib.request.Request(info["url"], headers=headers)
                with urllib.request.urlopen(req, context=contexto_ssl, timeout=8) as response:
                    conteudo = response.read()
                    if len(conteudo) > 200:
                        with open(caminho_local, 'wb') as out_file:
                            out_file.write(conteudo)
                        print(f"[OK] Escudo de {time} baixado com sucesso.")
            except Exception as e:
                print(f"[ERRO] Não foi possível baixar {time}: {e}")

baixar_escudos_automaticamente()


# =====================================================
# BANCO DE DADOS (SQLITE)
# =====================================================

conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    detalhes TEXT NOT NULL,
    subtotal REAL NOT NULL,
    taxa_entrega REAL NOT NULL,
    total REAL NOT NULL,
    data TEXT NOT NULL,
    rastreio TEXT NOT NULL,
    pagamento TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

cursor.execute("SELECT COUNT(*) FROM produtos")
if cursor.fetchone()[0] == 0:
    for time in times:
        cursor.execute(
            "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
            ("Camisa " + time, times_dados[time]["preco"])
        )

conexao.commit()


# =====================================================
# INTERFACE GRÁFICA (TKINTER)
# =====================================================

janela = tk.Tk()
janela.title(NOME_LOJA)

LARGURA_JANELA = 1100
ALTURA_JANELA = 680

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela // 2) - (LARGURA_JANELA // 2)
pos_y = (altura_tela // 2) - (ALTURA_JANELA // 2)

janela.geometry(f"{LARGURA_JANELA}x{ALTURA_JANELA}+{pos_x}+{pos_y}")
janela.resizable(True, True)
janela.configure(bg="#f4f6f9")

carrinho = []
time_selecionado = None
botoes_times_dados = []
imagens_carregadas = {}


def obter_escudo_widget(parent, time):
    info = times_dados.get(time, {})
    caminho_imagem = os.path.join(PASTA_ESCUDOS, info.get("arquivo", ""))

    if HAS_PIL and os.path.exists(caminho_imagem) and os.path.getsize(caminho_imagem) > 200:
        try:
            img = Image.open(caminho_imagem).convert("RGBA")
            img = img.resize((36, 36), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            imagens_carregadas[time] = photo
            
            return tk.Label(parent, image=photo, bg="white")
        except Exception as e:
            print(f"Erro ao carregar imagem do {time}: {e}")

    # Fallback Vetorial Personalizado no Canvas (caso a imagem falhe)
    canvas = tk.Canvas(parent, width=36, height=36, bg="white", highlightthickness=0)
    cor = info.get("cor", "#333333")
    sigla = info.get("sigla", "TIME")

    canvas.create_polygon(3, 3, 33, 3, 33, 23, 18, 33, 3, 23, fill=cor, outline="#000", width=1)
    canvas.create_polygon(6, 6, 30, 6, 30, 21, 18, 29, 6, 21, fill="white", outline="#000", width=1)
    canvas.create_text(18, 15, text=sigla, font=("Arial", 6, "bold"), fill=cor)

    return canvas


def selecionar_time(time):
    global time_selecionado
    time_selecionado = time
    label_selecionado.config(text=f"Time selecionado: {time}")

    for botao, nome_time in botoes_times_dados:
        if nome_time == time:
            botao.config(bg="#2e7d32", fg="white", text="OK ✓")
        else:
            botao.config(bg="#b71c1c", fg="white", text="Selecionar")


def calcular_totais():
    subtotal = sum(item["subtotal"] for item in carrinho)
    entrega = TAXA_ENTREGA if carrinho else 0.00
    total = subtotal + entrega
    return subtotal, entrega, total


def atualizar_total():
    subtotal, entrega, total = calcular_totais()
    label_subtotal.config(text=f"Subtotal: R$ {subtotal:.2f}".replace(".", ","))
    label_entrega.config(text=f"Taxa de Entrega: R$ {entrega:.2f}".replace(".", ","))
    label_total.config(text=f"TOTAL: R$ {total:.2f}".replace(".", ","))


def atualizar_carrinho():
    lista_carrinho.delete(*lista_carrinho.get_children())

    for item in carrinho:
        personalizado = "Sim" if item["personalizado"] else "Não"
        lista_carrinho.insert(
            "",
            "end",
            values=(
                item["produto"],
                item["tamanho"],
                personalizado,
                item["quantidade"],
                f"R$ {item['subtotal']:.2f}".replace(".", ",")
            )
        )

    atualizar_total()


def ativar_personalizacao():
    if var_personalizar.get():
        campo_nome.config(state="normal")
        campo_numero.config(state="normal")
    else:
        campo_nome.delete(0, tk.END)
        campo_numero.delete(0, tk.END)
        campo_nome.config(state="disabled")
        campo_numero.config(state="disabled")


def adicionar_carrinho():
    if time_selecionado is None:
        messagebox.showwarning("Aviso", "Selecione um time primeiro.")
        return

    tamanho = combo_tamanho.get()
    if not tamanho:
        messagebox.showwarning("Aviso", "Selecione o tamanho da camisa.")
        return

    try:
        quantidade = int(campo_quantidade.get())
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Digite uma quantidade válida.")
        return

    personalizado = var_personalizar.get()
    nome = campo_nome.get().strip()
    numero = campo_numero.get().strip()

    if personalizado and (not nome or not numero):
        messagebox.showwarning("Aviso", "Preencha o nome e o número para personalização.")
        return

    preco_unitario = times_dados[time_selecionado]["preco"]
    if personalizado:
        preco_unitario += PRECO_PERSONALIZACAO

    subtotal = preco_unitario * quantidade

    item = {
        "produto": "Camisa " + time_selecionado,
        "tamanho": tamanho,
        "personalizado": personalizado,
        "nome": nome,
        "numero": numero,
        "quantidade": quantidade,
        "subtotal": subtotal
    }

    carrinho.append(item)
    atualizar_carrinho()


def remover_item():
    selecionado = lista_carrinho.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um item para remover.")
        return

    indice = lista_carrinho.index(selecionado[0])
    carrinho.pop(indice)
    atualizar_carrinho()


def gerar_cliente():
    nome = fake.name() if fake else "Cliente Automático"
    campo_cliente.delete(0, tk.END)
    campo_cliente.insert(0, nome)


def finalizar_pedido():
    if not carrinho:
        messagebox.showwarning("Aviso", "O carrinho está vazio.")
        return

    cliente = campo_cliente.get().strip()
    pagamento = combo_pagamento.get()

    if not cliente:
        messagebox.showwarning("Aviso", "Digite o nome do cliente.")
        return

    if not pagamento:
        messagebox.showwarning("Aviso", "Selecione a forma de pagamento.")
        return

    subtotal, entrega, total = calcular_totais()

    detalhes = []
    for item in carrinho:
        desc = f"{item['quantidade']}x {item['produto']} ({item['tamanho']})"
        if item["personalizado"]:
            desc += f" [Pers: {item['nome']} N°{item['numero']}]"
        detalhes.append(desc)

    detalhes_texto = " | ".join(detalhes)
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    rastreio = "NM" + str(random.randint(100000, 999999)) + "BR"
    status = "Aguardando Envio"

    cursor.execute("""
        INSERT INTO pedidos (cliente, detalhes, subtotal, taxa_entrega, total, data, rastreio, pagamento, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (cliente, detalhes_texto, subtotal, entrega, total, data, rastreio, pagamento, status))

    conexao.commit()

    carrinho.clear()
    atualizar_carrinho()
    campo_cliente.delete(0, tk.END)
    combo_pagamento.set("")

    messagebox.showinfo(
        "Pedido Finalizado",
        f"✅ Pedido cadastrado com sucesso!\n\n"
        f"👤 Cliente: {cliente}\n"
        f"💳 Pagamento: {pagamento}\n"
        f"📦 Rastreio: {rastreio}\n"
        f"💵 Subtotal: R$ {subtotal:.2f}\n"
        f"🚚 Taxa de Entrega: R$ {entrega:.2f}\n"
        f"💰 TOTAL FINAL: R$ {total:.2f}\n"
        f"📌 Status: {status}"
    )


def mostrar_historico():
    tela = tk.Toplevel(janela)
    tela.title("Histórico de Pedidos")
    tela.geometry("900x400")
    tela.configure(bg="white")

    tabela = ttk.Treeview(
        tela,
        columns=("id", "cliente", "detalhes", "subtotal", "entrega", "total", "data", "rastreio", "pagamento", "status"),
        show="headings"
    )

    colunas = {
        "id": "ID", "cliente": "Cliente", "detalhes": "Itens", "subtotal": "Subtotal",
        "entrega": "Frete", "total": "Total", "data": "Data", "rastreio": "Rastreio",
        "pagamento": "Pagamento", "status": "Status"
    }

    for col, tit in colunas.items():
        tabela.heading(col, text=tit)

    tabela.column("id", width=30)
    tabela.column("cliente", width=110)
    tabela.column("detalhes", width=220)
    tabela.column("subtotal", width=65)
    tabela.column("entrega", width=55)
    tabela.column("total", width=65)
    tabela.column("data", width=100)
    tabela.column("rastreio", width=90)
    tabela.column("pagamento", width=90)
    tabela.column("status", width=85)

    tabela.pack(fill="both", expand=True, padx=8, pady=8)

    cursor.execute("""
        SELECT id, cliente, detalhes, subtotal, taxa_entrega, total, data, rastreio, pagamento, status
        FROM pedidos ORDER BY id DESC
    """)

    for p in cursor.fetchall():
        tabela.insert("", "end", values=(
            p[0], p[1], p[2],
            f"R$ {p[3]:.2f}", f"R$ {p[4]:.2f}", f"R$ {p[5]:.2f}",
            p[6], p[7], p[8], p[9]
        ))


def fechar_programa():
    conexao.close()
    janela.destroy()


# =====================================================
# LAYOUT DA APLICAÇÃO
# =====================================================

lado_esquerdo = tk.Frame(janela, bg="white", padx=10, pady=10)
lado_esquerdo.pack(side="left", fill="both", expand=True)

lado_direito = tk.Frame(janela, bg="#c62828", padx=10, pady=10)
lado_direito.pack(side="right", fill="both", expand=True)

tk.Label(lado_esquerdo, text=NOME_LOJA, font=("Arial", 16, "bold"), bg="white", fg="#b71c1c").pack(anchor="w")
tk.Label(lado_esquerdo, text="Entrega Fixa: R$ 10,00", font=("Arial", 9), bg="white", fg="#555").pack(anchor="w", pady=(0, 5))

frame_times = tk.LabelFrame(lado_esquerdo, text="Escolha o Time (Escudos PNG HD)", bg="white", padx=5, pady=5)
frame_times.pack(fill="both", expand=True)

canvas_times = tk.Canvas(frame_times, bg="white", highlightthickness=0)
barra_times = ttk.Scrollbar(frame_times, orient="vertical", command=canvas_times.yview)
lista_times = tk.Frame(canvas_times, bg="white")

lista_times.bind("<Configure>", lambda e: canvas_times.configure(scrollregion=canvas_times.bbox("all")))
canvas_times.create_window((0, 0), window=lista_times, anchor="nw")
canvas_times.configure(yscrollcommand=barra_times.set)

canvas_times.pack(side="left", fill="both", expand=True)
barra_times.pack(side="right", fill="y")

for numero, time in enumerate(times, start=1):
    linha = tk.Frame(lista_times, bg="white", relief="solid", borderwidth=1)
    linha.pack(fill="x", padx=3, pady=2)

    escudo_widget = obter_escudo_widget(linha, time)
    escudo_widget.pack(side="left", padx=4, pady=2)

    info_text = f"{time} — R$ {times_dados[time]['preco']:.2f}".replace(".", ",")
    tk.Label(linha, text=info_text, font=("Arial", 9, "bold"), bg="white", anchor="w").pack(side="left", fill="x", expand=True, padx=4)

    btn = tk.Button(linha, text="Selecionar", font=("Arial", 8), bg="#b71c1c", fg="white", command=lambda t=time: selecionar_time(t))
    btn.pack(side="right", padx=5, pady=2)

    botoes_times_dados.append((btn, time))

label_selecionado = tk.Label(lado_esquerdo, text="Time selecionado: nenhum", font=("Arial", 10, "bold"), bg="white", fg="#2e7d32")
label_selecionado.pack(anchor="w", pady=4)

frame_opcoes = tk.LabelFrame(lado_esquerdo, text="Opções da Camisa", bg="white", padx=6, pady=6)
frame_opcoes.pack(fill="x", pady=4)

linha_tam_qtd = tk.Frame(frame_opcoes, bg="white")
linha_tam_qtd.pack(fill="x")

tk.Label(linha_tam_qtd, text="Tamanho:", bg="white", font=("Arial", 9)).pack(side="left")
combo_tamanho = ttk.Combobox(linha_tam_qtd, values=["PP", "P", "M", "G", "GG", "XG"], state="readonly", width=4)
combo_tamanho.set("M")
combo_tamanho.pack(side="left", padx=4)

tk.Label(linha_tam_qtd, text="Qtd:", bg="white", font=("Arial", 9)).pack(side="left", padx=(8, 0))
campo_quantidade = tk.Entry(linha_tam_qtd, width=4)
campo_quantidade.insert(0, "1")
campo_quantidade.pack(side="left", padx=4)

var_personalizar = tk.BooleanVar(value=False)
tk.Checkbutton(frame_opcoes, text="Personalizar (+R$ 20,00)", variable=var_personalizar, command=ativar_personalizacao, bg="white", font=("Arial", 9)).pack(anchor="w", pady=2)

linha_pers = tk.Frame(frame_opcoes, bg="white")
linha_pers.pack(fill="x")

tk.Label(linha_pers, text="Nome:", bg="white", font=("Arial", 9)).pack(side="left")
campo_nome = tk.Entry(linha_pers, width=12, state="disabled")
campo_nome.pack(side="left", padx=3)

tk.Label(linha_pers, text="N°:", bg="white", font=("Arial", 9)).pack(side="left", padx=(4, 0))
campo_numero = tk.Entry(linha_pers, width=4, state="disabled")
campo_numero.pack(side="left", padx=3)

tk.Button(lado_esquerdo, text="Adicionar ao Carrinho", command=adicionar_carrinho, bg="#b71c1c", fg="white", font=("Arial", 10, "bold")).pack(fill="x", pady=6)

# Lado Direito (Carrinho e Checkout)
tk.Label(lado_direito, text="CARRINHO DE COMPRAS", font=("Arial", 14, "bold"), bg="#c62828", fg="white").pack(anchor="w")

frame_carrinho = tk.LabelFrame(lado_direito, text="Itens Selecionados", bg="#c62828", fg="white", padx=5, pady=5)
frame_carrinho.pack(fill="both", expand=True, pady=4)

lista_carrinho = ttk.Treeview(
    frame_carrinho,
    columns=("produto", "tamanho", "personalizado", "quantidade", "subtotal"),
    show="headings",
    height=8
)

cols = {"produto": "Produto", "tamanho": "Tam.", "personalizado": "Pers.", "quantidade": "Qtd.", "subtotal": "Subtotal"}
for c, t in cols.items():
    lista_carrinho.heading(c, text=t)

lista_carrinho.column("produto", width=120)
lista_carrinho.column("tamanho", width=40)
lista_carrinho.column("personalizado", width=40)
lista_carrinho.column("quantidade", width=40)
lista_carrinho.column("subtotal", width=65)

lista_carrinho.pack(fill="both", expand=True)

tk.Button(frame_carrinho, text="Remover Item Selecionado", command=remover_item, bg="#8e0000", fg="white", font=("Arial", 8)).pack(pady=3)

label_subtotal = tk.Label(lado_direito, text="Subtotal: R$ 0,00", font=("Arial", 10), bg="#c62828", fg="white")
label_subtotal.pack(anchor="e")

label_entrega = tk.Label(lado_direito, text="Taxa de Entrega: R$ 0,00", font=("Arial", 10), bg="#c62828", fg="white")
label_entrega.pack(anchor="e")

label_total = tk.Label(lado_direito, text="TOTAL: R$ 0,00", font=("Arial", 13, "bold"), bg="#c62828", fg="white")
label_total.pack(anchor="e", pady=(2, 4))

frame_cliente = tk.LabelFrame(lado_direito, text="Dados do Cliente", bg="#c62828", fg="white", padx=6, pady=6)
frame_cliente.pack(fill="x")

tk.Label(frame_cliente, text="Nome do Cliente:", bg="#c62828", fg="white", font=("Arial", 9)).pack(anchor="w")
campo_cliente = tk.Entry(frame_cliente)
campo_cliente.pack(fill="x", pady=2)

tk.Button(frame_cliente, text="Gerar Nome Automático (Faker)", command=gerar_cliente, bg="#6a1b9a", fg="white", font=("Arial", 8)).pack(fill="x", pady=2)

tk.Label(frame_cliente, text="Forma de Pagamento:", bg="#c62828", fg="white", font=("Arial", 9)).pack(anchor="w", pady=(4, 1))
combo_pagamento = ttk.Combobox(frame_cliente, values=["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"], state="readonly")
combo_pagamento.pack(fill="x")

tk.Button(lado_direito, text="FINALIZAR PEDIDO DE LOJA", command=finalizar_pedido, bg="#2e7d32", fg="white", font=("Arial", 11, "bold")).pack(fill="x", pady=6)
tk.Button(lado_direito, text="Ver Histórico de Pedidos", command=mostrar_historico, bg="#333", fg="white", font=("Arial", 9)).pack(fill="x")

janela.protocol("WM_DELETE_WINDOW", fechar_programa)
janela.mainloop()