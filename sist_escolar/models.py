import ZODB, ZODB.FileStorage
import transaction
from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

class Aluno(Persistent):
    def __init__(self, matricula, nome):
        self.matricula = matricula
        self.nome = nome

class Turma(Persistent):
    def __init__(self, nome_turma):
        self.nome_turma = nome_turma
        self.alunos = PersistentMapping()  # {matricula: Aluno}
        self.frequencias = PersistentMapping() # {data: [matriculas_presentes]}

class SistemaEscolar:
    def __init__(self, db_path="escola.fs"):
        self.storage = ZODB.FileStorage.FileStorage(db_path)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        if 'turmas' not in self.root:
            self.root['turmas'] = PersistentMapping()
        transaction.commit()

    def criar_turma(self, nome):
        nome_id = nome.strip().upper()
        if nome_id in self.root['turmas']:
            return False
        self.root['turmas'][nome_id] = Turma(nome)
        transaction.commit()
        return True

    def cadastrar_aluno_na_turma(self, nome_turma, matricula, nome_aluno):
        turma = self.root['turmas'].get(nome_turma.strip().upper())
        if not turma:
            return False, "Turma não encontrada."
        if matricula in turma.alunos:
            return False, "Aluno já matriculado nesta turma."
        
        turma.alunos[matricula] = Aluno(matricula, nome_aluno)
        transaction.commit()
        return True, "Aluno cadastrado com sucesso!"

    def registrar_presenca(self, nome_turma, data, lista_matriculas):
        turma = self.root['turmas'].get(nome_turma.strip().upper())
        if not turma:
            return False, "Turma não encontrada."
        
        # Registra a lista de quem estava presente naquela data
        turma.frequencias[data] = PersistentList(lista_matriculas)
        transaction.commit()
        return True, f"Frequência do dia {data} registrada!"

    def obter_relatorio_turma(self, nome_turma):
        return self.root['turmas'].get(nome_turma.strip().upper())

    def listar_turmas(self):
        return self.root['turmas'].keys()

    def fechar(self):
        self.connection.close()
        self.db.close()
        self.storage.close()