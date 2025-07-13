# Importações necessárias
import customtkinter as ctk                 # Interface moderna baseada em Tkinter
import tkinter as tk                        # Biblioteca padrão para GUI em Python
from tkinter import messagebox              # Janela de mensagens (erro, alerta, info)
from PIL import Image                       # Manipulação de imagens
import mysql.connector                      # Conexão com banco de dados MySQL
import bcrypt                               # Criptografia de senhas

"""
Sistema de Gestão de Saúde - VidaPlus
Desenvolvido por: Marcos Luís de Oliveira Silva
RU: 4330689

Descrição:
Este sistema foi desenvolvido utilizando Python com a biblioteca CustomTkinter para a interface gráfica
e MySQL para o banco de dados. Ele tem como objetivo gerenciar o acesso e as funções de três tipos de usuários:
Administrador, Médico e Paciente.

Funcionalidades principais:
- Login com autenticação criptografada (bcrypt) e validação de hierarquia (Administrador, Médico ou Paciente).
- Cadastro de novos usuários com controle de permissões.
- Interface personalizada para cada tipo de usuário:
  • Administrador: pode atualizar dados de médicos e pacientes.
  • Médico: pode atualizar seu cadastro e visualizar agendamentos de pacientes.
  • Paciente: pode atualizar seus dados e agendar consultas.
- Agendamento de consultas vinculando paciente a médico, com data, hora e observações.
- Consulta de agendamentos para o paciente logado.

O sistema busca ser simples, funcional e com foco em segurança básica de dados e experiência do usuário.

Requisitos:
- Python 3.x
- Biblioteca CustomTkinter
- Biblioteca bcrypt
- Banco de dados MySQL com as tabelas `usuarios` e `agendamentos` corretamente estruturadas.
"""

# ---------- Validação de login ----------
def validar_login(usuario_digitado, senha_digitada, janela_login, hierarquia_esperada):
    try:
        # Conectando ao banco de dados
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='890866', 
            database='vidaplus'
        )

        cursor = conexao.cursor()
        # Consulta para buscar senha e hierarquia do usuário
        query = "SELECT senha, hierarquia FROM usuarios WHERE usuario = %s"
        cursor.execute(query, (usuario_digitado,))
        resultado = cursor.fetchone()

        if resultado:
            senha_banco, hierarquia_banco = resultado
            # Verifica se a senha informada corresponde à senha criptografada do banco
            if bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_banco.encode('utf-8')):
                # Define permissões por hierarquia
                permissoesValidas = {
                    'Administrador': ['Administrador'],
                    'Medico': ['Administrador', 'Medico'],
                    'Paciente': ['Paciente']
                }
                # Verifica se o usuário tem permissão para acessar com a hierarquia informada
                if hierarquia_banco in permissoesValidas[hierarquia_esperada]:
                    global usuario_logado
                    usuario_logado = usuario_digitado  # Armazena o nome do usuário logado
                    messagebox.showinfo("Login", f"Login bem-sucedido como {hierarquia_banco}!")
                    janela_login.destroy()
                    # Abre a tela conforme o tipo de usuário
                    if hierarquia_banco == 'Administrador':
                        tela_principal_adm()
                    elif hierarquia_banco == 'Medico':
                        tela_principal_medico()
                    else:
                        tela_principal_paciente()
                else:
                    # Usuário autenticado mas sem permissão para a hierarquia selecionada
                    messagebox.showwarning('Permissao Negada!', f'Voce nao tem autorizaçao para acessar como {hierarquia_esperada}.')
            else:
                # Senha inválida
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            # Usuário não encontrado
            messagebox.showerror("Erro", "Usuário não encontrado.")

        cursor.close()
        conexao.close()

    except mysql.connector.Error as err:
        # Erro de conexão com o banco
        messagebox.showerror("Erro", f"Erro ao conectar ao banco:\n{err}")
        
