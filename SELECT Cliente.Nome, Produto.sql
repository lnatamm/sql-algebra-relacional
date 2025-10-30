SELECT Cliente.Nome, Produto.Nome, Pedido.DataPedido, Produto.Preco, Pedido_has_Produto.Quantidade
FROM Cliente 
INNER JOIN Pedido ON Cliente.idCliente = Pedido.Cliente_idCliente 
INNER JOIN Pedido_has_Produto ON Pedido.idPedido = Pedido_has_Produto.Pedido_idPedido 
INNER JOIN Produto ON Pedido_has_Produto.Produto_idProduto = Produto.idProduto
 WHERE Produto.Preco > 100 AND Cliente.Nome = 'A';