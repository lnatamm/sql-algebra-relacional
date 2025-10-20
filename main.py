from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao

if __name__ == "__main__":
    queries = [
        "SELECT Alunos.nome, Cursos.nome, Professores.nome FROM Alunos INNER JOIN Cursos ON Alunos.curso_id = Cursos.id INNER JOIN Professores ON Cursos.professor_id = Professores.id WHERE Cursos.nome = 'Banco de Dados';",
        "SELECT * FROM teste WHERE idade >= 18;",
        "SELECT nome, idade FROM Pessoa;",
    ]
    
    for idx, query in enumerate(queries, 1):
        print("\n" + "=" * 80)
        print(f"QUERY {idx}")
        print("=" * 80)
        print("Query SQL:", query)

        parsed_query = Parser().parse(query.upper())

        if parsed_query:
            print("\nQuery Parseada:", parsed_query)
            
            # Álgebra Relacional
            algebra_relacional = AlgebraRelacional(parsed_query)
            expressao_algebra = algebra_relacional.converter()
            print("\nÁlgebra Relacional:", expressao_algebra)

            detalhamento = algebra_relacional.converter_detalhado()
            print("\nDetalhamento da Conversão:", detalhamento)
            
            # Gerar Grafo de Execução
            print("\n" + "-" * 80)
            print("GRAFO DE EXECUÇÃO")
            print("-" * 80)
            
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
            try:
                nome_arquivo = f"grafo_query_{idx}"
                output = gerador_grafo.gerar_grafo(formato='png', nome_arquivo=nome_arquivo)
                gerador_grafo.gerar_mermaid(direcao='TB', incluir_legenda=True)
                gerador_grafo.gerar_grafo_networkx(nome_arquivo=f"networkx_query_{idx}.png")
                print(f"\n✅ Grafo visual gerado: {output}")
            except ImportError as e:
                print(f"\n⚠️  {e}")
            except Exception as e:
                print(f"\n❌ Erro ao gerar grafo visual: {e}")
        else:
            print("❌ Falha ao parsear a query.")
        
        print("\n" + "=" * 80)