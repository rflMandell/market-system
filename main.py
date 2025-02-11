produtos = [
    {"ID": 1, "nome": "Arroz", "preco": 10.50, "quantidade": 50},
    {"ID": 2, "nome": "Feijão", "preco": 8.00, "quantidade": 30},
    {"ID": 3, "nome": "Macarrão", "preco": 4.50, "quantidade": 20}
]

def consultar_produto(produtos):
    while True:
        print("\nDigite o ID ou o nome do item que deseja consultar (ou digite 'sair' para cancelar):")
        consulta = input()

        if consulta.lower() == "sair":
            print("Consulta cancelada.")
            break

        produto_encontrado = None

        if consulta.isdigit():
            consulta = int(consulta)
            for produto in produtos:
                if produto["ID"] == consulta:
                    produto_encontrado = produto
                    break
        else:
            for produto in produtos:
                if produto["nome"].lower() == consulta.lower():
                    produto_encontrado = produto
                    break

        if produto_encontrado:
            print(f"\nProduto encontrado:")
            print(f"Nome: {produto_encontrado['nome']}")
            print(f"Preço: R${produto_encontrado['preco']:.2f}")
            print(f"Quantidade: {produto_encontrado['quantidade']}")
            break
        else:
            print("Produto não encontrado. Tente novamente ou digite 'sair' para cancelar.")

def cadastrar_produto(produtos):
    novo_id = int(input(f"Digite o ID do novo produto:\n-> "))
    novo_nome = input(f"Digite o nome do novo produto:\n-> ")
    novo_preco = float(input(f"Digite o preco do novo produto:\n-> "))
    novo_quantidade = int(input(f"Digite a quantidade do novo produto:\n-> "))
    
    novo_produto = {
        "ID": novo_id,
        "nome": novo_nome,
        "preco": novo_preco,
        "quantidade": novo_quantidade
    }
    produtos.append(novo_produto)
    print("Produto cadastrado com sucesso!")

def caixa(produtos):
    print("")

# cargos manager x funcionario
def menu(cargo):
    while True:
        print("\nEscolha uma opcao: ")
        if cargo == "manager":
            print("1 - Consulta")
            print("2 - Caixa")
            print("3 - Cadastro")
        elif cargo == "funcionario":
            print("1 - Consulta")
            print("2 - Caixa")
        
        opcao = input("Digite o numero da opcao desejada: ")
        
        if opcao == "1":
            consultar_produto(produtos)
            break
        elif opcao == "2":
            caixa()
            break
        elif opcao == "3":
            if cargo == "manager":
                cadastrar_produto(produtos)
                break
            else:
                print("Acesso negado: Voce nao tem permissao para cadastrar produtos.")
        else:
            print("Opcao invalida. Tente novamente.")
            
cargo_usuario = input("Digite ser cargo (manager/funcionario): ").lower()
menu(cargo_usuario)
