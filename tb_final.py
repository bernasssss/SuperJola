import os
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry  # Widget para seleção de data com calendário
import datetime

# Conexão com a base de dados MySQL
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
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO clientes (nome, telemovel, morada, email, data_nascimento) VALUES (%s, %s, %s, %s, %s)',
        (nome, telemovel, morada, email, data_nascimento)
    )
    conn.commit()
    conn.close()

def listar_clientes():
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def remover_cliente(cliente_id):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
    conn.commit()
    conn.close()

def atualizar_cliente_edicao(cliente_id, nome, telemovel, morada, email, data_nascimento):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET nome=%s, telemovel=%s, morada=%s, email=%s, data_nascimento=%s WHERE id=%s",
        (nome, telemovel, morada, email, data_nascimento, cliente_id)
    )
    conn.commit()
    conn.close()

# Funções de CRUD para Vinhos
def adicionar_vinho(nome, safra, preco, tipo, pais_origem):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO vinhos (nome, safra, preco, tipo, pais_origem) VALUES (%s, %s, %s, %s, %s)',
        (nome, safra, preco, tipo, pais_origem)
    )
    conn.commit()
    conn.close()

def listar_vinhos():
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vinhos')
    vinhos = cursor.fetchall()
    conn.close()
    return vinhos

def remover_vinho(vinho_id):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vinhos WHERE id = %s", (vinho_id,))
    conn.commit()
    conn.close()

def atualizar_vinho_edicao(vinho_id, nome, safra, preco, tipo, pais_origem):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE vinhos SET nome=%s, safra=%s, preco=%s, tipo=%s, pais_origem=%s WHERE id=%s",
        (nome, safra, preco, tipo, pais_origem, vinho_id)
    )
    conn.commit()
    conn.close()