# ---------- Tela de Início ---------
def tela_inicio():
    ctk.set_appearance_mode('dark')               # Define modo escuro no app
    inicio = ctk.CTk()                             # Janela inicial
    inicio.title('Bem-Vindo a VidaPlus')
    inicio.geometry('300x400')                     # Tamanho da janela
    inicio.resizable(False, False)                 # Não permite redimensionamento
    
    # Carrega a imagem do logo
    try:
        inicio.logo = ctk.CTkImage(dark_image=Image.open("vidaplusimagem.png"), size=(175, 175))
        label_imagem = ctk.CTkLabel(inicio, image=inicio.logo, text='')
        label_imagem.pack(pady=15)
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")     # Mostra erro no terminal se a imagem não carregar

    # Ações ao clicar nos botões
    def abrir_login_adm():
        inicio.destroy()
        tela_login(exibir_cadastro=True, hierarquia_esperada='Administrador')
    
    def abrir_login_medico():
        inicio.destroy()
        tela_login(exibir_cadastro=True, hierarquia_esperada='Medico')

    def abrir_login_paciente():
        inicio.destroy()
        tela_login(exibir_cadastro=False, hierarquia_esperada='Paciente')

    # Botões de acesso conforme o tipo de usuário
    ctk.CTkButton(inicio, text='Administrador(a)', command=abrir_login_adm).pack(pady=15)
    ctk.CTkButton(inicio, text='Medico(a)', command=abrir_login_medico).pack(pady=15)
    ctk.CTkButton(inicio, text='Paciente', command=abrir_login_paciente).pack(pady=15)

    inicio.mainloop()                              # Executa o loop principal da interface

# ---------- Tela de login ----------
def tela_login(exibir_cadastro=True, hierarquia_esperada='Paciente'):
    ctk.set_appearance_mode("dark")                # Modo escuro
    app = ctk.CTk()                                 # Janela de login
    app.title("VidaPlus - Login")
    app.geometry("300x350")                        # Tamanho da janela

    ctk.CTkLabel(app, text="Login VidaPlus", font=ctk.CTkFont(size=20)).pack(pady=20)

    entry_usuario = ctk.CTkEntry(app, placeholder_text="Usuário")  # Campo de usuário
    entry_usuario.pack(pady=10)

    entry_senha = ctk.CTkEntry(app, placeholder_text="Senha", show="*")  # Campo de senha
    entry_senha.pack(pady=10)
    
    # Função que chama a validação de login
    def realizar_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        if usuario and senha:
            validar_login(usuario, senha, app, hierarquia_esperada)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    ctk.CTkButton(app, text="Login", command=realizar_login).pack(pady=10)

    # Credenciais fixas para permitir acesso ao cadastro
    USUARIO_MESTRE = "admincadastro2025"
    SENHA_MESTRE = "cadastro2025"

    # Função que abre a tela de autenticação para cadastro
    def abrir_cadastro():
        popup = ctk.CTkToplevel(app)               # Janela sobreposta
        popup.attributes('-topmost', True)
        popup.lift()
        popup.focus_force()
        popup.title("Autenticação Requerida")
        popup.geometry("300x200")
        popup.resizable(False, False)

        # Campos de autenticação
        ctk.CTkLabel(popup, text="Usuário Mestre").pack(pady=(20, 5))
        entry_user = ctk.CTkEntry(popup)
        entry_user.pack()

        ctk.CTkLabel(popup, text="Senha Mestre").pack(pady=(10, 5))
        entry_pass = ctk.CTkEntry(popup, show="*")
        entry_pass.pack()

        # Validação de usuário mestre
        def autenticar():
            if entry_user.get() == USUARIO_MESTRE and entry_pass.get() == SENHA_MESTRE:
                popup.destroy()
                app.withdraw()  # Esconde a tela de login
                janela_cadastro = construir_tela_cadastro(app, hierarquia_esperada=hierarquia_esperada)
                janela_cadastro.protocol("WM_DELETE_WINDOW", lambda: [janela_cadastro.destroy(), app.deiconify()])
            else:
                messagebox.showerror("Erro", "Usuário ou senha mestre inválidos.")

        ctk.CTkButton(popup, text="Confirmar", command=autenticar).pack(pady=15)
        ctk.CTkButton(popup, text="Cancelar", command=popup.destroy).pack()

    # Botão para abrir cadastro, se permitido
    if exibir_cadastro:
        ctk.CTkButton(app, text="Cadastrar novo usuário", command=abrir_cadastro).pack(pady=5)
    
    # Botão para voltar à tela inicial
    ctk.CTkButton(app, text="Voltar", command=lambda: [app.destroy(), tela_inicio()]).pack(pady=10)

    app.mainloop()

