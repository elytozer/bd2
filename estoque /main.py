from models import Estoque

def menu():
    sistema = Estoque()
    
    while True:
        print("\n--- SISTEMA DE ESTOQUE ZODB ---")
        print("1. Adicionar")
        print("2. Buscar")
        print("3. Listar")
        print("4. Atualizar")
        print("5. Remover")
        print("6. Sair") # <--- A OPÇÃO ESTÁ AQUI
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            # ... lógica de adicionar
            pass
        elif opcao == '6':
            print("Encerrando conexões e saindo...")
            sistema.encerrar_conexao() # Libera o arquivo estoque.fs.lock
            break 
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()