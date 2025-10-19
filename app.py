import streamlit as st
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional

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

query_input = st.text_area(
    "Digite sua query SQL:",
    height=100,
    placeholder="SELECT * FROM tabela WHERE condicao;"
)

# Botão para processar
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    processar = st.button("🚀 Converter", type="primary", use_container_width=True)
with col2:
    limpar = st.button("🗑️ Limpar", use_container_width=True)

if limpar:
    st.rerun()

# Processar a query
if processar and query_input:
    parsed_query = Parser().parse(query_input.upper())

    if parsed_query:
        st.text("Query Parseada:")
        st.json(parsed_query)
        
        algebra_relacional = AlgebraRelacional(parsed_query)

        expressao_algebra = algebra_relacional.converter()
        st.text("Álgebra Relacional:")
        st.text(expressao_algebra)

        detalhamento = algebra_relacional.converter_detalhado()
        st.text("Detalhamento da Conversão:")
        st.text(detalhamento)
        
    else:
        st.text("Falha ao parsear a query.")