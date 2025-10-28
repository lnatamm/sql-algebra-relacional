import streamlit as st
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao
from classes.heuristica_reducao_tuplas import HeuristicaReducaoTuplas
from classes.heuristica_atributos import HeuristicaReducaoAtributos

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
        # Query Original
        parsed_query_original = parsed_query
        
        # Aplicar heurística de redução de tuplas
        heuristica_tuplas = HeuristicaReducaoTuplas(parsed_query)
        parsed_query_com_tuplas = heuristica_tuplas.otimizar()
        
        # Aplicar heurística de redução de atributos (em cima da query já otimizada com tuplas)
        heuristica_atributos = HeuristicaReducaoAtributos(parsed_query_com_tuplas)
        parsed_query_com_ambas = heuristica_atributos.otimizar()
        
        # Seção 1: Query Detalhada
        st.header("1. Query Detalhada")
        tab1, tab2, tab3 = st.tabs(["Query Original", "Com Heurística de Tuplas", "Com Ambas Heurísticas"])
        
        with tab1:
            st.json(parsed_query_original)
        
        with tab2:
            st.json(parsed_query_com_tuplas)
        
        with tab3:
            st.json(parsed_query_com_ambas)
        
        st.markdown("---")
        
        # Seção 2: Álgebra Relacional Final
        st.header("2. Álgebra Relacional Final")
        
        col1, col2, col3 = st.columns(3)
        
        st.subheader("Query Original")
        algebra_relacional = AlgebraRelacional(parsed_query_original)
        algebra_final = algebra_relacional.converter()
        st.code(algebra_final, language="text")
        
        st.subheader("Com Heurística de Tuplas")
        algebra_relacional_tuplas = AlgebraRelacional(parsed_query_com_tuplas)
        algebra_final_tuplas = algebra_relacional_tuplas.converter()
        st.code(algebra_final_tuplas, language="text")
        
        st.subheader("Com Ambas Heurísticas")
        algebra_relacional_ambas = AlgebraRelacional(parsed_query_com_ambas)
        algebra_final_ambas = algebra_relacional_ambas.converter()
        st.code(algebra_final_ambas, language="text")
        
        st.markdown("---")
        
        # Seção 3: Grafo de Execução
        st.header("3. Grafo de Execução")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Query Original")
            gerador_grafo = GrafoExecucao(parsed_query_original)
            try:
                nome_arquivo = "networkx_query_original.png"
                caminho_grafo = gerador_grafo.gerar_grafo_networkx(nome_arquivo=nome_arquivo)
                st.image(caminho_grafo, caption="Grafo de Execução da Query Original", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")
        
        with col2:
            st.subheader("Com Heurística de Tuplas")
            gerador_grafo_tuplas = GrafoExecucao(parsed_query_com_tuplas)
            try:
                nome_arquivo_tuplas = "networkx_query_tuplas.png"
                caminho_grafo_tuplas = gerador_grafo_tuplas.gerar_grafo_networkx(nome_arquivo=nome_arquivo_tuplas)
                st.image(caminho_grafo_tuplas, caption="Grafo de Execução com Heurística de Tuplas", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")
        
        with col3:
            st.subheader("Com Ambas Heurísticas")
            gerador_grafo_ambas = GrafoExecucao(parsed_query_com_ambas)
            try:
                nome_arquivo_ambas = "networkx_query_ambas.png"
                caminho_grafo_ambas = gerador_grafo_ambas.gerar_grafo_networkx(nome_arquivo=nome_arquivo_ambas)
                st.image(caminho_grafo_ambas, caption="Grafo de Execução com Ambas Heurísticas", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")
    else:
        st.error("Falha ao parsear a query.")