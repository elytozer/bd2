import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent

class Produto(Persistent):
    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade = quantidade

class Estoque:
    def __init__(self, db_path="estoque.fs"):
        self.storage = ZODB.FileStorage.FileStorage(db_path)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        if 'produtos' not in self.root:
            self.root['produtos'] = {}
            transaction.commit()

    def encerrar_conexao(self):
        """Fecha o banco de forma segura para liberar os arquivos .lock"""
        self.connection.close()
        self.db.close()
        self.storage.close()

    # ... (métodos adicionar, buscar, listar, atualizar, remover permanecem aqui)