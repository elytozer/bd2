from models import SistemaEscolar

def menu():
    escola = SistemaEscolar()
    
    while True:
        print("\n--- SISTEMA ESCOLAR (FREQUÊNCIA) ---")
        print("1. Criar Turma")
        print("2. Cadastrar Aluno em Turma")
        print("3. Lançar Frequência")
        print("4. Ver Relatório de Frequência")
        print("5. Sair")

        op = input("\nEscolha: ")

        if op == '1':
            nome = input("Nome da Turma (ex: 3A, 9B): ")
            if escola.criar_turma(nome): print("✅ Turma criada!")
            else: print("❌ Turma já existe.")

        elif op == '2':
            t = input("Nome da Turma: ")
            m = input("Matrícula do Aluno: ")
            n = input("Nome do Aluno: ")
            sucesso, msg = escola.cadastrar_aluno_na_turma(t, m, n)
            print(f"{'✅' if sucesso else '❌'} {msg}")

        elif op == '3':
            t_nome = input("Turma: ")
            turma = escola.obter_relatorio_turma(t_nome)
            if not turma:
                print("❌ Turma não encontrada.")
                continue
            
            data = input("Data da aula (DD/MM/AAAA): ")
            presentes = []
            print(f"\nChamada para a turma {t_nome}:")
            for m, aluno in turma.alunos.items():
                presenca = input(f"Aluno: {aluno.nome} ({m}) está presente? (s/n): ").lower()
                if presenca == 's':
                    presentes.append(m)
            
            escola.registrar_presenca(t_nome, data, presentes)
            print("✅ Chamada finalizada e salva!")

        elif op == '4':
            t_nome = input("Ver relatório de qual turma: ")
            turma = escola.obter_relatorio_turma(t_nome)
            if not turma:
                print("❌ Turma não encontrada.")
                continue
            
            print(f"\n--- RELATÓRIO DE FREQUÊNCIA: {turma.nome_turma} ---")
            if not turma.frequencias:
                print("Nenhuma aula registrada ainda.")
            else:
                for data, presentes in turma.frequencias.items():
                    print(f"\n📅 Data: {data}")
                    for m, aluno in turma.alunos.items():
                        status = "PRESENTE" if m in presentes else "FALTOU"
                        print(f"   - {aluno.nome}: {status}")

        elif op == '5':
            escola.fechar()
            break

if __name__ == "__main__":
    menu()