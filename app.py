import streamlit as st
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao

# Configuração da página
st.set_page_config(
    page_title="SQL para Álgebra Relacional",
    page_icon="🔄",
    layout="wide"
)

# Título principal
st.title("🔄 Conversor SQL para Álgebra Relacional")
st.markdown("---")

# Área de input da query
st.subheader("📝 Query SQL")

default_query = (
    "SELECT Cliente.Nome, Produto.Nome, Pedido.DataPedido "
    "FROM Cliente "
    "INNER JOIN Pedido ON Cliente.idCliente = Pedido.Cliente_idCliente "
    "INNER JOIN Pedido_has_Produto ON Pedido.idPedido = Pedido_has_Produto.Pedido_idPedido "
    "INNER JOIN Produto ON Pedido_has_Produto.Produto_idProduto = Produto.idProduto "
    "WHERE Produto.Preco > 100 AND Cliente.Nome LIKE 'A%';"
)

query_input = st.text_area(
    "Digite sua query SQL:",
    height=100,
    value=default_query
)

# Botão para processar
processar = st.button("🚀 Converter", type="primary", use_container_width=True)

# Processar a query
if processar and query_input:
    parsed_query = Parser().parse(query_input.upper())

    if parsed_query:
        st.subheader("📊 Query Detalhada:")
        st.json(parsed_query)

        st.subheader("⚙️ Conversão para Álgebra Relacional:")
        algebra_relacional = AlgebraRelacional(parsed_query)
        detalhamento = algebra_relacional.converter_detalhado()
        items = list(detalhamento.items())
        for key, value in items[:-1]:
            st.markdown(f"**{key}**")
            st.code(value)

        gerador_grafo = GrafoExecucao(parsed_query)
            
        # Árvore ASCII
        print(gerador_grafo.gerar_ascii_tree())
        
        # Ordem de execução
        print("\nOrdem de Execução:")
        ordem = gerador_grafo.gerar_ordem_execucao()
        for i, (op, desc) in enumerate(ordem, 1):
            print(f"  {i}. [{op:8}] {desc}")
        
        # Estatísticas
        print("\nEstatísticas:")
        stats = gerador_grafo.exibir_estatisticas()
        for chave, valor in stats.items():
            print(f"  • {chave}: {valor}")
        
        # Tentar gerar grafo visual
        nome_arquivo = "grafo_query"
        # output = gerador_grafo.gerar_grafo(formato='png', nome_arquivo=nome_arquivo)
        gerador_grafo.gerar_mermaid(direcao='TB', incluir_legenda=True)
        gerador_grafo.gerar_grafo_networkx(nome_arquivo=f"networkx_query.png")
    else:
        st.text("Falha ao parsear a query.")