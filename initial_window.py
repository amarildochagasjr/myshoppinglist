import customtkinter as ctk
from PIL import Image
from tkinter import ttk
import sqlite3

lista_compras = None

ctk.set_appearance_mode("dark")

def limitar_descricao(event, descricao_textbox):
    texto = descricao_textbox.get("1.0", "end-1c")  # Pega o texto inserido
    if len(texto) > 40:
        descricao_textbox.delete("1.0", "end")  # Limpa o texto atual
        descricao_textbox.insert("1.0", texto[:40])  # Coloca apenas os primeiros 50 caracteres

def optionmenu_callback(value):
    if value == "-Selecione-":
        print("Por favor, selecione uma opção válida.")
        return

def centralizar_janela(janela, largura, altura):
    # Obtendo o tamanho da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    # Calculando a posição para centralizar a janela
    x_pos = (largura_tela - largura) // 2
    y_pos = (altura_tela - altura) // 2

    # Definindo a posição centralizada
    janela.geometry(f"{largura}x{altura}+{x_pos}+{y_pos}")

def limpar_campos(nome, medida, quantidade, descricao):
    nome.delete(0, 'end')  # Limpa o campo de texto do nome
    medida.set("-Selecione-")  # Reseta o valor do OptionMenu
    quantidade.delete(0, 'end')  # Limpa o campo de texto da quantidade
    descricao.delete("1.0", "end")  # Limpa a Textbox de descrição

def conecta_bd():
    conn = sqlite3.connect("listas.bd")
    cursor = conn.cursor()

    print("Conectando ao bd")

    return conn, cursor

def desconecta_bd(conn):
    conn.close()
    print("Deconecta bd")

