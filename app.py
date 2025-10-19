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
    value="SELECT Alunos.nome, Cursos.nome, Professores.nome FROM Alunos INNER JOIN Cursos ON Alunos.curso_id = Cursos.id INNER JOIN Professores ON Cursos.professor_id = Professores.id WHERE Cursos.nome = 'Banco de Dados';"
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
    else:
        st.text("Falha ao parsear a query.")