# ---------- Tela de Cadastro ----------
def construir_tela_cadastro(janela_principal, hierarquia_esperada):
    cadastro = ctk.CTkToplevel(janela_principal)           # Nova janela sobreposta
    cadastro.title('Cadastro de Usuário')
    cadastro.geometry('500x550')
    cadastro.resizable(False, False)

    ctk.CTkLabel(cadastro, text="Cadastro de Usuário", font=ctk.CTkFont("Arial", 20)).pack(pady=10)

    frame_formulario = ctk.CTkFrame(cadastro)
    frame_formulario.pack(pady=10)

    # Campos do formulário de cadastro
    campos = [
        "Nome completo",
        "CPF",
        "Telefone",
        "Endereço",
        "Usuário",
        "Senha"
    ]

    entradas = []  # Lista que armazena os campos de entrada

    # Criação dos campos no formulário, 2 por linha
    for i in range(0, len(campos), 2):
        campo1 = ctk.CTkEntry(frame_formulario, placeholder_text=campos[i])
        campo1.grid(row=i//2, column=0, padx=10, pady=5, sticky="ew")
        entradas.append(campo1)

        if i + 1 < len(campos):
            campo2 = ctk.CTkEntry(frame_formulario, placeholder_text=campos[i+1], show="*" if campos[i+1] == "Senha" else "")
            campo2.grid(row=i//2, column=1, padx=10, pady=5, sticky="ew")
            entradas.append(campo2)

    # Configuração das colunas para redimensionamento
    frame_formulario.columnconfigure(0, weight=1)
    frame_formulario.columnconfigure(1, weight=1)

    # Título para seleção de hierarquia
    ctk.CTkLabel(cadastro, text="Selecione a hierarquia:", font=ctk.CTkFont(size=14)).pack(pady=(10, 0))
    hierarquia_var = ctk.StringVar(value="Paciente")
    frame_hierarquia = ctk.CTkFrame(cadastro)
    frame_hierarquia.pack(pady=5)
    
    # Botões para selecionar a hierarquia do novo usuário
    if hierarquia_esperada == 'Administrador':
        ctk.CTkRadioButton(frame_hierarquia, text="Administrador", variable=hierarquia_var, value="Administrador").pack(side="left", padx=20)
        ctk.CTkRadioButton(frame_hierarquia, text="Medico", variable=hierarquia_var, value="Medico").pack(side="left", padx=20)
        ctk.CTkRadioButton(frame_hierarquia, text="Paciente", variable=hierarquia_var, value="Paciente").pack(side="left", padx=20)
    else:
        ctk.CTkRadioButton(frame_hierarquia, text="Paciente", variable=hierarquia_var, value="Paciente").pack(side="left", padx=20)
    
    # Função para finalizar o cadastro de um novo usuário
    def finalizar_cadastro():
        # Obtém todos os valores digitados nos campos de entrada
        dados = [entrada.get().strip() for entrada in entradas]
        # Obtém a hierarquia selecionada (Administrador, Médico ou Paciente)
        hierarquia = hierarquia_var.get()
            
        # Verifica se todos os campos foram preenchidos
        if all(dados):
            # Criptografa a senha antes de armazenar no banco
            senha_cripto = bcrypt.hashpw(dados[5].encode('utf-8'), bcrypt.gensalt())
            # Substitui a senha original pela senha criptografada
            dados[5] = senha_cripto.decode('utf-8')
            # Insere os dados do usuário no banco de dados
            inserir_usuario_mysql(dados, hierarquia)
            # Fecha a janela de cadastro
            cadastro.destroy()
            # Restaura a janela principal (janela anterior)
            janela_principal.deiconify()
        else:
            # Exibe aviso caso haja campos vazios
            messagebox.showwarning("Campos vazios", "Preencha todos os campos.")

    # Botão para finalizar e salvar o cadastro
    ctk.CTkButton(cadastro, text="Finalizar Cadastro", command=finalizar_cadastro).pack(pady=20)

    # Botão para voltar à tela de login, destruindo a tela de cadastro atual
    ctk.CTkButton(cadastro, text="Voltar", command=lambda: [cadastro.destroy(), tela_login(exibir_cadastro=True, hierarquia_esperada=hierarquia_esperada)]).pack(pady=10)

    # Retorna a referência da tela de cadastro
    return cadastro


# ---------- Tela principal do Administrador ----------
def tela_principal_adm():
    # Cria a janela principal da interface do administrador
    telaAdm = ctk.CTk()
    telaAdm.title('SGHSS - Vida Plus - Administrador')
    telaAdm.geometry('800x500')
    telaAdm.resizable(True, True)

    # Cria o menu lateral (esquerdo)
    frame_menu = ctk.CTkFrame(telaAdm, width=200)
    frame_menu.pack(side='left', fill='y', padx=10, pady=10)

    # Cria o espaço onde os formulários e conteúdo principal serão exibidos
    frame_conteudo = ctk.CTkFrame(telaAdm)
    frame_conteudo.pack(side='right', expand=True, fill='both', padx=10, pady=10)

    # Função para limpar o conteúdo atual do frame principal
    def limpar_conteudo():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    # ---------- Formulário de atualização de médicos ----------
    def mostrar_formulario_medico():
        limpar_conteudo()

        # Título do formulário
        ctk.CTkLabel(frame_conteudo, text="Atualizar Cadastro Médico", font=ctk.CTkFont(size=18)).pack(pady=10)

        # Tenta buscar os médicos cadastrados no banco
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='890866',
                database='vidaplus'
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT usuario FROM usuarios WHERE hierarquia = 'Medico'")
            medicos = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            # Mostra erro se não conseguir conectar ao banco
            messagebox.showerror("Erro", f"Erro ao buscar médicos:\n{err}")
            return

        # Se nenhum médico for encontrado, avisa o usuário
        if not medicos:
            messagebox.showinfo("Aviso", "Nenhum médico encontrado.")
            return

        # Variável que armazena o médico atualmente selecionado
        medico_selecionado = ctk.StringVar(value=medicos[0])

        # Função que carrega os dados do médico selecionado no menu
        def carregar_dados_medico(*_):
            usuario = medico_selecionado.get()
            try:
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='890866',
                    database='vidaplus'
                )
                cursor = conexao.cursor()
                cursor.execute("""
                    SELECT nome_completo, cpf, telefone, endereco, usuario 
                    FROM usuarios WHERE usuario = %s
                """, (usuario,))
                resultado = cursor.fetchone()
                cursor.close()
                conexao.close()

                if resultado:
                    # Preenche os campos com os dados recuperados do banco
                    for entrada, valor in zip(entradas, resultado):
                        entrada.delete(0, tk.END)
                        entrada.insert(0, valor)
                else:
                    messagebox.showwarning("Atenção", "Médico não encontrado.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao carregar dados:\n{err}")

        # Frame para seleção de médicos
        menu_frame = ctk.CTkFrame(frame_conteudo)
        menu_frame.pack(pady=5)
        ctk.CTkLabel(menu_frame, text="Selecionar Médico:").pack(side='left', padx=(0, 10))
        ctk.CTkOptionMenu(menu_frame, variable=medico_selecionado, values=medicos, command=carregar_dados_medico).pack(side='left')

        # Lista de campos que serão exibidos no formulário
        campos = ["Nome completo", "CPF", "Telefone", "Endereço", "Usuário", "Senha"]
        entradas = []

        # Frame que contém os campos de entrada
        frame_form = ctk.CTkFrame(frame_conteudo)
        frame_form.pack(pady=10)

        # Cria os campos de entrada de dois em dois (duas colunas)
        for i in range(0, len(campos), 2):
            campo1 = ctk.CTkEntry(frame_form, placeholder_text=campos[i])
            campo1.grid(row=i//2, column=0, padx=10, pady=5, sticky="ew")
            entradas.append(campo1)

            if i + 1 < len(campos):
                campo2 = ctk.CTkEntry(frame_form, placeholder_text=campos[i+1], show="*" if campos[i+1] == "Senha" else "")
                campo2.grid(row=i//2, column=1, padx=10, pady=5, sticky="ew")
                entradas.append(campo2)

        # Permite que as colunas se expandam proporcionalmente
        frame_form.columnconfigure(0, weight=1)
        frame_form.columnconfigure(1, weight=1)

        # Carrega os dados do primeiro médico automaticamente
        carregar_dados_medico()

        # Função para salvar os dados editados no banco de dados
        def salvar_medico():
            dados = [entrada.get().strip() for entrada in entradas]
            if all(dados):
                senha_cripto = bcrypt.hashpw(dados[5].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                dados[5] = senha_cripto.decode('utf-8')
                try:
                    conexao = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='890866',
                        database='vidaplus'
                    )
                    cursor = conexao.cursor()
                    query = """
                        UPDATE usuarios SET 
                            nome_completo=%s, cpf=%s, telefone=%s, endereco=%s, usuario=%s, senha=%s
                        WHERE usuario = %s AND hierarquia = 'Medico'
                    """
                    # Executa o update com os dados fornecidos
                    cursor.execute(query, (*dados, medico_selecionado.get()))
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    messagebox.showinfo("Sucesso", "Cadastro do médico atualizado com sucesso.")
                    limpar_conteudo()
                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao atualizar:\n{err}")
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        # Botão para salvar as alterações no cadastro
        ctk.CTkButton(frame_conteudo, text="Salvar", command=salvar_medico).pack(pady=10)


    # ---------- Formulário de atualização de pacientes ----------
    def mostrar_formulario_paciente():
        limpar_conteudo()

        # Título do formulário
        ctk.CTkLabel(frame_conteudo, text="Atualizar Cadastro Paciente", font=ctk.CTkFont(size=18)).pack(pady=10)

        try:
            # Busca usuários com hierarquia de paciente
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='890866',
                database='vidaplus'
            )
            cursor = conexao.cursor()
            cursor.execute("SELECT usuario FROM usuarios WHERE hierarquia = 'Paciente'")
            pacientes = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar pacientes:\n{err}")
            return

        # Exibe aviso se não houver pacientes
        if not pacientes:
            messagebox.showinfo("Aviso", "Nenhum paciente encontrado.")
            return

        # Armazena o paciente selecionado
        paciente_selecionado = ctk.StringVar(value=pacientes[0])

        # Função que carrega os dados de um paciente selecionado no menu
        def carregar_dados_paciente(*_):
            usuario = paciente_selecionado.get()  # Obtém o usuário selecionado
            try:
                # Conecta ao banco de dados
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='890866',
                    database='vidaplus'
                )
                cursor = conexao.cursor()
                # Executa a consulta para buscar os dados do paciente
                cursor.execute("""
                    SELECT nome_completo, cpf, telefone, endereco, usuario 
                    FROM usuarios WHERE usuario = %s
                """, (usuario,))
                resultado = cursor.fetchone()
                cursor.close()
                conexao.close()

                if resultado:
                    # Preenche os campos com os dados do paciente
                    for entrada, valor in zip(entradas, resultado):
                        entrada.delete(0, tk.END)
                        entrada.insert(0, valor)
                else:
                    # Exibe alerta se o paciente não for encontrado
                    messagebox.showwarning("Atenção", "Paciente não encontrado.")
            except mysql.connector.Error as err:
                # Exibe erro caso a consulta falhe
                messagebox.showerror("Erro", f"Erro ao carregar dados:\n{err}")

            # Frame do menu com o dropdown de pacientes
            menu_frame = ctk.CTkFrame(frame_conteudo)
            menu_frame.pack(pady=5)
            ctk.CTkLabel(menu_frame, text="Selecionar Paciente:").pack(side='left', padx=(0, 10))
            # Menu suspenso para selecionar o paciente
            ctk.CTkOptionMenu(menu_frame, variable=paciente_selecionado, values=pacientes, command=carregar_dados_paciente).pack(side='left')

        # Lista de campos que serão preenchidos
        campos = ["Nome completo", "CPF", "Telefone", "Endereço", "Usuário", "Senha"]
        entradas = []

        # Frame do formulário
        frame_form = ctk.CTkFrame(frame_conteudo)
        frame_form.pack(pady=10)

        # Cria os campos de entrada de dois em dois (colunas)
        for i in range(0, len(campos), 2):
            campo1 = ctk.CTkEntry(frame_form, placeholder_text=campos[i])
            campo1.grid(row=i//2, column=0, padx=10, pady=5, sticky="ew")
            entradas.append(campo1)

            if i + 1 < len(campos):
                campo2 = ctk.CTkEntry(frame_form, placeholder_text=campos[i+1], show="*" if campos[i+1] == "Senha" else "")
                campo2.grid(row=i//2, column=1, padx=10, pady=5, sticky="ew")
                entradas.append(campo2)

        # Permite que as colunas se expandam
        frame_form.columnconfigure(0, weight=1)
        frame_form.columnconfigure(1, weight=1)

        # Carrega automaticamente os dados do primeiro paciente listado
        carregar_dados_paciente()

        # Função para salvar as alterações nos dados do paciente
        def salvar_paciente():
            dados = [entrada.get().strip() for entrada in entradas]
            if all(dados):
                # Criptografa a senha antes de salvar no banco
                senha_cripto = bcrypt.hashpw(dados[5].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                dados[5] = senha_cripto.decode('utf-8')
                try:
                    conexao = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='890866',
                        database='vidaplus'
                    )
                    cursor = conexao.cursor()
                    # Query para atualizar os dados do paciente
                    query = """
                        UPDATE usuarios SET 
                            nome_completo=%s, cpf=%s, telefone=%s, endereco=%s, usuario=%s, senha=%s
                        WHERE usuario = %s AND hierarquia = 'Paciente'
                    """
                    cursor.execute(query, (*dados, paciente_selecionado.get()))
                    conexao.commit()
                    cursor.close()
                    conexao.close()
                    # Exibe mensagem de sucesso
                    messagebox.showinfo("Sucesso", "Cadastro do paciente atualizado com sucesso.")
                    limpar_conteudo()
                except mysql.connector.Error as err:
                    # Exibe mensagem de erro
                    messagebox.showerror("Erro", f"Erro ao atualizar:\n{err}")
            else:
                # Alerta se houver campos vazios
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        # Botão para salvar alterações do paciente
        ctk.CTkButton(frame_conteudo, text="Salvar", command=salvar_paciente).pack(pady=10)


# ---------------- Botões do Menu Lateral ----------------
    botoes = {
        'Atualizar Cadastro Médico': mostrar_formulario_medico,
        'Atualizar Cadastro Paciente': mostrar_formulario_paciente,
        'Visualizar Histórico Clínico': lambda: print("Em construção"),
        'Verificar Consultas Pacientes': lambda: print("Em construção"),
        'Gerenciar Cadastro Administrador': lambda: print("Em construção"),
        'Logout': lambda: [telaAdm.destroy(), tela_login()]
    }

    # Cria cada botão do menu com sua respectiva ação
    for texto, comando in botoes.items():
        ctk.CTkButton(frame_menu, text=texto, command=comando).pack(pady=10, fill='x')

    # Inicia a interface principal do administrador
    telaAdm.mainloop()


# ---------- Tela principal para Médicos ----------
def tela_principal_medico():
    # Cria a janela do médico
    telaMed = ctk.CTk()
    telaMed.title('SGHSS - Vida Plus - Médico')
    telaMed.geometry('800x500')
    telaMed.resizable(True, True)

    # Frame lateral do menu
    frame_menu = ctk.CTkFrame(telaMed, width=200)
    frame_menu.pack(side='left', fill='y', padx=10, pady=10)

    # Frame do conteúdo principal
    frame_conteudo = ctk.CTkFrame(telaMed)
    frame_conteudo.pack(side='right', expand=True, fill='both', padx=10, pady=10)

    # Função para limpar os elementos do frame de conteúdo
    def limpar_conteudo():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    # Função para exibir formulário de atualização do próprio cadastro
    def mostrar_formulario_medico():
        limpar_conteudo()

        # Título do formulário
        ctk.CTkLabel(frame_conteudo, text="Atualizar Cadastro", font=ctk.CTkFont(size=18)).pack(pady=10)

        campos = [
            "Nome completo",
            "CPF",
            "Telefone",
            "Endereço",
            "Usuário",
            "Senha"
        ]
        entradas = []

        # Frame do formulário
        frame_form = ctk.CTkFrame(frame_conteudo)
        frame_form.pack(pady=10)

        # Cria os campos de entrada (2 por linha)
        for i in range(0, len(campos), 2):
            campo1 = ctk.CTkEntry(frame_form, placeholder_text=campos[i])
            campo1.grid(row=i//2, column=0, padx=10, pady=5, sticky="ew")
            entradas.append(campo1)

            if i + 1 < len(campos):
                campo2 = ctk.CTkEntry(frame_form, placeholder_text=campos[i+1], show="*" if campos[i+1] == "Senha" else "")
                campo2.grid(row=i//2, column=1, padx=10, pady=5, sticky="ew")
                entradas.append(campo2)

        frame_form.columnconfigure(0, weight=1)
        frame_form.columnconfigure(1, weight=1)

        # Função para salvar os dados do médico no banco
        def salvar():
            dados = [entrada.get().strip() for entrada in entradas]
            if all(dados):
                senha_cripto = bcrypt.hashpw(dados[5].encode('utf-8'), bcrypt.gensalt())
                dados[5] = senha_cripto.decode('utf-8')
                inserir_usuario_mysql(dados, 'Medico')
                messagebox.showinfo("Sucesso", "Cadastro atualizado com sucesso.")
                limpar_conteudo()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        # Botão de salvar alterações
        ctk.CTkButton(frame_conteudo, text="Salvar", command=salvar).pack(pady=10)
    # Dicionário com os botões do menu lateral da interface do médico
    botoes = {
        'Verificar Agendamentos': lambda: print("Verificar..."),
        'Emitir Receita': lambda: print("Emitir..."),
        'Gerenciar Pacientes': lambda: print("Gerenciar..."),
        'Telemedicina - Atender': lambda: print("Atender..."),
        'Atualização Cadastral': mostrar_formulario_medico  # Exibe o formulário para editar dados
    }

    # Criação dos botões no menu lateral com os textos e comandos definidos acima
    for texto, comando in botoes.items():
        ctk.CTkButton(frame_menu, text=texto, command=comando).pack(pady=10, fill='x')

    # Botão para logout (fecha a tela atual e retorna para o login)
    ctk.CTkButton(frame_menu, text="Logout", command=lambda: [telaMed.destroy(), tela_login()]).pack(pady=10, fill='x')

    # Inicia o loop principal da interface do médico
    telaMed.mainloop()


# ---------- Tela principal do paciente ----------
def tela_principal_paciente():
    # Cria a janela principal para o paciente
    telaPac = ctk.CTk()
    telaPac.title('SGHSS - Vida Plus - Paciente')
    telaPac.geometry('800x500')
    telaPac.resizable(True, True)

    # Frame lateral do menu
    frame_menu = ctk.CTkFrame(telaPac, width=200)
    frame_menu.pack(side='left', fill='y', padx=10, pady=10)

    # Frame do conteúdo principal
    frame_conteudo = ctk.CTkFrame(telaPac)
    frame_conteudo.pack(side='right', expand=True, fill='both', padx=10, pady=10)

    # Função que limpa os widgets do frame de conteúdo
    def limpar_conteudo():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    # Função para exibir formulário de atualização de dados cadastrais
    def mostrar_formulario_paciente():
        limpar_conteudo()

        ctk.CTkLabel(frame_conteudo, text="Atualizar Cadastro", font=ctk.CTkFont(size=18)).pack(pady=10)

        campos = [
            "Nome completo",
            "CPF",
            "Telefone",
            "Endereço",
            "Usuário",
            "Senha"
        ]
        entradas = []

        # Frame do formulário
        frame_form = ctk.CTkFrame(frame_conteudo)
        frame_form.pack(pady=10)

        # Cria os campos de entrada (em pares lado a lado)
        for i in range(0, len(campos), 2):
            campo1 = ctk.CTkEntry(frame_form, placeholder_text=campos[i])
            campo1.grid(row=i//2, column=0, padx=10, pady=5, sticky="ew")
            entradas.append(campo1)

            if i + 1 < len(campos):
                campo2 = ctk.CTkEntry(frame_form, placeholder_text=campos[i+1], show="*" if campos[i+1] == "Senha" else "")
                campo2.grid(row=i//2, column=1, padx=10, pady=5, sticky="ew")
                entradas.append(campo2)

        frame_form.columnconfigure(0, weight=1)
        frame_form.columnconfigure(1, weight=1)

        # Função que salva os dados atualizados no banco
        def salvar():
            dados = [entrada.get().strip() for entrada in entradas]
            if all(dados):
                # Criptografa a senha antes de salvar
                senha_cripto = bcrypt.hashpw(dados[5].encode('utf-8'), bcrypt.gensalt())
                dados[5] = senha_cripto.decode('utf-8')
                inserir_usuario_mysql(dados, 'Paciente')
                messagebox.showinfo("Sucesso", "Cadastro atualizado com sucesso.")
                limpar_conteudo()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        # Botão para salvar os dados
        ctk.CTkButton(frame_conteudo, text="Salvar", command=salvar).pack(pady=10)

    def agendar_consulta_paciente():
        # Limpa o conteúdo atual da interface para exibir o novo formulário
        limpar_conteudo()

        # Título da seção de agendamento
        ctk.CTkLabel(frame_conteudo, text="Agendar Consulta", font=ctk.CTkFont(size=18)).pack(pady=10)

        # Tenta conectar ao banco de dados e buscar médicos disponíveis
        try:
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='890866',
                database='vidaplus'
            )
            cursor = conexao.cursor()
            # Consulta todos os usuários com hierarquia 'Medico'
            cursor.execute("SELECT usuario FROM usuarios WHERE hierarquia = 'Medico'")
            medicos = [row[0] for row in cursor.fetchall()]  # Extrai apenas os nomes de usuário
            cursor.close()
            conexao.close()
        except mysql.connector.Error as err:
            # Em caso de erro na conexão ou consulta, exibe mensagem de erro
            messagebox.showerror("Erro", f"Erro ao carregar médicos:\n{err}")
            return

        # Se não houver médicos cadastrados, informa ao usuário
        if not medicos:
            messagebox.showinfo("Aviso", "Nenhum médico disponível.")
            return

        # Variáveis para armazenar os dados do formulário
        medico_var = ctk.StringVar(value=medicos[0])
        data_var = ctk.StringVar()
        hora_var = ctk.StringVar()
        observacoes_var = ctk.StringVar()

        # Campo: Seleção do médico
        ctk.CTkLabel(frame_conteudo, text="Selecionar Médico:").pack()
        ctk.CTkOptionMenu(frame_conteudo, values=medicos, variable=medico_var).pack(pady=5)

        # Campo: Data da consulta
        ctk.CTkLabel(frame_conteudo, text="Data (YYYY-MM-DD):").pack()
        ctk.CTkEntry(frame_conteudo, textvariable=data_var).pack(pady=5)

        # Campo: Hora da consulta
        ctk.CTkLabel(frame_conteudo, text="Hora (HH:MM):").pack()
        ctk.CTkEntry(frame_conteudo, textvariable=hora_var).pack(pady=5)

        # Campo: Observações adicionais
        ctk.CTkLabel(frame_conteudo, text="Observações:").pack()
        ctk.CTkEntry(frame_conteudo, textvariable=observacoes_var).pack(pady=5)

        # Função interna para salvar o agendamento no banco de dados
        def salvar_agendamento():
            try:
                # Conecta ao banco novamente para inserir o novo agendamento
                conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='890866',
                    database='vidaplus'
                )
                cursor = conexao.cursor()

                # Comando SQL de inserção
                query = """
                INSERT INTO agendamentos (paciente_usuario, medico_usuario, data_consulta, hora_consulta, observacoes)
                VALUES (%s, %s, %s, %s, %s)
                """
                #Criaçao de uma variável para o usuario logado
                usuario_logado = None
                
                cursor.execute(query, (
                    usuario_logado,  # <- IMPORTANTE: esta variável deve conter o login do paciente logado
                    medico_var.get(),         # Médico selecionado
                    data_var.get(),           # Data inserida
                    hora_var.get(),           # Hora inserida
                    observacoes_var.get()     # Observações da consulta
                ))
                conexao.commit()  # Confirma a inserção no banco
                cursor.close()
                conexao.close()
                
                # Mensagem de sucesso
                messagebox.showinfo("Sucesso", "Consulta agendada com sucesso.")
                limpar_conteudo()  # Limpa a tela após agendar
            except mysql.connector.Error as err:
                # Exibe erro se houver falha ao salvar
                messagebox.showerror("Erro", f"Erro ao agendar consulta:\n{err}")

        # Botão para confirmar agendamento
        ctk.CTkButton(frame_conteudo, text="Agendar", command=salvar_agendamento).pack(pady=10)

    def consultar_agendamentos_paciente():
        limpar_conteudo()  # Limpa o conteúdo anterior da tela

        ctk.CTkLabel(frame_conteudo, text="Consultas Agendadas", font=ctk.CTkFont(size=18)).pack(pady=10)

        try:
            # Conectar ao banco de dados
            conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                password='890866',
                database='vidaplus'
            )
            cursor = conexao.cursor()

            # Buscar consultas do paciente logado
            query = """
                SELECT medico_usuario, data_consulta, hora_consulta, observacoes
                FROM agendamentos
                WHERE paciente_usuario = %s
                ORDER BY data_consulta, hora_consulta
            """
            cursor.execute(query, (usuario_logado,))
            resultados = cursor.fetchall()

            cursor.close()
            conexao.close()

            if not resultados:
                messagebox.showinfo("Aviso", "Nenhuma consulta agendada encontrada.")
                return

            # Criar uma textbox para exibir os agendamentos
            texto_resultado = ctk.CTkTextbox(frame_conteudo, height=300, width=600)
            texto_resultado.pack(pady=10)

            for medico, data, hora, obs in resultados:
                texto_resultado.insert(tk.END, f"Médico: {medico}\nData: {data}\nHora: {hora}\nObservações: {obs}\n\n")

            texto_resultado.configure(state="disabled")  # Desativa edição

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao consultar agendamentos:\n{err}")

    # Dicionário com os botões da interface do paciente
    botoes = {
        'Agendar Consulta': agendar_consulta_paciente,
        'Consultar Agendamento': consultar_agendamentos_paciente,
        'Visualizar Histórico Clínico': lambda: print("Histórico..."),
        'Telemedicina - Consulta Online': lambda: print("Telemedicina..."),
        'Atualização Cadastral': mostrar_formulario_paciente  # Exibe o formulário de atualização
    }

    # Cria os botões de menu com suas respectivas ações
    for texto, comando in botoes.items():
        ctk.CTkButton(frame_menu, text=texto, command=comando).pack(pady=10, fill='x')

    # Botão de logout
    def logout():
        global usuario_logado
        usuario_logado = None
        tela_login()

    ctk.CTkButton(frame_menu, text="Logout", command=lambda: [telaPac.destroy(), logout()]).pack(pady=10, fill='x')

    # Inicia o loop principal da interface do paciente
    telaPac.mainloop()

# ---------- Função para inserir um novo usuário no banco de dados ----------
def inserir_usuario_mysql(dados, hierarquia):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='890866',  # Substituir por senha segura em produção
            database='vidaplus'
        )
        cursor = conexao.cursor()

        # Query para inserir novo usuário
        query = """
        INSERT INTO usuarios (
            nome_completo, cpf, telefone, endereco, usuario, senha, hierarquia
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (*dados, hierarquia))
        conexao.commit()

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

        cursor.close()
        conexao.close()

    except mysql.connector.Error as err:
        # Mensagem de erro, caso ocorra alguma falha
        messagebox.showerror("Erro", f"Erro ao cadastrar usuário:\n{err}")


# ---------- Início do sistema ----------
tela_inicio()  # Chamada inicial para exibir a primeira tela do sistema

