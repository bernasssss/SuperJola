import os
import mysql.connector
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Conexão com a bases de dados
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='projetofinalpaw-projetofinal.k.aivencloud.com',
            port=28660,
            user='avnadmin',
            password='AVNS_9ObcOM992ixhN0yqF8B',
            database='defaultdb',
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None
    
# Funções de CRUD para Clientes
def adicionar_cliente(nome, telemovel, morada, email, data_nascimento):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, telemovel, morada, email, data_nascimento) VALUES (?, ?, ?, ?, ?)', 
                   (nome, telemovel, morada, email, data_nascimento))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# Funções de CRUD para Vinhos
def adicionar_vinho(nome, safra, preco, tipo, pais_origem):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vinhos (nome, safra, preco, tipo, pais_origem) VALUES (?, ?, ?, ?, ?)', 
                   (nome, safra, preco, tipo, pais_origem))
    conn.commit()
    conn.close()

def listar_vinhos():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vinhos')
    vinhos = cursor.fetchall()
    conn.close()
    return vinhos

# Função para criar pedidos
def criar_pedido(cliente_id, vinho_id, quantidade, data_pedido):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    # Buscar preço do vinho
    cursor.execute('SELECT preco FROM vinhos WHERE id = ?', (vinho_id,))
    vinho = cursor.fetchone()
    if not vinho:
        messagebox.showerror("Erro", "Vinho não encontrado!")
        return

    preco = vinho[0]
    total = preco * quantidade

    # Inserir pedido
    cursor.execute('''
    INSERT INTO pedidos (cliente_id, vinho_id, quantidade, total, data_pedido)
    VALUES (?, ?, ?, ?, ?)
    ''', (cliente_id, vinho_id, quantidade, total, data_pedido))

    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Pedido criado com sucesso!")

