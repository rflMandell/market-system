produtos = [
    {"nome": "detergente", "ID": 1000, "quantidade": 0, "preco": 10.00},
    {"nome": "alcool", "ID": 2000, "quantidade": 0, "preco": 15.00}
    ]

print("Digite o ID do item que deseja consultar")
consulta = int(input())

produto_encontrado = ""

for produto in produtos:
    if produto["ID"] == consulta:
        produto_encontrado = produto
        break

if produto_encontrado:
    print(f"{produto_encontrado['nome']}, {produto_encontrado['preco']}, {produto_encontrado['quantidade']}")
else:
    print("produto nao encontrado")