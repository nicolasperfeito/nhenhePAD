import re
import sqlite3
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox


class ConectarDB:
    def __init__(self):
        self.con = sqlite3.connect('db.sqlite3')
        self.cur = self.con.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS assist (
                nome TEXT,
                cpf TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                necessidade TEXT)''')
        except Exception as e:
            print('[x] Falha ao criar tabela: %s [x]' % e)
        else:
            print('\n[!] Tabela criada com sucesso [!]\n')

    def inserir_registro(self, nome, cpf, telefone, email, endereco, necessidade):
        try:
            self.cur.execute(
                '''INSERT INTO assist VALUES (?, ?, ?, ?, ?, ?)''', (nome, cpf, telefone, email, endereco, necessidade,))
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro inserido com sucesso [!]\n')

    def consultar_registros(self):
        return self.cur.execute('SELECT rowid, * FROM assist').fetchall()

    def consultar_ultimo_rowid(self):
        return self.cur.execute('SELECT MAX(rowid) FROM assist').fetchone()

    def remover_registro(self, rowid):
        try:
            self.cur.execute("DELETE FROM assist WHERE rowid=?", (rowid,))
        except Exception as e:
            print('\n[x] Falha ao remover registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro removido com sucesso [!]\n')


class Janela(tk.Frame):
    """Janela principal"""

    def __init__(self, master=None):
        """Construtor"""
        super().__init__(master)
        # Coletando informações do monitor
        largura = round(self.winfo_screenwidth() / 2)
        altura = round(self.winfo_screenheight() / 3)
        tamanho = ('%sx%s' % (largura, altura))

        # Título da janela principal.
        master.title('CRUD HOW-IV')

        # Tamanho da janela principal (definido em comando anterior).
        master.geometry(tamanho)

        # Instanciando a conexão com o banco.
        self.banco = ConectarDB()

        # Gerenciador de layout da janela principal.
        self.pack()

        # Criando os widgets da interface.
        self.criar_widgets()

    def criar_widgets(self):
        # Containers.
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=3, pady=3)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=3)

        # Labels > nome, cpf, telefone, email, endereco, necessidade
        label_documento = tk.Label(frame1, text='Nome', width=20)
        label_documento.grid(row=0, column=0)

        label_assunto = tk.Label(frame1, text='CPF', width=20)
        label_assunto.grid(row=0, column=1)

        label_recebido = tk.Label(frame1, text='Telefone', width=20)
        label_recebido.grid(row=0, column=2)

        label_recebido = tk.Label(frame1, text='E-mail', width=20)
        label_recebido.grid(row=0, column=3)

        label_recebido = tk.Label(frame1, text='Endereço', width=20)
        label_recebido.grid(row=0, column=4)

        label_recebido = tk.Label(frame1, text='Necessidade', width=20)
        label_recebido.grid(row=0, column=5)

        # Entrada de texto.
        self.entry_nome = tk.Entry(frame1)
        self.entry_nome.grid(row=1, column=0)

        self.entry_cpf = tk.Entry(frame1)
        self.entry_cpf.grid(row=1, column=1)

        self.entry_telefone = tk.Entry(frame1)
        self.entry_telefone.grid(row=1, column=2)

        self.entry_email = tk.Entry(frame1)
        self.entry_email.grid(row=1, column=3)

        self.entry_endereco = tk.Entry(frame1)
        self.entry_endereco.grid(row=1, column=4)

        self.entry_necessidade = tk.Entry(frame1)
        self.entry_necessidade.grid(row=1, column=5)

        # Botão para adicionar um novo registro.
        button_adicionar = tk.Button(frame1, text='Adicionar', bg='blue', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_adicionar['command'] = self.adicionar_registro
        button_adicionar.grid(row=0, column=6, rowspan=2, padx=15)

        # Treeview.
        # nome, cpf, telefone, email, endereco, necessidade
        self.treeview = tkk.Treeview(frame2, columns=('Nome', 'CPF', 'Telefone', 'E-mail', 'Endereço', 'Necessidade'))
        self.treeview.heading('#0', text='ID')
        self.treeview.heading('#1', text='Nome')
        self.treeview.heading('#2', text='CPF')
        self.treeview.heading('#3', text='E-mail')
        self.treeview.heading('#4', text='Telefone')
        self.treeview.heading('#5', text='Endereço')
        self.treeview.heading('#6', text='Necessidade')

        #Ajustar tamanho das colunas
        self.treeview.column(0, width=100)
        self.treeview.column(1, width=100)
        self.treeview.column(2, width=100)
        self.treeview.column(3, width=100)
        self.treeview.column(4, width=100)
        self.treeview.column(5, width=100)

        # Inserindo os dados do banco no treeview.
        for row in self.banco.consultar_registros():
            self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6]))

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Botão para remover um item.
        button_excluir = tk.Button(frame3, text='Excluir', bg='red', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_excluir['command'] = self.excluir_registro
        button_excluir.pack(pady=10)

    def adicionar_registro(self):
        # Coletando os valores.
        nome=self.entry_nome.get()
        cpf=self.entry_cpf.get()
        telefone=self.entry_telefone.get()
        email=self.entry_email.get()
        endereco=self.entry_endereco.get()
        necessidade=self.entry_necessidade.get()

    def excluir_registro(self):
        # Verificando se algum item está selecionado.
        if not self.treeview.focus():
            messagebox.showerror('Erro', 'Nenhum item selecionado')
        else:
            # Coletando qual item está selecionado.
            item_selecionado = self.treeview.focus()

            # Coletando os dados do item selecionado (dicionário).
            rowid = self.treeview.item(item_selecionado)

            # Removendo o item com base no valor do rowid (argumento text do treeview).
            # Removendo valor da tabela.
            self.banco.remover_registro(rowid['text'])

            # Removendo valor do treeview.
            self.treeview.delete(item_selecionado)


root = tk.Tk()
app = Janela(master=root)
app.mainloop()