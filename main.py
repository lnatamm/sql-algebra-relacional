from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional

if __name__ == "__main__":
    queries = [
        "SELECT Alunos.nome, Cursos.nome, Professores.nome FROM Alunos INNER JOIN Cursos ON Alunos.curso_id = Cursos.id INNER JOIN Professores ON Cursos.professor_id = Professores.id WHERE Cursos.nome = 'Banco de Dados';",
        "SELECT * FROM teste WHERE idade >= 18;",
        "SELECT nome, idade FROM Pessoa;",
    ]
    
    for query in queries:
        print("\nQuery SQL:", query)

        parsed_query = Parser().parse(query.upper())

        if parsed_query:
            print("Query Parseada:", parsed_query)
            
            algebra_relacional = AlgebraRelacional(parsed_query)

            expressao_algebra = algebra_relacional.converter()
            print("Álgebra Relacional:", expressao_algebra)

            detalhamento = algebra_relacional.converter_detalhado()
            print("Detalhamento da Conversão:", detalhamento)
        else:
            print("Falha ao parsear a query.")