import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        banco = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="database"
        )
        return banco
    except mysql.connector.Error as err:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
        return None

# Funções do sistema
def inserir_aluno():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    cpf = entry_cpf.get()
    RG = entry_RG.get()
    endereco = entry_endereco.get()
    ncartrab = entry_ncartrab.get()

    if not nome or not telefone or not email:
        messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos!")
        return

    try:
        banco = conectar_banco()
        if banco:
            cursor = banco.cursor()
            sql = ("INSERT INTO alunos (nome, telefone, email, cpf, RG, endereco, ncartrab, salario, horario_trabalho, data_exame_aso) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data = (nome, telefone, email, cpf, RG, endereco, ncartrab, salario, horario_trabalho, data_exame_aso)
            cursor.execute(sql, data)
            banco.commit()
            cursor.close()
            banco.close()
            messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
            limpar_campos()
            listar_alunos()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao adicionar funcionário: {err}")

def listar_alunos():
    try:
        banco = conectar_banco()
        if banco:
            cursor = banco.cursor()
            cursor.execute("SELECT * FROM alunos")
            alunos = cursor.fetchall()
            cursor.close()
            banco.close()

            listbox_alunos.delete(0, tk.END)
            for aluno in alunos:
                listbox_alunos.insert(tk.END, f"{aluno[0]} - {aluno[1]}")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao listar alunos: {err}")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_RG.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_ncartrab.delete(0, tk.END)

def deletar_aluno():
    selecionado = listbox_alunos.get(tk.ACTIVE)
    if not selecionado:
        messagebox.showwarning("Seleção vazia", "Por favor, selecione um funcionário para deletar!")
        return

    id_aluno = selecionado.split(" - ")[0]
    try:
        banco = conectar_banco()
        if banco:
            cursor = banco.cursor()
            sql = "DELETE FROM alunos WHERE id = %s"
            cursor.execute(sql, (id_aluno,))
            banco.commit()
            cursor.close()
            banco.close()
            messagebox.showinfo("Sucesso", "Funcionário deletado com sucesso!")
            listar_alunos()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao deletar funcionário: {err}")

def abrir_informacoes():
    selecionado = listbox_alunos.get(tk.ACTIVE)
    if not selecionado:
        messagebox.showwarning("Seleção vazia", "Por favor, selecione um funcionário para abrir!")
        return

    id_aluno = selecionado.split(" - ")[0]
    try:
        banco = conectar_banco()
        if banco:
            cursor = banco.cursor()
            sql = "SELECT * FROM alunos WHERE id = %s"
            cursor.execute(sql, (id_aluno,))
            aluno = cursor.fetchone()
            cursor.close()
            banco.close()

            if aluno:
                limpar_campos()
                entry_nome.insert(0, aluno[1])
                entry_telefone.insert(0, aluno[2])
                entry_email.insert(0, aluno[3])
                entry_cpf.insert(0, aluno[4])
                entry_RG.insert(0, aluno[5])
                entry_endereco.insert(0, aluno[6])
                entry_ncartrab.insert(0, aluno[7])
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao abrir informações: {err}")

# Configuração da interface Tkinter
root = tk.Tk()
root.title("Cadastro de Funcionários")
root.geometry("600x700")

# Configuração de estilos
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 12))
style.configure("TFrame", background="#f0f0f0")

# Frame para entrada de dados
frame_entrada = ttk.Frame(root, padding=10)
frame_entrada.pack(pady=10, fill=tk.X)

def criar_label_entry(parent, texto, row):
    label = ttk.Label(parent, text=texto)
    label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
    entry = ttk.Entry(parent)
    entry.grid(row=row, column=1, padx=5, pady=5, sticky=tk.EW)
    return entry

entry_nome = criar_label_entry(frame_entrada, "Nome:", 0)
entry_telefone = criar_label_entry(frame_entrada, "Telefone:", 1)
entry_email = criar_label_entry(frame_entrada, "Email:", 2)
entry_cpf = criar_label_entry(frame_entrada, "CPF:", 3)
entry_RG = criar_label_entry(frame_entrada, "RG:", 4)
entry_endereco = criar_label_entry(frame_entrada, "Endereço:", 5)
entry_ncartrab = criar_label_entry(frame_entrada, "N° Carteira de Trabalho:", 6)

# Botões principais
frame_botoes = ttk.Frame(root, padding=10)
frame_botoes.pack(fill=tk.X)

btn_inserir = ttk.Button(frame_botoes, text="Inserir Funcionário", command=inserir_aluno)
btn_inserir.pack(side=tk.LEFT, padx=5, pady=5)

btn_deletar = ttk.Button(frame_botoes, text="Deletar Funcionário", command=deletar_aluno)
btn_deletar.pack(side=tk.LEFT, padx=5, pady=5)

btn_abrir = ttk.Button(frame_botoes, text="Abrir Informações", command=abrir_informacoes)
btn_abrir.pack(side=tk.LEFT, padx=5, pady=5)

btn_atualizar = ttk.Button(frame_botoes, text="Atualizar Lista", command=listar_alunos)
btn_atualizar.pack(side=tk.LEFT, padx=5, pady=5)

# Listbox para exibir os funcionários
frame_listbox = ttk.Frame(root, padding=10)
frame_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

label_lista = ttk.Label(frame_listbox, text="Funcionários Cadastrados:")
label_lista.pack(anchor=tk.W)

listbox_alunos = tk.Listbox(frame_listbox, font=("Arial", 12), height=15)
listbox_alunos.pack(fill=tk.BOTH, expand=True)

# Inicia a lista de funcionários
listar_alunos()

# Inicia a interface
root.mainloop()