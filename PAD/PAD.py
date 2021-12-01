import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *



class Notepad:
    __root = Tk()

    # Tamanho padrão da janela
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # Barra de rolagem lateral
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self, **kwargs):

        # Ícone
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass

        # Tamanho da janela (O padrão é 300x300 conforme comando anterior)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Título da janela
        self.__root.title("Sem título - nhenhePAD")

        # Centraliza a janela
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # Alinhar a esquerda
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # Alinhar a direita
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # Em cima e embaixo
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        # Ajusta automaticamente o texto
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Adiciona o widget de controles
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # Função novo arquivo (Novo)
        self.__thisFileMenu.add_command(label="Novo",
                                        command=self.__newFile)

        # Função abrir (Abrir)
        self.__thisFileMenu.add_command(label="Abrir",
                                        command=self.__openFile)

        # Função salvar
        self.__thisFileMenu.add_command(label="Salvar",
                                        command=self.__saveFile)

        # Para criar uma linha no menu entre Fechar e o resto do Menu Arquivo
        self.__thisFileMenu.add_separator()


        self.__thisFileMenu.add_command(label="Fechar",
                                        command=self.__quitApplication)
        #Menu Arquivo
        self.__thisMenuBar.add_cascade(label="Arquivo",
                                       menu=self.__thisFileMenu)

        # Função Cortar
        self.__thisEditMenu.add_command(label="Cortar",
                                        command=self.__cut)

        # Função Copiar
        self.__thisEditMenu.add_command(label="Copiar",
                                        command=self.__copy)

        # Função Colar
        self.__thisEditMenu.add_command(label="Colar",
                                        command=self.__paste)

        # Menu Editar
        self.__thisMenuBar.add_cascade(label="Editar",
                                       menu=self.__thisEditMenu)

        # Aparece a descrição do bloco de notas
        self.__thisHelpMenu.add_command(label="Sobre",
                                        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Ajuda",
                                       menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar se ajusta automaticamente de acordo com o conteúdo
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()
        # exit()

    def __showAbout(self):
        showinfo("nhenhePAD", "Esse é um bloco de notas feito pelo nhenhe")

    def __openFile(self):

        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisTextArea.insert(1.0, file.read())

            file.close()

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")])

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")


        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):

        # Executa a aplicação principal
        self.__root.mainloop()


# Executa a aplicação principal
notepad = Notepad(width=600, height=400)
notepad.run()