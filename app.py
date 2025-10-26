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
st.title("Conversor SQL para Álgebra Relacional")
st.markdown("---")

# Área de input da query
st.subheader("Query SQL")

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
processar = st.button("Converter", type="primary", use_container_width=True)

# Processar a query
if processar and query_input:
    parsed_query = Parser().parse(query_input.upper())

    if parsed_query:
        # 1. Query Detalhada
        st.subheader("1. Query Detalhada")
        st.json(parsed_query)
        
        st.markdown("---")
        
        # 2. Álgebra Relacional Final
        st.subheader("2. Álgebra Relacional Final")
        algebra_relacional = AlgebraRelacional(parsed_query)
        algebra_final = algebra_relacional.converter()
        st.code(algebra_final)
        
        st.markdown("---")
        
        # 3. Grafo de Execução
        st.subheader("3. Grafo de Execução")
        gerador_grafo = GrafoExecucao(parsed_query)
        try:
            nome_arquivo = "networkx_query.png"
            caminho_grafo = gerador_grafo.gerar_grafo_networkx(nome_arquivo=nome_arquivo)
            st.image(caminho_grafo, caption="Grafo de Execução da Query", use_container_width=True)
        except ImportError as e:
            st.error(f"Erro: {str(e)}")
            st.info("Execute: `pip install networkx matplotlib`")
        except Exception as e:
            st.error(f"Erro ao gerar grafo: {str(e)}")
    else:
        st.error("Falha ao parsear a query.")