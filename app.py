import streamlit as st
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao
from classes.heuristica_reducao_tuplas import HeuristicaReducaoTuplas

# Configuração da página
st.set_page_config(
    page_title="SQL para Álgebra Relacional",
    page_icon="🔄",
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
        # Aplicar heurística de redução de tuplas
        heuristica = HeuristicaReducaoTuplas(parsed_query)
        parsed_query_otimizada = heuristica.otimizar()
        
        # Seção 1: Query Detalhada
        st.header("1. Query Detalhada")
        tab1, tab2 = st.tabs(["Query Original", "Query com Heurística"])
        
        with tab1:
            st.json(parsed_query)
        
        with tab2:
            st.json(parsed_query_otimizada)
        
        st.markdown("---")
        
        # Seção 2: Álgebra Relacional Final
        st.header("2. Álgebra Relacional Final")
        tab3, tab4 = st.tabs(["Query Original", "Query com Heurística"])
        
        with tab3:
            algebra_relacional = AlgebraRelacional(parsed_query)
            algebra_final = algebra_relacional.converter()
            st.code(algebra_final, language="text")
        
        with tab4:
            algebra_relacional_otimizada = AlgebraRelacional(parsed_query_otimizada)
            algebra_final_otimizada = algebra_relacional_otimizada.converter()
            st.code(algebra_final_otimizada, language="text")
        
        st.markdown("---")
        
        # Seção 3: Grafo de Execução
        st.header("3. Grafo de Execução")
        tab5, tab6 = st.tabs(["Query Original", "Query com Heurística"])
        
        with tab5:
            gerador_grafo = GrafoExecucao(parsed_query)
            try:
                nome_arquivo = "networkx_query_original.png"
                caminho_grafo = gerador_grafo.gerar_grafo_networkx(nome_arquivo=nome_arquivo)
                st.image(caminho_grafo, caption="Grafo de Execução da Query Original", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")
        
        with tab6:
            gerador_grafo_otimizado = GrafoExecucao(parsed_query_otimizada)
            try:
                nome_arquivo_otimizado = "networkx_query_otimizada.png"
                caminho_grafo_otimizado = gerador_grafo_otimizado.gerar_grafo_networkx(nome_arquivo=nome_arquivo_otimizado)
                st.image(caminho_grafo_otimizado, caption="Grafo de Execução da Query Otimizada", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")
    else:
        st.error("Falha ao parsear a query.")