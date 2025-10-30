import streamlit as st
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao
from classes.heuristica_reducao_tuplas import HeuristicaReducaoTuplas
from classes.heuristica_atributos import HeuristicaReducaoAtributos
from classes.heuristica_reordenar_folhas import HeuristicaReordenarFolhas
from classes.heuristica_evitar_joins import HeuristicaEvitarProdutoCartesiano

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
    # Cenário intencionalmente projetado para gerar produto cartesiano antes da heurística:
    # - o JOIN com Produto tem uma condição irrelevante (self-equality)
    # - a condição que realmente liga Produto a Pedido_has_Produto está no WHERE
    # A heurística `HeuristicaEvitarProdutoCartesiano` deve mover essa condição do WHERE
    # para o JOIN apropriado, evitando o produto cartesiano.
    "SELECT Cliente.Nome, Produto.Nome, Pedido.DataPedido "
    "FROM Cliente "
    "INNER JOIN Pedido ON Cliente.idCliente = Pedido.Cliente_idCliente "
    "INNER JOIN Pedido_has_Produto ON Pedido.idPedido = Pedido_has_Produto.Pedido_idPedido "
    "INNER JOIN Produto ON Produto.Nome = Produto.Nome "
    "WHERE Pedido_has_Produto.Produto_idProduto = Produto.idProduto AND Produto.Preco > 100;"
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

        # Aplica heurística para evitar produto cartesiano (move equijoins do WHERE para JOINs)
        heuristica_evitar = HeuristicaEvitarProdutoCartesiano(parsed_query_com_ambas)
        parsed_query_sem_prod = heuristica_evitar.otimizar()

        # Aplica heurística de reordenação às estruturas já otimizadas (usar versão sem produto cartesiano)
        heuristica_reord = HeuristicaReordenarFolhas(parsed_query_sem_prod)
        parsed_query_reordenado = heuristica_reord.otimizar()

        # Seção 1: Query Detalhada
        st.header("1. Query Detalhada")
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Query Original",
            "Com Heurística de Tuplas",
            "Com Ambas Heurísticas",
            "Sem Produto Cartesiano",
            "Com Reordenação de Folhas"
        ])

        with tab1:
            st.json(parsed_query_original)

        with tab2:
            st.json(parsed_query_com_tuplas)

        with tab3:
            st.json(parsed_query_com_ambas)

        with tab4:
            st.json(parsed_query_sem_prod)

        with tab5:
            st.json(parsed_query_reordenado)

        st.markdown("---")

        # Seção 2: Álgebra Relacional Final
        st.header("2. Álgebra Relacional Final")

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

        st.subheader("Sem Produto Cartesiano")
        algebra_relacional_semprod = AlgebraRelacional(parsed_query_sem_prod)
        algebra_final_semprod = algebra_relacional_semprod.converter()
        st.code(algebra_final_semprod, language="text")

        st.subheader("Com Reordenação de Folhas")
        algebra_relacional_reord = AlgebraRelacional(parsed_query_reordenado)
        algebra_final_reord = algebra_relacional_reord.converter()
        st.code(algebra_final_reord, language="text")

        st.markdown("---")

        # Seção 3: Grafo de Execução
        st.header("3. Grafo de Execução")

        col1, col2, col3, col4, col5 = st.columns(5)

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

        with col4:
            st.subheader("Com Reordenação de Folhas")
            gerador_grafo_reord = GrafoExecucao(parsed_query_reordenado)
            try:
                nome_arquivo_reord = "networkx_query_reordenado.png"
                caminho_grafo_reord = gerador_grafo_reord.gerar_grafo_networkx(nome_arquivo=nome_arquivo_reord)
                st.image(caminho_grafo_reord, caption="Grafo de Execução com Reordenação de Folhas", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")

        with col5:
            st.subheader("Sem Produto Cartesiano")
            gerador_grafo_semprod = GrafoExecucao(parsed_query_sem_prod)
            try:
                nome_arquivo_semprod = "networkx_query_semprod.png"
                caminho_grafo_semprod = gerador_grafo_semprod.gerar_grafo_networkx(nome_arquivo=nome_arquivo_semprod)
                st.image(caminho_grafo_semprod, caption="Grafo de Execução sem Produto Cartesiano", use_container_width=True)
            except ImportError as e:
                st.error(f"Erro: {str(e)}")
                st.info("Execute: `pip install networkx matplotlib`")
            except Exception as e:
                st.error(f"Erro ao gerar grafo: {str(e)}")

    else:
        st.error("Falha ao parsear a query.")