import sqlite3

def conectar_banco():
    conn = sqlite3.connect('produtos.db')
    return conn

def criar_tabela():
    conn = conectar_banco()
    try:
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
    finally:
        conn.close()

def autenticar_manager():
    username = input("digite o nome de usuário: ").strip()
    password = input("digite a senha: ").strip()
    
    if username == "admin" and password == "admin":
        return True
    else:
        print("credenciais inválidas. acesso negado.")
        return False

def consultar_produto():
    conn = conectar_banco()
    try:
        cursor = conn.cursor()
        consulta = input("digite o id ou o nome do item que deseja consultar (ou 'sair' para cancelar): ").strip()

        if consulta.lower() == "sair":
            print("consulta cancelada.")
            return None

        if consulta.isdigit():
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (int(consulta),))
        else:
            cursor.execute("SELECT * FROM produtos WHERE nome LIKE ? COLLATE NOCASE", (f"%{consulta}%",))

        produto = cursor.fetchone()

        if produto:
            print("\nproduto encontrado:")
            print(f"id: {produto[0]}")
            print(f"nome: {produto[1]}")
            print(f"preço: R${produto[2]:.2f}")
            print(f"quantidade: {produto[3]}")
            return produto
        else:
            print("produto não encontrado.")
            return None
    finally:
        conn.close()

def cadastrar_produto():
    try:
        nome = input("digite o nome do novo produto:\n-> ").strip()
        preco = float(input("digite o preço do novo produto:\n-> "))
        quantidade = int(input("digite a quantidade do novo produto:\n-> "))

        conn = conectar_banco()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
            conn.commit()
            print("produto cadastrado com sucesso!")
        finally:
            conn.close()
    except ValueError as e:
        print(f"erro: entrada inválida. certifique-se de digitar números para preço e quantidade. detalhes: {e}")

def adicionar_quantidade():
    produto = consultar_produto()
    if produto:
        try:
            quantidade = int(input("digite a quantidade a ser adicionada:\n-> "))
            if quantidade > 0:
                conn = conectar_banco()
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto[0]))
                    conn.commit()

                    # buscar a quantidade atualizada
                    cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto[0],))
                    nova_quantidade = cursor.fetchone()[0]

                    print(f"quantidade atualizada com sucesso! nova quantidade: {nova_quantidade}")
                finally:
                    conn.close()
            else:
                print("erro: a quantidade deve ser maior que zero.")
        except ValueError:
            print("erro: entrada inválida. certifique-se de digitar um número inteiro.")

def caixa():
    carrinho = []
    total_compra = 0.0

    while True:
        print("\n--- modo caixa ---")
        print("1 - adicionar produto ao carrinho")
        print("2 - visualizar carrinho")
        print("3 - finalizar compra")
        print("4 - cancelar compra")
        opcao = input("escolha uma opção: ").strip()

        if opcao == "1":
            produto = consultar_produto()
            if produto is not None:
                try:
                    quantidade = int(input(f"digite a quantidade de '{produto[1]}' que deseja comprar: "))
                    if quantidade <= produto[3]:
                        carrinho.append({
                            "nome": produto[1],
                            "preco": produto[2],
                            "quantidade": quantidade
                        })

                        conn = conectar_banco()
                        try:
                            cursor = conn.cursor()
                            cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto[0]))
                            conn.commit()
                        finally:
                            conn.close()

                        print(f"{quantidade} unidades de '{produto[1]}' adicionadas ao carrinho.")
                    else:
                        print(f"estoque insuficiente. há apenas {produto[3]} unidades disponíveis.")
                except ValueError:
                    print("erro: entrada inválida. certifique-se de digitar um número inteiro.")

        elif opcao == "2":
            if not carrinho:
                print("o carrinho está vazio.")
            else:
                print("\n--- carrinho de compras ---")
                for item in carrinho:
                    print(f"{item['quantidade']} x {item['nome']} - R${item['preco']:.2f} cada")
                print("--------------------------")

        elif opcao == "3":
            if not carrinho:
                print("o carrinho está vazio. nada para finalizar.")
            else:
                print("\n--- finalizando compra ---")
                total_compra = sum(item["preco"] * item["quantidade"] for item in carrinho)
                print(f"total da compra: R${total_compra:.2f}")
                print("compra finalizada com sucesso!")
                carrinho.clear()
                break

        elif opcao == "4":
            print("compra cancelada. todos os itens foram removidos do carrinho.")
            carrinho.clear()
            break

        else:
            print("opção inválida. tente novamente.")

def menu(cargo):
    while True:
        print("\nescolha uma opção: ")
        if cargo == "manager":
            print("1 - consulta")
            print("2 - caixa")
            print("3 - cadastro")
            print("4 - adicionar quantidade")
        elif cargo == "funcionario":
            print("1 - consulta")
            print("2 - caixa")
        
        opcao = input("digite o número da opção desejada: ").strip()
        
        if opcao == "1":
            consultar_produto()
        elif opcao == "2":
            caixa()
        elif opcao == "3":
            if cargo == "manager":
                if autenticar_manager():
                    cadastrar_produto()
            else:
                print("acesso negado: você não tem permissão para cadastrar produtos.")
        elif opcao == "4":
            if cargo == "manager":
                if autenticar_manager():
                    adicionar_quantidade()
            else:
                print("acesso negado: você não tem permissão para adicionar quantidade.")
        else:
            print("opção inválida. tente novamente.")

# inicialização do sistema
if __name__ == "__main__":
    criar_tabela()
    while True:
        cargo_usuario = input("digite seu cargo (manager/funcionario): ").lower()
        if cargo_usuario in ["manager", "funcionario"]:
            break
        else:
            print("cargo inválido. digite 'manager' ou 'funcionario'.")
    menu(cargo_usuario)