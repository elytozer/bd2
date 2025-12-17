from models import Biblioteca

def menu():
    bib = Biblioteca()
    
    while True:
        print("\n--- GESTÃO DE BIBLIOTECA ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Registrar Empréstimo")
        print("4. Registrar Devolução")
        print("5. Listar Livros")
        print("6. Listar Usuários")
        print("7. Sair")

        op = input("\nEscolha uma opção: ")

        if op == '1':
            t = input("Título do livro: ")
            a = input("Autor: ")
            if bib.cadastrar_livro(t, a): print("✅ Livro cadastrado!")
            else: print("❌ Erro: Livro já existe.")

        elif op == '2':
            n = input("Nome do usuário: ")
            if bib.cadastrar_usuario(n): print("✅ Usuário cadastrado!")
            else: print("❌ Erro: Usuário já existe.")

        elif op == '3':
            l = input("Título do livro: ")
            u = input("Nome do usuário: ")
            sucesso, msg = bib.registrar_emprestimo(l, u)
            print(f"{'✅' if sucesso else '❌'} {msg}")

        elif op == '4':
            l = input("Título do livro a devolver: ")
            sucesso, msg = bib.registrar_devolucao(l)
            print(f"{'✅' if sucesso else '❌'} {msg}")

        elif op == '5':
            livros = bib.listar_livros()
            print("\n--- ACERVO ---")
            for liv in livros:
                status_str = f"Emprestado para: {liv.emprestado_para}" if liv.status == "Emprestado" else "Disponível"
                print(f"📖 {liv.titulo} ({liv.autor}) - [{status_str}]")

        elif op == '6':
            usuarios = bib.listar_usuarios()
            print("\n--- USUÁRIOS E POSSES ---")
            for usu in usuarios:
                livros_posse = ", ".join(usu.livros_locados) if usu.livros_locados else "Nenhum livro"
                print(f"👤 {usu.nome} | Livros: {livros_posse}")

        elif op == '7':
            bib.fechar()
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()