from persistent import Persistent
from persistent.list import PersistentList

class Tarefa(Persistent):
    def __init__(self, descricao, concluida=False):
        self.descricao = descricao
        self.concluida = concluida

    def concluir(self):
        self.concluida = True

    def reabrir(self):
        self.concluida = False

    def __repr__(self):
        status = "Concluída" if self.concluida else "Não concluída"
        return f"{self.descricao} - {status}"

class ListaDeTarefas(Persistent):
    def __init__(self):
        self.tarefas = PersistentList()

    def adicionar_tarefa(self, descricao):
        tarefa = Tarefa(descricao)
        self.tarefas.append(tarefa)
        self._p_changed = 1 # Notifica o ZODB sobre a mudança

    def remover_tarefa(self, indice):
        if indice < len(self.tarefas):
            del self.tarefas[indice]
            self._p_changed = 1 # Notifica o ZODB sobre a mudança
        else:
            print("Índice inválido.")

    def concluir_tarefa(self, indice):
        if indice < len(self.tarefas):
            self.tarefas[indice].concluir()
            self._p_changed = 1 # Notifica o ZODB sobre a mudança
        else:
            print("Índice inválido.")

    def reabrir_tarefa(self, indice):
        if indice < len(self.tarefas):
            self.tarefas[indice].reabrir()
            self._p_changed = 1 # Notifica o ZODB sobre a mudança
        else:
            print("Índice inválido.")

    def __repr__(self):
        return "\n".join([str(tarefa) for tarefa in self.tarefas])