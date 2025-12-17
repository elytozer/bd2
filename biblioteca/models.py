import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent
from persistent.list import PersistentList

class Livro(Persistent):
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.status = "Disponível"
        self.emprestado_para = None

class Usuario(Persistent):
    def __init__(self, nome):
        self.nome = nome
        self.livros_locados = PersistentList() # Lista especial do ZODB para persistência

class Biblioteca:
    def __init__(self, db_path="biblioteca.fs"):
        self.storage = ZODB.FileStorage.FileStorage(db_path)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        # Inicializa dicionários se não existirem
        if 'livros' not in self.root:
            self.root['livros'] = {}
        if 'usuarios' not in self.root:
            self.root['usuarios'] = {}
        transaction.commit()

    def cadastrar_livro(self, titulo, autor):
        titulo_chave = titulo.strip().lower()
        if titulo_chave in self.root['livros']:
            return False
        self.root['livros'][titulo_chave] = Livro(titulo, autor)
        transaction.commit()
        return True

    def cadastrar_usuario(self, nome):
        nome_chave = nome.strip().lower()
        if nome_chave in self.root['usuarios']:
            return False
        self.root['usuarios'][nome_chave] = Usuario(nome)
        transaction.commit()
        return True

    def registrar_emprestimo(self, titulo_livro, nome_usuario):
        livro = self.root['livros'].get(titulo_livro.strip().lower())
        usuario = self.root['usuarios'].get(nome_usuario.strip().lower())

        if not livro or not usuario:
            return False, "Livro ou Usuário não encontrado."
        if livro.status == "Emprestado":
            return False, f"O livro já está com {livro.emprestado_para}."

        # Atualiza status e vincula
        livro.status = "Emprestado"
        livro.emprestado_para = usuario.nome
        usuario.livros_locados.append(livro.titulo)
        
        transaction.commit()
        return True, "Empréstimo realizado com sucesso!"

    def registrar_devolucao(self, titulo_livro):
        livro = self.root['livros'].get(titulo_livro.strip().lower())
        
        if not livro or livro.status == "Disponível":
            return False, "Livro não encontrado ou já está disponível."

        # Remove da lista do usuário
        usuario_nome = livro.emprestado_para
        usuario = self.root['usuarios'].get(usuario_nome.lower())
        if usuario:
            usuario.livros_locados.remove(livro.titulo)

        # Reseta livro
        livro.status = "Disponível"
        livro.emprestado_para = None
        
        transaction.commit()
        return True, "Devolução concluída!"

    def listar_livros(self):
        return list(self.root['livros'].values())

    def listar_usuarios(self):
        return list(self.root['usuarios'].values())

    def fechar(self):
        self.connection.close()
        self.db.close()
        self.storage.close()