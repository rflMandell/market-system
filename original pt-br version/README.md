# Gerenciador de Produtos

Este projeto é um sistema simples de gerenciamento de produtos usando SQLite3 em Python. Ele permite que usuários autenticados como "manager" ou "funcionário" realizem diversas operações em um banco de dados de produtos.

## Funcionalidades

- **Criar banco de dados e tabela de produtos** automaticamente na inicialização.
- **Consultar produtos** por ID ou nome.
- **Cadastrar novos produtos** (somente para "manager").
- **Adicionar quantidade a um produto existente** (somente para "manager").
- **Modo caixa**, permitindo adicionar produtos ao carrinho e finalizar compras.
- **Autenticação básica** para gestores antes de certas operações.

## Tecnologias Utilizadas

- **Python 3**
- **SQLite3** (banco de dados local embutido)

## Como Executar o Projeto

1. Certifique-se de ter o Python instalado em seu sistema.
2. Baixe o arquivo do código-fonte.
3. Execute o script no terminal ou prompt de comando:
   ```bash
   python nome_do_arquivo.py
   ```
4. Insira seu cargo quando solicitado ("manager" ou "funcionario").

## Estrutura do Código

- `conectar_banco()`: Estabelece conexão com o banco de dados.
- `criar_tabela()`: Cria a tabela de produtos caso não exista.
- `autenticar_manager()`: Solicita credenciais do administrador.
- `consultar_produto()`: Permite buscar um produto por ID ou nome.
- `cadastrar_produto()`: Adiciona um novo produto ao banco de dados.
- `adicionar_quantidade()`: Aumenta o estoque de um produto existente.
- `caixa()`: Simula um caixa de vendas com carrinho de compras.
- `menu()`: Apresenta opções de ações de acordo com o cargo do usuário.

## Exemplo de Uso

Ao executar o script, o usuário deve informar seu cargo:
```bash
digite seu cargo (manager/funcionario):
```

Se for **manager**, poderá cadastrar produtos e adicionar quantidade. Se for **funcionário**, terá acesso apenas à consulta e ao modo caixa.

### Consulta de Produto
```bash
digite o id ou o nome do item que deseja consultar:
```

### Cadastro de Produto (somente "manager")
```bash
digite o nome do novo produto:
digite o preço do novo produto:
digite a quantidade do novo produto:
```

### Adicionar Quantidade (somente "manager")
```bash
digite a quantidade a ser adicionada:
```

### Modo Caixa
```bash
1 - adicionar produto ao carrinho
2 - visualizar carrinho
3 - finalizar compra
4 - cancelar compra
```

## Melhorias Futuras
- Implementação de um sistema de autenticação mais seguro.
- Interface gráfica para facilitar a usabilidade.
- Suporte para múltiplos usuários com permissões diferentes.

## Licença
Este projeto está sob a licença MIT.