# Interface com Tkinter
def main_window():
    def atualizar_lista_clientes():
        for item in tree_clientes.get_children():
            tree_clientes.delete(item)
        clientes = listar_clientes()
        for cliente in clientes:
            tree_clientes.insert('', 'end', values=cliente)

    def atualizar_lista_vinhos():
        for item in tree_vinhos.get_children():
            tree_vinhos.delete(item)
        vinhos = listar_vinhos()
        for vinho in vinhos:
            tree_vinhos.insert('', 'end', values=vinho)

    def adicionar_cliente_callback():
        nome = entry_cliente_nome.get()
        telemovel = entry_cliente_telemovel.get()
        morada = entry_cliente_morada.get()
        email = entry_cliente_email.get()
        data_nascimento = entry_cliente_data_nascimento.get()
        if nome and telemovel and morada and email and data_nascimento:
            adicionar_cliente(nome, telemovel, morada, email, data_nascimento)
            atualizar_lista_clientes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def adicionar_vinho_callback():
        nome = entry_vinho_nome.get()
        try:
            safra = int(entry_vinho_safra.get())
            preco = float(entry_vinho_preco.get())
            tipo = entry_vinho_tipo.get()
            pais_origem = entry_vinho_pais_origem.get()
            if nome and safra > 0 and preco >= 0 and tipo and pais_origem:
                adicionar_vinho(nome, safra, preco, tipo, pais_origem)
                atualizar_lista_vinhos()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")
        except ValueError:
            messagebox.showwarning("Atenção", "Safra e preço devem ser valores válidos!")

    app = tk.Tk()
    app.title("ERP Vinhos")

    # Frame para o menu e o ícone
    top_frame = ttk.Frame(app)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Carregar a imagem
    try:
        image = Image.open("superjola.png")
        image = image.resize((80, 80), Image.Resampling.LANCZOS)  # Redimensionar a imagem
        photo = ImageTk.PhotoImage(image)
        print("Imagem carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        photo = None

    # Adicionar a imagem no canto superior direito
    if photo:
        label_image = ttk.Label(top_frame, image=photo)
        label_image.image = photo  # Manter uma referência da imagem
        label_image.pack(side=tk.RIGHT)
    else:
        print("Imagem não carregada, label não será exibido.")

    # Estilo moderno e sofisticado
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook", background="#4b2e2e", foreground="#ffffff", padding=10)
    style.configure("TNotebook.Tab", background="#4b2e2e", foreground="#ffffff", padding=10)
    style.map("TNotebook.Tab", background=[("selected", "#2e1c1c")], foreground=[("selected", "#ffffff")])

    style.configure("TFrame", background="#4b2e2e")
    style.configure("TLabel", background="#4b2e2e", foreground="#ffffff")
    style.configure("TEntry", fieldbackground="#2e1c1c", foreground="#ffffff")
    style.configure("TButton", background="#2e1c1c", foreground="#ffffff", padding=5)
    style.map("TButton", background=[("active", "#2e1c1c")], foreground=[("active", "#ffffff")])

    tab_control = ttk.Notebook(app)

    # Aba de Clientes
    tab_clientes = ttk.Frame(tab_control)
    tab_control.add(tab_clientes, text="Clientes")

    frame_cliente_form = ttk.Frame(tab_clientes)
    frame_cliente_form.pack(pady=10)

    ttk.Label(frame_cliente_form, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_cliente_nome = ttk.Entry(frame_cliente_form)
    entry_cliente_nome.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_cliente_form, text="Telemóvel:").grid(row=1, column=0, padx=5, pady=5)
    entry_cliente_telemovel = ttk.Entry(frame_cliente_form)
    entry_cliente_telemovel.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_cliente_form, text="Morada:").grid(row=2, column=0, padx=5, pady=5)
    entry_cliente_morada = ttk.Entry(frame_cliente_form)
    entry_cliente_morada.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_cliente_form, text="Email:").grid(row=3, column=0, padx=5, pady=5)
    entry_cliente_email = ttk.Entry(frame_cliente_form)
    entry_cliente_email.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_cliente_form, text="Data de Nascimento:").grid(row=4, column=0, padx=5, pady=5)
    entry_cliente_data_nascimento = ttk.Entry(frame_cliente_form)
    entry_cliente_data_nascimento.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(frame_cliente_form, text="Adicionar Cliente", command=adicionar_cliente_callback).grid(row=5, column=0, columnspan=2, pady=10)

    tree_clientes = ttk.Treeview(tab_clientes, columns=("ID", "Nome", "Telemóvel", "Morada", "Email", "Data de Nascimento"), show="headings")
    tree_clientes.heading("ID", text="ID")
    tree_clientes.heading("Nome", text="Nome")
    tree_clientes.heading("Telemóvel", text="Telemóvel")
    tree_clientes.heading("Morada", text="Morada")
    tree_clientes.heading("Email", text="Email")
    tree_clientes.heading("Data de Nascimento", text="Data de Nascimento")
    tree_clientes.pack(fill=tk.BOTH, expand=True)

    # Aba de Vinhos
    tab_vinhos = ttk.Frame(tab_control)
    tab_control.add(tab_vinhos, text="Vinhos")

    frame_vinho_form = ttk.Frame(tab_vinhos)
    frame_vinho_form.pack(pady=10)

    ttk.Label(frame_vinho_form, text="Nome do Vinho:").grid(row=0, column=0, padx=5, pady=5)
    entry_vinho_nome = ttk.Entry(frame_vinho_form)
    entry_vinho_nome.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_vinho_form, text="Safra:").grid(row=1, column=0, padx=5, pady=5)
    entry_vinho_safra = ttk.Entry(frame_vinho_form)
    entry_vinho_safra.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_vinho_form, text="Preço:").grid(row=2, column=0, padx=5, pady=5)
    entry_vinho_preco = ttk.Entry(frame_vinho_form)
    entry_vinho_preco.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_vinho_form, text="Tipo:").grid(row=3, column=0, padx=5, pady=5)
    entry_vinho_tipo = ttk.Entry(frame_vinho_form)
    entry_vinho_tipo.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_vinho_form, text="País de Origem:").grid(row=4, column=0, padx=5, pady=5)
    entry_vinho_pais_origem = ttk.Entry(frame_vinho_form)
    entry_vinho_pais_origem.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(frame_vinho_form, text="Adicionar Vinho", command=adicionar_vinho_callback).grid(row=5, column=0, columnspan=2, pady=10)

    tree_vinhos = ttk.Treeview(tab_vinhos, columns=("ID", "Nome", "Safra", "Preço", "Tipo", "País de Origem"), show="headings")
    tree_vinhos.heading("ID", text="ID")
    tree_vinhos.heading("Nome", text="Nome")
    tree_vinhos.heading("Safra", text="Safra")
    tree_vinhos.heading("Preço", text="Preço")
    tree_vinhos.heading("Tipo", text="Tipo")
    tree_vinhos.heading("País de Origem", text="País de Origem")
    tree_vinhos.pack(fill=tk.BOTH, expand=True)

    # Aba de Pedidos
    tab_pedidos = ttk.Frame(tab_control)
    tab_control.add(tab_pedidos, text="Pedidos")

    frame_pedido_form = ttk.Frame(tab_pedidos)
    frame_pedido_form.pack(pady=10)

    ttk.Label(frame_pedido_form, text="ID do Cliente:").grid(row=0, column=0, padx=5, pady=5)
    entry_pedido_cliente_id = ttk.Entry(frame_pedido_form)
    entry_pedido_cliente_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_pedido_form, text="ID do Vinho:").grid(row=1, column=0, padx=5, pady=5)
    entry_pedido_vinho_id = ttk.Entry(frame_pedido_form)
    entry_pedido_vinho_id.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_pedido_form, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5)
    entry_pedido_quantidade = ttk.Entry(frame_pedido_form)
    entry_pedido_quantidade.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_pedido_form, text="Data do Pedido:").grid(row=3, column=0, padx=5, pady=5)
    entry_pedido_data = ttk.Entry(frame_pedido_form)
    entry_pedido_data.grid(row=3, column=1, padx=5, pady=5)

    def adicionar_pedido_callback():
        cliente_id = entry_pedido_cliente_id.get()
        vinho_id = entry_pedido_vinho_id.get()
        quantidade = entry_pedido_quantidade.get()
        data_pedido = entry_pedido_data.get()
        if cliente_id and vinho_id and quantidade and data_pedido:
            criar_pedido(cliente_id, vinho_id, int(quantidade), data_pedido)
            atualizar_lista_pedidos()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    ttk.Button(frame_pedido_form, text="Adicionar Pedido", command=adicionar_pedido_callback).grid(row=4, column=0, columnspan=2, pady=10)

    tree_pedidos = ttk.Treeview(tab_pedidos, columns=("ID", "ID do Cliente", "ID do Vinho", "Quantidade", "Total", "Data do Pedido"), show="headings")
    tree_pedidos.heading("ID", text="ID")
    tree_pedidos.heading("ID do Cliente", text="ID do Cliente")
    tree_pedidos.heading("ID do Vinho", text="ID do Vinho")
    tree_pedidos.heading("Quantidade", text="Quantidade")
    tree_pedidos.heading("Total", text="Total")
    tree_pedidos.heading("Data do Pedido", text="Data do Pedido")
    tree_pedidos.pack(fill=tk.BOTH, expand=True)

    def atualizar_lista_pedidos():
        for item in tree_pedidos.get_children():
            tree_pedidos.delete(item)
        conn = sqlite3.connect('erp_vinhos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pedidos')
        pedidos = cursor.fetchall()
        conn.close()
        for pedido in pedidos:
            tree_pedidos.insert('', 'end', values=pedido)

    tab_control.pack(expand=True, fill=tk.BOTH)

    atualizar_lista_clientes()
    atualizar_lista_vinhos()
    atualizar_lista_pedidos()

    app.mainloop()

# Inicializar banco de dados e executar o sistema
if __name__ == "__main__":
    main_window()