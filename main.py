import sqlite3

def conectar_banco():
    conn = sqlite3.connect('produtos.db')
    return conn

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def autenticar_manager():
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    
    if username == "admin" and password == "admin":
        return True
    else:
        print("Credenciais inválidas. Acesso negado.")
        return False

def consultar_produto():
    conn = conectar_banco()
    cursor = conn.cursor()

    consulta = input("Digite o ID ou o nome do item que deseja consultar (ou 'sair' para cancelar): ").strip()

    if consulta.lower() == "sair":
        print("Consulta cancelada.")
        return None

    if consulta.isdigit():
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (int(consulta),))
    else:
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{consulta}%",))

    produto = cursor.fetchone()
    conn.close()

    if produto:
        print(f"\nProduto encontrado:")
        print(f"ID: {produto[0]}")
        print(f"Nome: {produto[1]}")
        print(f"Preço: R${produto[2]:.2f}")
        print(f"Quantidade: {produto[3]}")
        return produto
    else:
        print("Produto não encontrado.")
        return None

def cadastrar_produto():
    try:
        nome = input("Digite o nome do novo produto:\n-> ").strip()
        preco = float(input("Digite o preço do novo produto:\n-> "))
        quantidade = int(input("Digite a quantidade do novo produto:\n-> "))

        conn = conectar_banco()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
        conn.commit()
        conn.close()

        print("Produto cadastrado com sucesso!")
    except ValueError:
        print("Erro: Entrada inválida. Certifique-se de digitar números para preço e quantidade.")

def adicionar_quantidade():
    produto = consultar_produto()
    if produto:
        try:
            quantidade = int(input("Digite a quantidade a ser adicionada:\n-> "))
            if quantidade > 0:
                conn = conectar_banco()
                cursor = conn.cursor()

                cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto[0]))
                conn.commit()
                conn.close()

                print(f"Quantidade atualizada com sucesso! Nova quantidade: {produto[3] + quantidade}")
            else:
                print("Erro: A quantidade deve ser maior que zero.")
        except ValueError:
            print("Erro: Entrada inválida. Certifique-se de digitar um número inteiro.")

def caixa():
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
            produto = consultar_produto()
            if produto:
                try:
                    quantidade = int(input(f"Digite a quantidade de '{produto[1]}' que deseja comprar: "))
                    if quantidade <= produto[3]:
                        carrinho.append({
                            "nome": produto[1],
                            "preco": produto[2],
                            "quantidade": quantidade
                        })

                        conn = conectar_banco()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto[0]))
                        conn.commit()
                        conn.close()

                        print(f"{quantidade} unidades de '{produto[1]}' adicionadas ao carrinho.")
                    else:
                        print(f"Estoque insuficiente. Há apenas {produto[3]} unidades disponíveis.")
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

# Menu principal
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
            consultar_produto()
        elif opcao == "2":
            caixa()
        elif opcao == "3":
            if cargo == "manager":
                if autenticar_manager():
                    cadastrar_produto()
            else:
                print("Acesso negado: Você não tem permissão para cadastrar produtos.")
        elif opcao == "4":
            if cargo == "manager":
                if autenticar_manager():
                    adicionar_quantidade()
            else:
                print("Acesso negado: Você não tem permissão para adicionar quantidade.")
        else:
            print("Opção inválida. Tente novamente.")

# Inicialização do sistema vambora krl isso demorou mais do que devia mds do ceuaaaaaaaaaa
if __name__ == "__main__":
    criar_tabela()
    cargo_usuario = input("Digite seu cargo (manager/funcionario): ").lower()
    menu(cargo_usuario)