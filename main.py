produtos = [
    {"ID": 1, "nome": "Arroz", "preco": 10.50, "quantidade": 50},
    {"ID": 2, "nome": "Feijão", "preco": 8.00, "quantidade": 30},
    {"ID": 3, "nome": "Macarrão", "preco": 4.50, "quantidade": 20}
]

manager_login = {
    "username": "admin",
    "password": "admin"
}
def autenticar_manager():
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    
    if username == manager_login["username"] and password == manager_login["password"]:
        return True
    else:
        print("Credenciais inválidas. Acesso negado.")
        return False

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
    carrinho = []  # Lista para armazenar os produtos selecionados
    total_compra = 0.0  # Variável para armazenar o valor total da compra

    while True:
        print("\n--- Modo Caixa ---")
        print("1 - Adicionar produto ao carrinho")
        print("2 - Visualizar carrinho")
        print("3 - Finalizar compra")
        print("4 - Cancelar compra")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            consultar_produto(produtos)
            produto_id = input("Digite o ID do produto que deseja adicionar ao carrinho (ou 'sair' para cancelar): ")

            if produto_id.lower() == "sair":
                continue

            produto_id = int(produto_id)
            produto_encontrado = None

            for produto in produtos:
                if produto["ID"] == produto_id:
                    produto_encontrado = produto
                    break

            if produto_encontrado:
                quantidade = int(input(f"Digite a quantidade de '{produto_encontrado['nome']}' que deseja comprar: "))

                if quantidade <= produto_encontrado["quantidade"]:

                    carrinho.append({
                        "nome": produto_encontrado["nome"],
                        "preco": produto_encontrado["preco"],
                        "quantidade": quantidade
                    })

                    produto_encontrado["quantidade"] -= quantidade
                    print(f"{quantidade} unidades de '{produto_encontrado['nome']}' adicionadas ao carrinho.")
                else:
                    print(f"Estoque insuficiente. Há apenas {produto_encontrado['quantidade']} unidades disponíveis.")
            else:
                print("Produto não encontrado.")

        elif opcao == "2":
            if not carrinho:
                print("O carrinho está vazio.")
            else:
                print("\n--- Carrinho de Compras ---")
                for item in carrinho:
                    print(f"{item['quantidade']} x {item['nome']} - R${item['preco']:.2f} cada")
                print("--------------------------")

        elif opcao == "3":
            if not carrinho:
                print("O carrinho está vazio. Nada para finalizar.")
            else:
                print("\n--- Finalizando Compra ---")
                total_compra = sum(item["preco"] * item["quantidade"] for item in carrinho)
                print(f"Total da compra: R${total_compra:.2f}")
                print("Compra finalizada com sucesso!")
                carrinho.clear()
                break

        elif opcao == "4":
            print("Compra cancelada. Todos os itens foram removidos do carrinho.")
            carrinho.clear()
            break

        else:
            print("Opção inválida. Tente novamente.")

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
            caixa(produtos)
            break
        elif opcao == "3":
            if cargo == "manager":
                if autenticar_manager():
                    cadastrar_produto(produtos)
                break
            else:
                print("Acesso negado: Voce nao tem permissao para cadastrar produtos.")
        else:
            print("Opcao invalida. Tente novamente.")
            
cargo_usuario = input("Digite seu cargo (manager/funcionario): ").lower()
menu(cargo_usuario)