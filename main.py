import ZODB
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
from persistent import Persistent
import transaction
import os

# Classe de objeto persistente
class ExampleObject(Persistent):
    def __init__(self, value):
        self.value = value

# Função para criar ou abrir o banco de dados
def get_database(path):
    if not os.path.exists('db'):
        os.makedirs('db')
    storage = FileStorage(os.path.join('db', path))
    db = DB(storage)
    connection = db.open()
    return connection.root()

# Função para adicionar um objeto ao banco de dados
def add_object(root, key, value):
    root[key] = ExampleObject(value)
    transaction.commit()

# Função para recuperar um objeto do banco de dados
def get_object(root, key):
    return root[key].value if key in root else None

# Função para modificar um objeto no banco de dados
def modify_object(root, key, new_value):
    if key in root:
        root[key].value = new_value
        transaction.commit()

# Função principal
def main():
    root = get_database('mydata.fs')
    # Adicionar um objeto
    add_object(root, 'greeting', 'Hello, ZODB!')
    print("Objeto adicionado.")
    # Recuperar o objeto
    value = get_object(root, 'greeting')
    print(f"Valor recuperado: {value}")
    # Modificar o objeto
    modify_object(root, 'greeting', 'Hello, Modified ZODB!')
    print("Objeto modificado.")
    # Recuperar o objeto modificado
    value = get_object(root, 'greeting')
    print(f"Valor modificado recuperado: {value}")