# Funções de CRUD para Pedidos
def criar_pedido(cliente_id, vinho_id, quantidade, data_pedido):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    # Buscar preço do vinho
    cursor.execute('SELECT preco FROM vinhos WHERE id = %s', (vinho_id,))
    vinho = cursor.fetchone()
    if not vinho:
        messagebox.showerror("Erro", "Vinho não encontrado!")
        conn.close()
        return
    preco = vinho[0]
    total = preco * quantidade
    cursor.execute(
        'INSERT INTO pedidos (cliente_id, vinho_id, quantidade, total, data_pedido) VALUES (%s, %s, %s, %s, %s)',
        (cliente_id, vinho_id, quantidade, total, data_pedido)
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Pedido criado com sucesso!")

def listar_pedidos():
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return []
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, CONCAT(c.id, ' - ', c.nome), CONCAT(v.id, ' - ', v.nome), p.quantidade, p.total, p.data_pedido
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        JOIN vinhos v ON p.vinho_id = v.id
    ''')
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def remover_pedido(pedido_id):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (pedido_id,))
    conn.commit()
    conn.close()

def atualizar_pedido_edicao(pedido_id, cliente_id, vinho_id, quantidade, data_pedido):
    conn = get_db_connection()
    if conn is None:
        messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
        return
    cursor = conn.cursor()
    # Recalcular o total com base no preço do vinho
    cursor.execute("SELECT preco FROM vinhos WHERE id = %s", (vinho_id,))
    vinho = cursor.fetchone()
    if not vinho:
        messagebox.showerror("Erro", "Vinho não encontrado!")
        conn.close()
        return
    preco = vinho[0]
    total = preco * quantidade
    cursor.execute(
        "UPDATE pedidos SET cliente_id=%s, vinho_id=%s, quantidade=%s, total=%s, data_pedido=%s WHERE id=%s",
        (cliente_id, vinho_id, quantidade, total, data_pedido, pedido_id)
    )
    conn.commit()
    conn.close()

# Interface com Tkinter
def main_window():
    app = tk.Tk()
    app.title("ERP Vinhos")

    # Função para atualizar os valores dos Comboboxes dos pedidos
    def atualizar_combobox_pedidos():
        combo_pedido_cliente_id['values'] = [str(cliente[0]) for cliente in listar_clientes()]
        combo_pedido_vinho_id['values'] = [str(vinho[0]) for vinho in listar_vinhos()]

    # Funções para atualizar as listas dos Treeviews
    def atualizar_lista_clientes():
        for item in tree_clientes.get_children():
            tree_clientes.delete(item)
        for cliente in listar_clientes():
            tree_clientes.insert('', 'end', values=cliente)

    def atualizar_lista_vinhos():
        for item in tree_vinhos.get_children():
            tree_vinhos.delete(item)
        for vinho in listar_vinhos():
            tree_vinhos.insert('', 'end', values=vinho)

    def atualizar_lista_pedidos():
        for item in tree_pedidos.get_children():
            tree_pedidos.delete(item)
        for pedido in listar_pedidos():
            tree_pedidos.insert('', 'end', values=pedido)

    # Callbacks para adição
    def adicionar_cliente_callback():
        nome = entry_cliente_nome.get()
        telemovel = entry_cliente_telemovel.get()
        morada = entry_cliente_morada.get()
        email = entry_cliente_email.get()
        data_nascimento = entry_cliente_data_nascimento.get()
        if not email.endswith('@gmail.com'):
            messagebox.showwarning("Atenção", "O email deve conter '@gmail.com'")
            return
        if nome and telemovel and morada and email and data_nascimento:
            adicionar_cliente(nome, telemovel, morada, email, data_nascimento)
            atualizar_lista_clientes()
            atualizar_combobox_pedidos()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    def adicionar_vinho_callback():
        nome = entry_vinho_nome.get()
        try:
            safra = datetime.datetime.strptime(entry_vinho_safra.get(), '%d/%m/%Y').date()
            if safra > datetime.date.today():
                messagebox.showwarning("Atenção", "A safra não pode ser uma data futura!")
                return
            preco = float(entry_vinho_preco.get())
            tipo = entry_vinho_tipo.get()
            pais_origem = entry_vinho_pais_origem.get()
            if nome and preco >= 0 and tipo and pais_origem:
                adicionar_vinho(nome, safra, preco, tipo, pais_origem)
                atualizar_lista_vinhos()
                atualizar_combobox_pedidos()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")
        except ValueError:
            messagebox.showwarning("Atenção", "Safra deve ser uma data válida e preço deve ser um valor numérico!")

    def adicionar_pedido_callback():
        cliente_id = combo_pedido_cliente_id.get()
        vinho_id = combo_pedido_vinho_id.get()
        quantidade = entry_pedido_quantidade.get()
        data_pedido = entry_pedido_data.get()
        if cliente_id and vinho_id and quantidade and data_pedido:
            criar_pedido(cliente_id, vinho_id, int(quantidade), data_pedido)
            atualizar_lista_pedidos()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    # Callbacks para remoção
    def remover_cliente_callback():
        selecionado = tree_clientes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para remover!")
            return
        cliente_id = tree_clientes.item(selecionado[0])["values"][0]
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este cliente?"):
            remover_cliente(cliente_id)
            atualizar_lista_clientes()
            atualizar_combobox_pedidos()

    def remover_vinho_callback():
        selecionado = tree_vinhos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um vinho para remover!")
            return
        vinho_id = tree_vinhos.item(selecionado[0])["values"][0]
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este vinho?"):
            remover_vinho(vinho_id)
            atualizar_lista_vinhos()
            atualizar_combobox_pedidos()

    def remover_pedido_callback():
        selecionado = tree_pedidos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para remover!")
            return
        pedido_id = tree_pedidos.item(selecionado[0])["values"][0]
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este pedido?"):
            remover_pedido(pedido_id)
            atualizar_lista_pedidos()

    # Callbacks para edição
    def editar_cliente_callback():
        selecionado = tree_clientes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar!")
            return
        cliente = tree_clientes.item(selecionado[0])["values"]
        cliente_id = cliente[0]
        edit_window = tk.Toplevel(app)
        edit_window.title("Editar Cliente")
        edit_window.configure(bg="#4b2e2e")
        ttk.Label(edit_window, text="Nome:", background="#4b2e2e").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = ttk.Entry(edit_window)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, cliente[1])
        ttk.Label(edit_window, text="Telemóvel:", background="#4b2e2e").grid(row=1, column=0, padx=5, pady=5)
        entry_telemovel = ttk.Entry(edit_window)
        entry_telemovel.grid(row=1, column=1, padx=5, pady=5)
        entry_telemovel.insert(0, cliente[2])
        ttk.Label(edit_window, text="Morada:", background="#4b2e2e").grid(row=2, column=0, padx=5, pady=5)
        entry_morada = ttk.Entry(edit_window)
        entry_morada.grid(row=2, column=1, padx=5, pady=5)
        entry_morada.insert(0, cliente[3])
        ttk.Label(edit_window, text="Email:", background="#4b2e2e").grid(row=3, column=0, padx=5, pady=5)
        entry_email = ttk.Entry(edit_window)
        entry_email.grid(row=3, column=1, padx=5, pady=5)
        entry_email.insert(0, cliente[4])
        ttk.Label(edit_window, text="Data de Nascimento:", background="#4b2e2e").grid(row=4, column=0, padx=5, pady=5)
        entry_data = DateEntry(edit_window, date_pattern='dd/mm/yyyy')
        entry_data.grid(row=4, column=1, padx=5, pady=5)
        entry_data.set_date(cliente[5])
        
        def salvar_cliente():
            novo_nome = entry_nome.get()
            novo_telemovel = entry_telemovel.get()
            nova_morada = entry_morada.get()
            novo_email = entry_email.get()
            nova_data = entry_data.get()
            if not novo_email.endswith('@gmail.com'):
                messagebox.showwarning("Atenção", "O email deve conter '@gmail.com'")
                return
            if novo_nome and novo_telemovel and nova_morada and novo_email and nova_data:
                atualizar_cliente_edicao(cliente_id, novo_nome, novo_telemovel, nova_morada, novo_email, nova_data)
                atualizar_lista_clientes()
                edit_window.destroy()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
        
        ttk.Button(edit_window, text="Aplicar Mudanças", command=salvar_cliente).grid(row=5, column=0, columnspan=2, pady=10)

    def editar_vinho_callback():
        selecionado = tree_vinhos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um vinho para editar!")
            return
        vinho = tree_vinhos.item(selecionado[0])["values"]
        vinho_id = vinho[0]
        edit_window = tk.Toplevel(app)
        edit_window.title("Editar Vinho")
        edit_window.configure(bg="#4b2e2e")
        ttk.Label(edit_window, text="Nome do Vinho:", background="#4b2e2e").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = ttk.Entry(edit_window)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_nome.insert(0, vinho[1])
        ttk.Label(edit_window, text="Safra:", background="#4b2e2e").grid(row=1, column=0, padx=5, pady=5)
        entry_safra = ttk.Entry(edit_window)
        entry_safra.grid(row=1, column=1, padx=5, pady=5)
        entry_safra.insert(0, vinho[2])
        ttk.Label(edit_window, text="Preço:", background="#4b2e2e").grid(row=2, column=0, padx=5, pady=5)
        entry_preco = ttk.Entry(edit_window)
        entry_preco.grid(row=2, column=1, padx=5, pady=5)
        entry_preco.insert(0, vinho[3])
        ttk.Label(edit_window, text="Tipo:", background="#4b2e2e").grid(row=3, column=0, padx=5, pady=5)
        entry_tipo = ttk.Entry(edit_window)
        entry_tipo.grid(row=3, column=1, padx=5, pady=5)
        entry_tipo.insert(0, vinho[4])
        ttk.Label(edit_window, text="País de Origem:", background="#4b2e2e").grid(row=4, column=0, padx=5, pady=5)
        entry_pais = ttk.Entry(edit_window)
        entry_pais.grid(row=4, column=1, padx=5, pady=5)
        entry_pais.insert(0, vinho[5])
        
        def salvar_vinho():
            novo_nome = entry_nome.get()
            try:
                nova_safra = int(entry_safra.get())
            except ValueError:
                messagebox.showwarning("Atenção", "Safra deve ser um número inteiro!")
                return
            try:
                novo_preco = float(entry_preco.get())
            except ValueError:
                messagebox.showwarning("Atenção", "Preço deve ser um número!")
                return
            novo_tipo = entry_tipo.get()
            novo_pais = entry_pais.get()
            if novo_nome and nova_safra and novo_preco >= 0 and novo_tipo and novo_pais:
                atualizar_vinho_edicao(vinho_id, novo_nome, nova_safra, novo_preco, novo_tipo, novo_pais)
                atualizar_lista_vinhos()
                edit_window.destroy()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos corretamente!")
        
        ttk.Button(edit_window, text="Aplicar Mudanças", command=salvar_vinho).grid(row=5, column=0, columnspan=2, pady=10)

    def editar_pedido_callback():
        selecionado = tree_pedidos.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para editar!")
            return
        pedido = tree_pedidos.item(selecionado[0])["values"]
        pedido_id = pedido[0]
        edit_window = tk.Toplevel(app)
        edit_window.title("Editar Pedido")
        edit_window.configure(bg="#4b2e2e")
        ttk.Label(edit_window, text="ID do Cliente:", background="#4b2e2e").grid(row=0, column=0, padx=5, pady=5)
        combo_cliente = ttk.Combobox(edit_window)
        combo_cliente['values'] = [str(cliente[0]) for cliente in listar_clientes()]
        combo_cliente.grid(row=0, column=1, padx=5, pady=5)
        combo_cliente.set(pedido[1])
        ttk.Label(edit_window, text="ID do Vinho:", background="#4b2e2e").grid(row=1, column=0, padx=5, pady=5)
        combo_vinho = ttk.Combobox(edit_window)
        combo_vinho['values'] = [str(vinho[0]) for vinho in listar_vinhos()]
        combo_vinho.grid(row=1, column=1, padx=5, pady=5)
        combo_vinho.set(pedido[2])
        ttk.Label(edit_window, text="Quantidade:", background="#4b2e2e").grid(row=2, column=0, padx=5, pady=5)
        entry_quantidade = ttk.Entry(edit_window)
        entry_quantidade.grid(row=2, column=1, padx=5, pady=5)
        entry_quantidade.insert(0, pedido[3])
        ttk.Label(edit_window, text="Data do Pedido:", background="#4b2e2e").grid(row=3, column=0, padx=5, pady=5)
        entry_data = DateEntry(edit_window, date_pattern='dd/mm/yyyy')
        entry_data.grid(row=3, column=1, padx=5, pady=5)
        entry_data.set_date(pedido[5])
        
        def salvar_pedido():
            novo_cliente = combo_cliente.get()
            novo_vinho = combo_vinho.get()
            try:
                nova_quantidade = int(entry_quantidade.get())
            except ValueError:
                messagebox.showwarning("Atenção", "Quantidade deve ser um número inteiro!")
                return
            nova_data = entry_data.get()
            if novo_cliente and novo_vinho and nova_quantidade and nova_data:
                atualizar_pedido_edicao(pedido_id, novo_cliente, novo_vinho, nova_quantidade, nova_data)
                atualizar_lista_pedidos()
                edit_window.destroy()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
        
        ttk.Button(edit_window, text="Aplicar Mudanças", command=salvar_pedido).grid(row=4, column=0, columnspan=2, pady=10)

    # Aba extra para cálculo automático da data de extração da pipa
    def calcular_extracao(event=None):
        # Obter a data de engarrafamento (retorna um objeto datetime.date)
        data_inicial = data_engarrafamento.get_date()
        try:
            dias = int(dias_extracao.get())
        except ValueError:
            dias = 45
        data_extracao = data_inicial + datetime.timedelta(days=dias)
        label_data_extracao.config(text=data_extracao.strftime("%d/%m/%Y"))

    # Configuração da interface principal
    top_frame = ttk.Frame(app)
    top_frame.pack(side=tk.TOP, fill=tk.X)
    try:
        image = Image.open("superjola.png")
        image = image.resize((80, 80), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        print("Imagem carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")
        photo = None
    if photo:
        label_image = ttk.Label(top_frame, image=photo)
        label_image.image = photo
        label_image.pack(side=tk.RIGHT)
    else:
        print("Imagem não carregada, label não será exibido.")
    
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
    entry_cliente_data_nascimento = DateEntry(frame_cliente_form, date_pattern='dd/mm/yyyy')
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
    ttk.Button(tab_clientes, text="Editar Cliente", command=editar_cliente_callback).pack(pady=5)
    ttk.Button(tab_clientes, text="Remover Cliente", command=remover_cliente_callback).pack(pady=5)
    
    # Aba de Vinhos
    tab_vinhos = ttk.Frame(tab_control)
    tab_control.add(tab_vinhos, text="Vinhos")
    frame_vinho_form = ttk.Frame(tab_vinhos)
    frame_vinho_form.pack(pady=10)
    ttk.Label(frame_vinho_form, text="Nome do Vinho:").grid(row=0, column=0, padx=5, pady=5)
    entry_vinho_nome = ttk.Entry(frame_vinho_form)
    entry_vinho_nome.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(frame_vinho_form, text="Safra:").grid(row=1, column=0, padx=5, pady=5)
    entry_vinho_safra = DateEntry(frame_vinho_form, date_pattern='dd/mm/yyyy')
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
    ttk.Button(tab_vinhos, text="Editar Vinho", command=editar_vinho_callback).pack(pady=5)
    ttk.Button(tab_vinhos, text="Remover Vinho", command=remover_vinho_callback).pack(pady=5)
    
    # Aba de Pedidos
    tab_pedidos = ttk.Frame(tab_control)
    tab_control.add(tab_pedidos, text="Pedidos")
    frame_pedido_form = ttk.Frame(tab_pedidos)
    frame_pedido_form.pack(pady=10)
    ttk.Label(frame_pedido_form, text="ID do Cliente:").grid(row=0, column=0, padx=5, pady=5)
    combo_pedido_cliente_id = ttk.Combobox(frame_pedido_form)
    combo_pedido_cliente_id.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(frame_pedido_form, text="ID do Vinho:").grid(row=1, column=0, padx=5, pady=5)
    combo_pedido_vinho_id = ttk.Combobox(frame_pedido_form)
    combo_pedido_vinho_id.grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(frame_pedido_form, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5)
    entry_pedido_quantidade = ttk.Entry(frame_pedido_form)
    entry_pedido_quantidade.grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(frame_pedido_form, text="Data do Pedido:").grid(row=3, column=0, padx=5, pady=5)
    entry_pedido_data = DateEntry(frame_pedido_form, date_pattern='dd/mm/yyyy')
    entry_pedido_data.grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(frame_pedido_form, text="Adicionar Pedido", command=adicionar_pedido_callback).grid(row=4, column=0, columnspan=2, pady=10)
    tree_pedidos = ttk.Treeview(tab_pedidos, columns=("ID", "ID do Cliente", "ID do Vinho", "Quantidade", "Total", "Data do Pedido"), show="headings")
    tree_pedidos.heading("ID", text="ID")
    tree_pedidos.heading("ID do Cliente", text="ID do Cliente")
    tree_pedidos.heading("ID do Vinho", text="ID do Vinho")
    tree_pedidos.heading("Quantidade", text="Quantidade")
    tree_pedidos.heading("Total", text="Total")
    tree_pedidos.heading("Data do Pedido", text="Data do Pedido")
    tree_pedidos.pack(fill=tk.BOTH, expand=True)
    ttk.Button(tab_pedidos, text="Editar Pedido", command=editar_pedido_callback).pack(pady=5)
    ttk.Button(tab_pedidos, text="Remover Pedido", command=remover_pedido_callback).pack(pady=5)
    
    # Aba de Extração da Pipa
    tab_extracao = ttk.Frame(tab_control)
    tab_control.add(tab_extracao, text="Extração da Pipa")

    frame_extracao = ttk.Frame(tab_extracao)
    frame_extracao.pack(pady=10)

    ttk.Label(frame_extracao, text="ID do Vinho:", background="#4b2e2e", foreground="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo_vinho_id_extracao = ttk.Combobox(frame_extracao)
    combo_vinho_id_extracao['values'] = [str(vinho[0]) for vinho in listar_vinhos()]
    combo_vinho_id_extracao.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_extracao, text="Data de Engarrafamento:", background="#4b2e2e", foreground="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    data_engarrafamento = DateEntry(frame_extracao, date_pattern='dd/mm/yyyy')
    data_engarrafamento.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame_extracao, text="Dias para Extração:", background="#4b2e2e", foreground="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    dias_extracao = ttk.Entry(frame_extracao)
    dias_extracao.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    dias_extracao.insert(0, "45")

    ttk.Label(frame_extracao, text="Data de Extração:", background="#4b2e2e", foreground="#ffffff").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    label_data_extracao = ttk.Label(frame_extracao, text="", background="#4b2e2e", foreground="#ffffff")
    label_data_extracao.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    def calcular_extracao(event=None):
        data_inicial = data_engarrafamento.get_date()
        try:
            dias = int(dias_extracao.get())
        except ValueError:
            dias = 45
        data_extracao = data_inicial + datetime.timedelta(days=dias)
        label_data_extracao.config(text=data_extracao.strftime("%d/%m/%Y"))

    def salvar_extracao():
        vinho_id = combo_vinho_id_extracao.get()
        data_enga = data_engarrafamento.get()
        dias_enga = dias_extracao.get()
        data_extra = label_data_extracao.cget("text")
        if vinho_id and data_enga and dias_enga and data_extra:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
                return
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO extracao (vinho_id, data_enga, dias_enga, data_extra) VALUES (%s, %s, %s, %s)',
                (vinho_id, data_enga, dias_enga, data_extra)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Extração salva com sucesso!")
            atualizar_lista_extracoes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")

    ttk.Button(frame_extracao, text="Salvar Extração", command=salvar_extracao).grid(row=4, column=0, columnspan=2, pady=10)

    data_engarrafamento.bind("<<DateEntrySelected>>", calcular_extracao)
    dias_extracao.bind("<KeyRelease>", calcular_extracao)
    calcular_extracao()  # cálculo inicial

    # Tabela de Extrações
    tree_extracoes = ttk.Treeview(tab_extracao, columns=("ID", "ID do Vinho", "Data de Engarrafamento", "Dias para Extração", "Data de Extração"), show="headings")
    tree_extracoes.heading("ID", text="ID")
    tree_extracoes.heading("ID do Vinho", text="ID do Vinho")
    tree_extracoes.heading("Data de Engarrafamento", text="Data de Engarrafamento")
    tree_extracoes.heading("Dias para Extração", text="Dias para Extração")
    tree_extracoes.heading("Data de Extração", text="Data de Extração")
    tree_extracoes.pack(fill=tk.BOTH, expand=True)

    def listar_extracoes():
        conn = get_db_connection()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar à base de dados!")
            return []
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, v.nome, e.data_enga, e.dias_enga, e.data_extra
            FROM extracao e
            JOIN vinhos v ON e.vinho_id = v.id
        ''')
        extracoes = cursor.fetchall()
        conn.close()
        return extracoes

    def atualizar_lista_extracoes():
        for item in tree_extracoes.get_children():
            tree_extracoes.delete(item)
        for extracao in listar_extracoes():
            #print("Carregando extração:", extracao)  # Depuração
            # Formatar as datas para exibição
            extracao_formatada = (
                extracao[0],
                extracao[1],
                extracao[2],
                extracao[3],
                extracao[4]
            )
            tree_extracoes.insert('', 'end', values=extracao_formatada)

    def remover_extracao_callback():
        selecionado = tree_extracoes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma extração para remover!")
            return
        extracao_id = tree_extracoes.item(selecionado[0])["values"][0]
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover esta extração?"):
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
                return
            cursor = conn.cursor()
            cursor.execute("DELETE FROM extracao WHERE id = %s", (extracao_id,))
            conn.commit()
            conn.close()
            atualizar_lista_extracoes()
            messagebox.showinfo("Sucesso", "Extração removida com sucesso!")

    def editar_extracao_callback():
        selecionado = tree_extracoes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma extração para editar!")
            return
        extracao = tree_extracoes.item(selecionado[0])["values"]
        extracao_id = extracao[0]
        edit_window = tk.Toplevel(app)
        edit_window.title("Editar Extração")
        edit_window.configure(bg="#4b2e2e")
        ttk.Label(edit_window, text="ID do Vinho:", background="#4b2e2e").grid(row=0, column=0, padx=5, pady=5)
        combo_vinho = ttk.Combobox(edit_window)
        combo_vinho['values'] = [str(vinho[0]) for vinho in listar_vinhos()]
        combo_vinho.grid(row=0, column=1, padx=5, pady=5)
        combo_vinho.set(extracao[1])
        ttk.Label(edit_window, text="Data de Engarrafamento:", background="#4b2e2e").grid(row=1, column=0, padx=5, pady=5)
        entry_data_enga = DateEntry(edit_window, date_pattern='dd/mm/yyyy')
        entry_data_enga.grid(row=1, column=1, padx=5, pady=5)
        entry_data_enga.set_date(datetime.datetime.strptime(extracao[2], '%d/%m/%Y'))
        ttk.Label(edit_window, text="Dias para Extração:", background="#4b2e2e").grid(row=2, column=0, padx=5, pady=5)
        entry_dias_enga = ttk.Entry(edit_window)
        entry_dias_enga.grid(row=2, column=1, padx=5, pady=5)
        entry_dias_enga.insert(0, extracao[3])
        ttk.Label(edit_window, text="Data de Extração:", background="#4b2e2e").grid(row=3, column=0, padx=5, pady=5)
        entry_data_extra = ttk.Entry(edit_window)
        entry_data_extra.grid(row=3, column=1, padx=5, pady=5)
        entry_data_extra.insert(0, extracao[4])

        def salvar_extracao_editada():
            novo_vinho_id = combo_vinho.get()
            nova_data_enga = entry_data_enga.get()
            novos_dias_enga = entry_dias_enga.get()
            nova_data_extra = entry_data_extra.get()
            if novo_vinho_id and nova_data_enga and novos_dias_enga and nova_data_extra:
                conn = get_db_connection()
                if conn is None:
                    messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados!")
                    return
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE extracao SET vinho_id=%s, data_engarrafamento=%s, dias_engarrafamento=%s, data_extracao=%s WHERE id=%s",
                    (novo_vinho_id, nova_data_enga, novos_dias_enga, nova_data_extra, extracao_id)
                )
                conn.commit()
                conn.close()
                atualizar_lista_extracoes()
                edit_window.destroy()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")

        ttk.Button(edit_window, text="Aplicar Mudanças", command=salvar_extracao_editada).grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(tab_extracao, text="Editar Extração", command=editar_extracao_callback).pack(pady=5)
    ttk.Button(tab_extracao, text="Remover Extração", command=remover_extracao_callback).pack(pady=5)

    tab_control.pack(expand=True, fill=tk.BOTH)
    # Criando a função para atualizar todas as abas
    def atualizar_todas_as_listas():
        atualizar_lista_clientes()
        atualizar_lista_vinhos()
        atualizar_lista_pedidos()
        atualizar_lista_extracoes()

    # Função que detecta a mudança de aba e atualiza os dados
    def on_tab_selected(event):
        atualizar_todas_as_listas()

    # Associando o evento de mudança de aba
    tab_control.bind("<<NotebookTabChanged>>", on_tab_selected)

    tab_control.pack(expand=True, fill=tk.BOTH)

    # Garantindo que os dados sejam carregados na primeira execução
    atualizar_todas_as_listas()
    atualizar_combobox_pedidos()
    app.mainloop()

if __name__ == "__main__":
    main_window()