PADRAO = (
    r"^SELECT\s+(?P<select>[\w\.\s,\*]+)\s+"       # permite . nos nomes e *
    r"FROM\s+(?P<from>\w+)"                        # nome da tabela após FROM
    r"(?P<joins>(?:\s+INNER\s+JOIN\s+\w+\s+ON\s+\w+\.\w+\s*=\s*\w+\.\w+)*)"  # zero ou mais INNER JOINs
    r"(?:\s+WHERE\s+(?P<where>.+?))?"              # cláusula WHERE opcional
    r";?$"                                         # final opcional com ;
)

PALAVRAS_RESERVADAS = {
    "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "RIGHT", "ON",
    "AS", "AND", "OR", "NOT", "INSERT", "UPDATE", "DELETE", "CREATE",
    "DROP", "TABLE", "VALUES", "INTO", "GROUP", "BY", "HAVING", "ORDER"
}

TABELAS = [
    "Categoria",
    "Produto",
    "TipoCliente",
    "Cliente",
    "TipoEndereco",
    "Endereco",
    "Telefone",
    "Status",
    "Pedido",
    "Pedido_has_Produto"
]

COLUNAS = [
    # Tabela Categoria
    "Categoria.idCategoria",
    "Categoria.Descricao",
    
    # Tabela Produto
    "Produto.idProduto",
    "Produto.Nome",
    "Produto.Descricao",
    "Produto.Preco",
    "Produto.QuantEstoque",
    "Produto.Categoria_idCategoria",
    
    # Tabela TipoCliente
    "TipoCliente.idTipoCliente",
    "TipoCliente.Descricao",
    
    # Tabela Cliente
    "Cliente.idCliente",
    "Cliente.Nome",
    "Cliente.Email",
    "Cliente.Nascimento",
    "Cliente.Senha",
    "Cliente.TipoCliente_idTipoCliente",
    "Cliente.DataRegistro",
    
    # Tabela TipoEndereco
    "TipoEndereco.idTipoEndereco",
    "TipoEndereco.Descricao",
    
    # Tabela Endereco
    "Endereco.idEndereco",
    "Endereco.EnderecoPadrao",
    "Endereco.Logradouro",
    "Endereco.Numero",
    "Endereco.Complemento",
    "Endereco.Bairro",
    "Endereco.Cidade",
    "Endereco.UF",
    "Endereco.CEP",
    "Endereco.TipoEndereco_idTipoEndereco",
    "Endereco.Cliente_idCliente",
    
    # Tabela Telefone
    "Telefone.Numero",
    "Telefone.Cliente_idCliente",
    
    # Tabela Status
    "Status.idStatus",
    "Status.Descricao",
    
    # Tabela Pedido
    "Pedido.idPedido",
    "Pedido.Status_idStatus",
    "Pedido.DataPedido",
    "Pedido.ValorTotalPedido",
    "Pedido.Cliente_idCliente",
    
    # Tabela Pedido_has_Produto
    "Pedido_has_Produto.idPedidoProduto",
    "Pedido_has_Produto.Pedido_idPedido",
    "Pedido_has_Produto.Produto_idProduto",
    "Pedido_has_Produto.Quantidade",
    "Pedido_has_Produto.PrecoUnitario"
]