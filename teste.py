import customtkinter as ctk

# Inicializar o aplicativo
app = ctk.CTk()

# Criar um CTkFrame com borda
frame = ctk.CTkFrame(app, border_width=2, border_color="black")
frame.pack(pady=20, padx=20)

# Definir as opções do menu
options = ["Opção 1", "Opção 2", "Opção 3"]

# Criar o CTkOptionMenu dentro do frame
menu = ctk.CTkOptionMenu(frame, values=options)
menu.pack(pady=10, padx=10)

# Rodar o aplicativo
app.mainloop()
