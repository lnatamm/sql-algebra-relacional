import streamlit as st
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao
import consts
from classes.heuristica_reducao_tuplas import HeuristicaReducaoTuplas

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

# Default mais complexo para demonstrar as heurísticas (múltiplas junções e filtros)
default_query = (
    "SELECT Cliente.Nome, Produto.Nome, Pedido.DataPedido "
    "FROM Cliente "
    "INNER JOIN Pedido ON Cliente.idCliente = Pedido.Cliente_idCliente "
    "INNER JOIN Pedido_has_Produto ON Pedido.idPedido = Pedido_has_Produto.Pedido_idPedido "
    "INNER JOIN Produto ON Pedido_has_Produto.Produto_idProduto = Produto.idProduto "
    "WHERE Produto.Preco > 100 AND Cliente.Nome LIKE 'A%';"
)

# Estatísticas simuladas das tabelas (para reordenação de joins)
estatisticas_tabelas = {
    'CLIENTE': {'num_tuplas': 50000},      # Muitos clientes
    'PEDIDO': {'num_tuplas': 200000},      # Muitos pedidos
    'PEDIDO_HAS_PRODUTO': {'num_tuplas': 500000},  # Muitos itens
    'PRODUTO': {'num_tuplas': 5000}        # Menos produtos (mais seletivo)
}

query_input = st.text_area(
    "Digite sua query SQL:",
    height=140,
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

        # ==========================
        # Etapa adicional: aplicar heurística de redução de tuplas
        # ==========================
        st.subheader("⚡ Otimização - Heurística de Redução de Tuplas")
        try:
            otimizador = HeuristicaReducaoTuplas(parsed_query, estatisticas_tabelas)
            resultado_otimizacao = otimizador.otimizar()

            # Mostrar álgebra original e otimizada
            original_algebra = algebra_relacional.converter()
            
            col_antes, col_depois = st.columns(2)
            with col_antes:
                st.markdown("**🔴 ANTES (Original):**")
                st.code(original_algebra, language="text")
            
            with col_depois:
                st.markdown("**🟢 DEPOIS (Otimizada):**")
                st.code(resultado_otimizacao.get('algebra_otimizada', ''), language="text")

            st.markdown("**Otimizações Aplicadas:**")
            explic = resultado_otimizacao.get('explicacao', [])
            if explic:
                for linha in explic:
                    st.write(f"- {linha}")
            else:
                st.write("Nenhuma otimização aplicada.")

            # Comparação dos grafos (Mermaid) e ordem de execução
            st.markdown("---")
            st.subheader("🔍 Comparação de Grafos: Antes x Depois")
            try:
                orig_grafo = GrafoExecucao(parsed_query)
                orig_mermaid = orig_grafo.gerar_mermaid(direcao='TB', incluir_legenda=False)

                # construir parsed_query otimizado (se fornecido)
                parsed_otimizado = resultado_otimizacao.get('query_otimizada', parsed_query)
                opt_grafo = GrafoExecucao(parsed_otimizado)
                opt_mermaid = opt_grafo.gerar_mermaid(direcao='TB', incluir_legenda=False)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🔴 ANTES - Árvore de Execução Original**")
                    st.code(orig_mermaid, language="mermaid")
                    st.markdown("**Ordem de Execução (Antes):**")
                    ordem_orig = orig_grafo.gerar_ordem_execucao()
                    for i, (op, desc) in enumerate(ordem_orig, 1):
                        st.write(f"{i}. [{op}] {desc}")

                with col2:
                    st.markdown("**🟢 DEPOIS - Árvore de Execução Otimizada**")
                    st.code(opt_mermaid, language="mermaid")
                    st.markdown("**Ordem de Execução (Depois):**")
                    ordem_opt = opt_grafo.gerar_ordem_execucao()
                    for i, (op, desc) in enumerate(ordem_opt, 1):
                        st.write(f"{i}. [{op}] {desc}")
                
                # Métricas de comparação
                st.markdown("---")
                st.markdown("**📊 Comparação de Métricas:**")
                met_col1, met_col2, met_col3 = st.columns(3)
                with met_col1:
                    st.metric("Operações Antes", len(ordem_orig))
                with met_col2:
                    st.metric("Operações Depois", len(ordem_opt))
                with met_col3:
                    reducao = len(ordem_orig) - len(ordem_opt)
                    st.metric("Redução", f"{reducao}", delta=f"{reducao} ops" if reducao != 0 else "Igual")

            except Exception as e:
                st.error(f"Erro ao gerar comparação dos grafos: {e}")

        except Exception as e:
            st.error(f"Erro ao aplicar heurística: {e}")

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