def monta_tabelas():
    conn, cursor = conecta_bd()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lista(
            cod_prod INTEGER PRIMARY KEY,
            nome_prod VARCHAR(50) NOT NULL,
            medida_prod VARCHAR(15) NOT NULL,
            quantidade_prod INTEGER NOT NULL,
            descricao_prod TEXT NOT NULL
        );
    """)
    conn.commit() 
    print("bd criado")
    desconecta_bd(conn)

def show_custom_messagebox(title, callback):
    # Criando a janela personalizada
    custom_window = ctk.CTkToplevel()
    custom_window.title(title)
    custom_window.resizable(False, False)

    if callback == "Adicionar":

        centralizar_janela(custom_window, 350, 200)

        custom_frame = ctk.CTkFrame(custom_window, width=340, height=193, fg_color="#2b2b2b")
        custom_frame.place(relx= 0.02, rely= 0.02)

        prodname_label = ctk.CTkLabel(custom_frame, text="Nome Produto  :", fg_color="#2b2b2b", text_color="white", font=("Roboto", 13, "bold"))
        prodname_label.place(relx= 0.02, rely= 0.04)

        prodname_entry = ctk.CTkEntry(custom_frame, width=228, height=25, placeholder_text="Digite o nome do produto", justify="center", border_color= "#7f4ae8")
        prodname_entry.place(relx= 0.31, rely= 0.05)

        proddesc_label = ctk.CTkLabel(custom_frame, text="Descrição Prod :", fg_color="#2b2b2b", text_color="white", font=("Roboto", 13, "bold"))
        proddesc_label.place(relx= 0.02, rely= 0.25)

        proddesc_text = ctk.CTkTextbox(custom_frame, width=228, height=50, fg_color="#2b2b2b",border_width= 2, border_color= "#7f4ae8")
        proddesc_text.place(relx= 0.31, rely= 0.25)

        # Para garantir que o campo de descrição não ultrapasse 50 caracteres
        proddesc_text.bind("<KeyRelease>", lambda event, widget=proddesc_text: limitar_descricao(event, widget))

        prodqtde_label = ctk.CTkLabel(custom_frame, text=("Quantidade     :").center(20), fg_color="#2b2b2b", text_color="white",font=("Roboto", 13, "bold"))
        prodqtde_label.place(relx= 0.02, rely= 0.58)

        prodqtde_entry = ctk.CTkEntry(custom_frame, width=55, height=25, justify="center", border_color= "#7f4ae8")
        prodqtde_entry.place(relx= 0.31, rely= 0.59)

        prodmedida_label = ctk.CTkLabel(custom_frame, text="Medida :", fg_color="#2b2b2b", text_color="white", font=("Roboto", 13, "bold"))
        prodmedida_label.place(relx= 0.50, rely= 0.58)

        medida_frame = ctk.CTkFrame(custom_window, width=106, height=28, fg_color="#2b2b2b", border_width= 2, border_color="#7f4ae8")
        medida_frame.place(relx= 0.67, rely= 0.58)

        prodmedida_entry = ctk.CTkOptionMenu(medida_frame, width=100, height=22, values=['Quilograma', 'Grama', 'Litro', 'Mililitro', 'Unidade', 'Metro', 'Centimetro'], 
                                             fg_color="#2b2b2b", bg_color="transparent", button_color="#7f4ae8", button_hover_color="#be48fa", dropdown_hover_color="#7f4ae8")
        prodmedida_entry.set("-Selecione-")
        prodmedida_entry.place(relx= 0.5, rely= 0.5, anchor="center")

        add_button = ctk.CTkButton(custom_frame, text="Adicionar", width= 75, height= 25, fg_color="#7f4ae8", hover_color="#be48fa", 
                                   command=lambda: adiciona_itens(prodname_entry, prodmedida_entry, prodqtde_entry, proddesc_text))
        add_button.place(relx= 0.50, rely= 0.88, anchor="center")

        btn_sair = ctk.CTkButton(custom_frame, text="Sair", width=20, height=15, fg_color= "#fa6457", hover_color= "#fa120e", command= custom_window.destroy)
        btn_sair.place(relx= 0.80, rely= 0.88, anchor="center")

    elif callback == "Remover":

        def button_ok(cod):
            item_cod = cod.get()

            conn, cursor = conecta_bd()

            cursor.execute("""
                SELECT nome_prod, quantidade_prod, medida_prod FROM lista WHERE cod_prod = ?;
            """, (item_cod,))
            
            resultado = cursor.fetchone()

            if resultado:
                nome_produto, quantidade, medida = resultado
                
                # Preenche os campos com os valores recuperados
                prodname_entry.configure(state="normal")  # Habilita antes de alterar
                prodname_entry.delete(0, 'end')
                prodname_entry.insert(0, nome_produto)
                prodname_entry.configure(state="disabled")  # Desabilita para impedir a edição

                prodqtde_entry.configure(state="normal")  # Habilita antes de alterar
                prodqtde_entry.delete(0, 'end')
                prodqtde_entry.insert(0, str(quantidade))
                prodqtde_entry.configure(state="disabled")  # Desabilita para impedir a edição

                prodmedida_entry.configure(state="normal")  # Habilita antes de alterar
                prodmedida_entry.delete(0, 'end')
                prodmedida_entry.insert(0, medida)
                prodmedida_entry.configure(state="disabled")
            else:
                print("Produto não encontrado.")

            conn.commit()
            desconecta_bd(conn)

        centralizar_janela(custom_window, 350, 200)

        custom_frame = ctk.CTkFrame(custom_window, width=340, height=193, fg_color="#2b2b2b")
        custom_frame.place(relx= 0.02, rely= 0.02)

        rminfo_label = ctk.CTkLabel(custom_frame, text="Digite o código do produto\ne clique em ok: ", fg_color="#2b2b2b", text_color="white", font=("Roboto", 15, "bold"))
        rminfo_label.place(relx= 0.50, rely= 0.12, anchor="center")

        rmcod_entry = ctk.CTkEntry(custom_frame, width=55, height=25,placeholder_text="Cód.", justify="center", border_color= "#7f4ae8")
        rmcod_entry.place(relx= 0.40, rely= 0.27)

        prodname_label = ctk.CTkLabel(custom_frame, text="Nome Produto  :", fg_color="#2b2b2b", text_color="white", font=("Roboto", 13, "bold"))
        prodname_label.place(relx= 0.02, rely= 0.44)

        prodname_entry = ctk.CTkEntry(custom_frame, width=228, height=25, justify="center", border_color= "#7f4ae8")
        prodname_entry.place(relx= 0.31, rely= 0.45)

        prodqtde_label = ctk.CTkLabel(custom_frame, text=("Quantidade     :").center(20), fg_color="#2b2b2b", text_color="white",font=("Roboto", 13, "bold"))
        prodqtde_label.place(relx= 0.02, rely= 0.63)

        prodqtde_entry = ctk.CTkEntry(custom_frame, width=55, height=25, justify="center", border_color= "#7f4ae8")
        prodqtde_entry.place(relx= 0.31, rely= 0.64)

        prodmedida_label = ctk.CTkLabel(custom_frame, text="Medida :", fg_color="#2b2b2b", text_color="white", font=("Roboto", 13, "bold"))
        prodmedida_label.place(relx= 0.50, rely= 0.63)

        prodmedida_entry = ctk.CTkEntry(custom_frame, width=106, height=25, justify="center", border_color= "#7f4ae8")
        prodmedida_entry.place(relx= 0.67, rely= 0.64)

        ok_button = ctk.CTkButton(custom_frame, text="ok", width= 50, height= 25, fg_color="#7f4ae8", hover_color="#be48fa",
                                      command= lambda: button_ok(rmcod_entry))
        ok_button.place(relx= 0.65, rely= 0.33, anchor="center")

        remove_button = ctk.CTkButton(custom_frame, text="Remover", width= 75, height= 25, fg_color="#7f4ae8", hover_color="#be48fa", 
                                      command= lambda: remove_itens(rmcod_entry, prodname_entry, prodqtde_entry, prodmedida_entry))
        remove_button.place(relx= 0.50, rely= 0.88, anchor="center")

        btn_sair = ctk.CTkButton(custom_frame, text="Sair", width=20, height=15, fg_color= "#fa6457", hover_color= "#fa120e", command= custom_window.destroy)
        btn_sair.place(relx= 0.80, rely= 0.88, anchor="center")

        
    else:
        centralizar_janela(custom_window, 300, 150)

        custom_frame = ctk.CTkFrame(custom_window, width=290, height=140, fg_color="#2b2b2b")
        custom_frame.place(relx= 0.50, rely= 0.50, anchor="center")

        message_label = ctk.CTkLabel(custom_frame, text=callback, fg_color="#2b2b2b", font=("Roboto", 14, "bold"), text_color="white")
        message_label.place(relx= 0.50, rely= 0.35, anchor="center")

        # Botão para fechar a caixa
        close_button = ctk.CTkButton(custom_frame, text="Fechar", fg_color="#7f4ae8", hover_color="#be48fa", command=custom_window.destroy)
        close_button.place(relx= 0.50, rely= 0.80, anchor="center")

def onclick(value):
    if value == "Adicionar":
        show_custom_messagebox("Adicionar", value)

    elif value == "Remover":
        show_custom_messagebox("Remover", value)
    
    elif value == "Search":
        show_custom_messagebox("Pesquisar", value)

def main_frame():

    nome = name_entry.get().strip()  # Obtém e limpa os espaços em branco do início e fim

    if nome == "":  # Se o nome estiver vazio
        show_custom_messagebox("Aviso", "O nome não pode ficar em branco!")
        return

    saudacao = f'Olá, {nome.title()}'

    global lista_compras

    initial_frame.forget()

    main_frame = ctk.CTkFrame(initial_window, width=500, height=700, fg_color= "#030117")
    main_frame.pack()

    logo2 = ctk.CTkImage(Image.open("images/my_shop.png"), size=(200,200))
    label_logo2 = ctk.CTkLabel(main_frame, image= logo2, text= None, fg_color= "#030117")
    label_logo2.place(relx= -0.13, rely= -0.08)

    hello_label = ctk.CTkLabel(main_frame, text= saudacao, fg_color= "#030117", font= bold_font_hello)
    hello_label.place(relx= 0.20, rely= 0.05)

    list_frame = ctk.CTkFrame(initial_window, width=480, height=350, fg_color= "#2b2b2b", border_width= 2, border_color= "#7f4ae8")
    list_frame.place(x=10,y=90)

    options_frame = ctk.CTkFrame(initial_window, width=480, height=120, fg_color= "#2b2b2b", border_width= 2, border_color= "#7f4ae8")
    options_frame.place(x=10,y=460)

    btn_add = ctk.CTkButton(options_frame, text="Adicionar", width=180, height=25, fg_color= "#7f4ae8", hover_color= "#be48fa", font= bold_font_button, command= lambda: onclick("Adicionar"))
    btn_add.place(relx= 0.08, rely= 0.17)

    btn_remove = ctk.CTkButton(options_frame, text="Remover", width=180, height=25, fg_color= "#7f4ae8", hover_color= "#be48fa", font= bold_font_button, command= lambda: onclick("Remover"))
    btn_remove.place(relx= 0.08, rely= 0.63)

    btn_search = ctk.CTkButton(options_frame, text="Pesquisar", width=180, height=25, fg_color= "#7f4ae8", hover_color= "#be48fa", font= bold_font_button, command= lambda: onclick("Pesquisar"))
    btn_search.place(relx= 0.54, rely= 0.17)

    btn_esc = ctk.CTkButton(options_frame, text="Sair", width=100, height=25, fg_color= "#fa6457", hover_color= "#fa120e", font= bold_font_button, command= initial_window.destroy)
    btn_esc.place(relx= 0.63, rely= 0.63)

    scroll_lista = ctk.CTkScrollbar(list_frame, fg_color="#2b2b2b",orientation="vertical")
    scroll_lista.place(relx= 0.966, rely= 0.03, relwidth=0.03, relheight= 0.92)

    scroll_lista2 = ctk.CTkScrollbar(list_frame, fg_color="#2b2b2b",orientation="horizontal")
    scroll_lista2.place(relx= 0.005, rely= 0.95, relwidth=0.97, relheight= 0.04)
    
    lista_compras = ttk.Treeview(list_frame, height= 3, column=("col1", "col2", "col3", "col4", "col5"))
    lista_compras.heading("#0", text="")
    lista_compras.heading("#1", text="Cód.")
    lista_compras.heading("#2", text="Nome")
    lista_compras.heading("#3", text="Medida")
    lista_compras.heading("#4", text="Qtde")
    lista_compras.heading("#5", text="Descrição")

    lista_compras.column("#0", anchor="center",width= 1)
    lista_compras.column("#1", anchor="center",width= 40)
    lista_compras.column("#2", anchor="center",width= 120)
    lista_compras.column("#3", anchor="center",width= 85)
    lista_compras.column("#4", anchor="center",width= 50)
    lista_compras.column("#5", anchor="center",width= 350)

    style = ttk.Style()

    # Alterar a cor de fundo geral da Treeview
    style.configure("Treeview", background="#1f1f1f", foreground="white", fieldbackground="#1f1f1f")
    style.configure("Treeview.Heading", background="white", foreground="#1f1f1f", font= bold_font_button)
    style.map("Treeview.Heading", background=[("active", "#be48fa")])

    # Alterar a cor de fundo das células selecionadas
    style.map("Treeview", background=[("selected", "#7f4ae8")])

    # Alterar a cor de fundo das linhas (usando tags)
    lista_compras.tag_configure('oddrow', background="#2b2b2b")
    lista_compras.tag_configure('evenrow', background="#1f1f1f")

    lista_compras.configure(yscrollcommand=scroll_lista.set, xscrollcommand=scroll_lista2.set)
    scroll_lista.configure(command=lista_compras.yview)
    scroll_lista2.configure(command=lista_compras.xview)

    lista_compras.place(relx= 0.01, rely= 0.02, relwidth=0.955, relheight= 0.92)

    select_lista(lista_compras)

    return lista_compras

def select_lista(lista_compras):
    conn, cursor = conecta_bd()

    lista_compras.delete(*lista_compras.get_children())

    lista = cursor.execute(""" 
        SELECT  cod_prod , nome_prod, medida_prod, quantidade_prod, descricao_prod FROM lista
            ORDER BY cod_prod ASC;
    """)
    for item in lista:
        lista_compras.insert("", "end", values=item)
    desconecta_bd(conn)

def adiciona_itens(nome, medida, quantidade, descricao):
    item_nome = nome.get().title()
    item_medida = medida.get()
    item_quant = quantidade.get()
    item_desc = descricao.get("1.0", "end").strip().capitalize()

    if item_nome == "":
        show_custom_messagebox("Erro", "Nome do produto obrigatório.")
        return

    if item_quant == "":
        show_custom_messagebox("Erro", "A quantidade é obrigatória.")
        return
    
    try:
        if '.' in item_quant:  # Verifica se é um float
            item_quant = float(item_quant)
        else:  # Caso contrário, trata como int
            item_quant = int(item_quant)
    except ValueError:
        show_custom_messagebox("Erro", "A quantidade deve ser um número válido!")
        return
    
    if item_medida == "-Selecione-":
        show_custom_messagebox("Erro", "Escolha uma opção válida para medida.")
        return

    conn, cursor = conecta_bd()

    cursor.execute("""
        INSERT INTO lista (nome_prod, medida_prod, quantidade_prod, descricao_prod)
            VALUES (?, ?, ?, ?)
    """, (item_nome, item_medida, item_quant, item_desc))

    conn.commit()
    desconecta_bd(conn)

    select_lista(lista_compras)

    show_custom_messagebox("Sucesso", "Item adicionado com sucesso!")

    limpar_campos(nome, medida, quantidade, descricao)

def remove_itens(cod, name, qtde, medida):
    # Criando a janela personalizada
    custom_window = ctk.CTkToplevel()
    custom_window.title("Remover")
    custom_window.resizable(False, False)

    centralizar_janela(custom_window, 300, 150)

    item_cod = cod.get()
    item_nome = name.get().title()
    item_quant = qtde.get()
    item_medida = medida.get()

    conn, cursor = conecta_bd()

    cursor.execute("""
        DELETE FROM lista WHERE cod_prod = ?;
    """, item_cod)

    custom_frame = ctk.CTkFrame(custom_window, width=290, height=140, fg_color="#2b2b2b")
    custom_frame.place(relx= 0.50, rely= 0.50, anchor="center")

    message_label = ctk.CTkLabel(custom_frame, text=f'Deseja realmente remover o item\n{item_nome}', fg_color="#2b2b2b", font=("Roboto", 14, "bold"), text_color="white")
    message_label.place(relx= 0.50, rely= 0.35, anchor="center")

    conn.commit()
    desconecta_bd(conn)

    select_lista(lista_compras)

    limpar_campos(item_cod, item_nome, item_quant, item_medida)

    #show_custom_messagebox("Remover", "Item removido com sucesso !")

"""def ondoubleclick():

    lista_compras.selection()
    remove"""


initial_window = ctk.CTk()

monta_tabelas()

#Configurando a janela
initial_window.title("My Shopping List")
initial_window.resizable(width= False, height= False)

# Fontes
bold_font_button = ctk.CTkFont(family="Roboto", size=15, weight="bold")
bold_font_hello = ctk.CTkFont(family="Roboto", size=20, weight="bold")

centralizar_janela(initial_window, 500, 700)

initial_frame = ctk.CTkFrame(initial_window, width=500, height=700, fg_color= "#030117")
initial_frame.pack()

logo = ctk.CTkImage(Image.open("images/my_shop.png"), size=(500,500))
label_logo = ctk.CTkLabel(initial_frame, image= logo, text= None, fg_color= "#030117")
label_logo.place(relx= 0.46, rely= 0.30, anchor= "center")

name_entry = ctk.CTkEntry (initial_frame, width=300, height=35, placeholder_text="Digite seu nome", justify="center", border_color= "#7f4ae8")
name_entry.place(relx= 0.50, rely= 0.50, anchor= "center")

btn_iniciar = ctk.CTkButton(initial_frame, text="Iniciar", fg_color= "#7f4ae8", hover_color= "#be48fa", command= main_frame)
btn_iniciar.place(relx= 0.50, rely= 0.60, anchor= "center")

#initial_window.after(3000, main_frame)

initial_window.mainloop()