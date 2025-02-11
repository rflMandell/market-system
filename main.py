produtos = [
    {"ID": 1, "nome": "Arroz", "preco": 10.50, "quantidade": 50},
    {"ID": 2, "nome": "Feijão", "preco": 8.00, "quantidade": 30},
    {"ID": 3, "nome": "Macarrão", "preco": 4.50, "quantidade": 20},
    {"ID": 4, "nome": "Açúcar", "preco": 5.20, "quantidade": 40},
    {"ID": 5, "nome": "Sal", "preco": 2.00, "quantidade": 60},
    {"ID": 6, "nome": "Óleo de Soja", "preco": 9.80, "quantidade": 25},
    {"ID": 7, "nome": "Leite", "preco": 6.30, "quantidade": 35},
    {"ID": 8, "nome": "Café", "preco": 12.00, "quantidade": 15},
    {"ID": 9, "nome": "Farinha de Trigo", "preco": 4.80, "quantidade": 22},
    {"ID": 10, "nome": "Margarina", "preco": 3.90, "quantidade": 18},
    {"ID": 11, "nome": "Detergente", "preco": 2.50, "quantidade": 50},
    {"ID": 12, "nome": "Sabão em Pó", "preco": 15.00, "quantidade": 10},
    {"ID": 13, "nome": "Papel Higiênico", "preco": 11.50, "quantidade": 12},
    {"ID": 14, "nome": "Shampoo", "preco": 14.00, "quantidade": 8},
    {"ID": 15, "nome": "Creme Dental", "preco": 6.90, "quantidade": 20},
    {"ID": 16, "nome": "Molho de Tomate", "preco": 3.40, "quantidade": 25},
    {"ID": 17, "nome": "Biscoito", "preco": 7.20, "quantidade": 30},
    {"ID": 18, "nome": "Refrigerante", "preco": 8.50, "quantidade": 40},
    {"ID": 19, "nome": "Queijo Mussarela", "preco": 29.90, "quantidade": 15},
    {"ID": 20, "nome": "Presunto", "preco": 22.50, "quantidade": 18}
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
        consulta = input().strip()

        if consulta.lower() == "sair":
            print("Consulta cancelada.")
            return None

        produto_encontrado = None

        if consulta.isdigit():
            consulta = int(consulta)
            produto_encontrado = next((produto for produto in produtos if produto["ID"] == consulta), None)
        else:
            produto_encontrado = next((produto for produto in produtos if produto["nome"].lower() == consulta.lower()), None)

        if produto_encontrado:
            print(f"\nProduto encontrado:")
            print(f"Nome: {produto_encontrado['nome']}")
            print(f"Preço: R${produto_encontrado['preco']:.2f}")
            print(f"Quantidade: {produto_encontrado['quantidade']}")
            return produto_encontrado
        else:
            print("Produto não encontrado. Tente novamente ou digite 'sair' para cancelar.")

def cadastrar_produto(produtos):
    try:
        novo_id = int(input("Digite o ID do novo produto:\n-> "))
        novo_nome = input("Digite o nome do novo produto:\n-> ").strip()
        novo_preco = float(input("Digite o preco do novo produto:\n-> "))
        novo_quantidade = int(input("Digite a quantidade do novo produto:\n-> "))
        
        if any(produto["ID"] == novo_id for produto in produtos):
            print("Erro: ID já existe.")
            return

        novo_produto = {
            "ID": novo_id,
            "nome": novo_nome,
            "preco": novo_preco,
            "quantidade": novo_quantidade
        }
        produtos.append(novo_produto)
        print("Produto cadastrado com sucesso!")
    except ValueError:
        print("Erro: Entrada inválida. Certifique-se de digitar números para ID, preço e quantidade.")

def adicionar_quantidade(produtos):
    produto = consultar_produto(produtos)
    if produto:
        try:
            quantidade = int(input("Digite a quantidade a ser adicionada:\n-> "))
            if quantidade > 0:
                produto["quantidade"] += quantidade
                print(f"Quantidade atualizada com sucesso! Nova quantidade: {produto['quantidade']}")
            else:
                print("Erro: A quantidade deve ser maior que zero.")
        except ValueError:
            print("Erro: Entrada inválida. Certifique-se de digitar um número inteiro.")

def caixa(produtos):
    carrinho = []
    total_compra = 0.0

    while True:
        print("\n--- Modo Caixa ---")
        print("1 - Adicionar produto ao carrinho")
        print("2 - Visualizar carrinho")
        print("3 - Finalizar compra")
        print("4 - Cancelar compra")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            produto = consultar_produto(produtos)
            if produto:
                try:
                    quantidade = int(input(f"Digite a quantidade de '{produto['nome']}' que sera comprada: "))
                    if quantidade <= produto["quantidade"]:
                        carrinho.append({
                            "nome": produto["nome"],
                            "preco": produto["preco"],
                            "quantidade": quantidade
                        })
                        produto["quantidade"] -= quantidade
                        print(f"{quantidade} unidades de '{produto['nome']}' adicionadas ao carrinho.")
                    else:
                        print(f"Estoque insuficiente. Há apenas {produto['quantidade']} unidades disponíveis.")
                except ValueError:
                    print("Erro: Entrada inválida. Certifique-se de digitar um número inteiro.")

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
        print("\nEscolha uma opção: ")
        if cargo == "manager":
            print("1 - Consulta")
            print("2 - Caixa")
            print("3 - Cadastro")
            print("4 - Adicionar quantidade")
        elif cargo == "funcionario":
            print("1 - Consulta")
            print("2 - Caixa")
        
        opcao = input("Digite o número da opção desejada: ").strip()
        
        if opcao == "1":
            consultar_produto(produtos)
        elif opcao == "2":
            caixa(produtos)
        elif opcao == "3":
            if cargo == "manager":
                if autenticar_manager():
                    cadastrar_produto(produtos)
            else:
                print("Acesso negado: Você não tem permissão para cadastrar produtos.")
        elif opcao == "4":
            if cargo == "manager":
                if autenticar_manager():
                    adicionar_quantidade(produtos)
            else:
                print("Acesso negado: Você não tem permissão para adicionar quantidade.")
        else:
            print("Opção inválida. Tente novamente.")

cargo_usuario = input("Digite seu cargo (manager/funcionario): ").lower()
menu(cargo_usuario)