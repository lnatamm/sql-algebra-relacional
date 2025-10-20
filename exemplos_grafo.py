"""
Exemplo de uso isolado do Gerador de Grafos de Execução

Este arquivo demonstra como usar a classe GrafoExecucao de forma independente.
"""

from classes.parser import Parser
from classes.grafo_execucao import GrafoExecucao

def exemplo_simples():
    """Exemplo com query simples"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Query Simples")
    print("=" * 80)
    
    query = "SELECT nome, email FROM usuarios WHERE ativo = true;"
    print(f"Query: {query}\n")
    
    # Parsear a query
    parsed = Parser().parse(query.upper())
    
    if parsed:
        # Criar gerador de grafo
        gerador = GrafoExecucao(parsed)
        
        # Exibir árvore ASCII
        print(gerador.gerar_ascii_tree())

        # Tentar uma visualização bonita no terminal (Rich)
        print("\nVisualização Rich (se disponível):")
        try:
            gerador.renderizar_rich_tree()
        except ImportError as e:
            print(f"  ⚠️  {e}")
        
        # Exibir ordem de execução
        print("\nOrdem de Execução Detalhada:")
        for i, (op, desc) in enumerate(gerador.gerar_ordem_execucao(), 1):
            print(f"  Passo {i}: [{op}] {desc}")


def exemplo_com_joins():
    """Exemplo com múltiplas junções"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Query com Múltiplas Junções")
    print("=" * 80)
    
    query = """
    SELECT p.nome, d.nome, c.nome 
    FROM pessoas p 
    INNER JOIN departamentos d ON p.dept_id = d.id 
    INNER JOIN cidades c ON p.cidade_id = c.id 
    WHERE p.salario > 5000;
    """
    print(f"Query: {query}\n")
    
    # Parsear a query
    parsed = Parser().parse(query.upper())
    
    if parsed:
        # Criar gerador de grafo
        gerador = GrafoExecucao(parsed)

        # Exibir árvore ASCII
        print(gerador.gerar_ascii_tree())

        # Exportar como Mermaid (sem dependências)
        print("\nMermaid (cola isso em Markdown com bloco ```mermaid):")
        mermaid = gerador.gerar_mermaid(direcao='BT', incluir_legenda=True)
        print(mermaid)

        # Exibir estatísticas
        print("\nEstatísticas da Query:")
        stats = gerador.exibir_estatisticas()
        print(f"  • Número de tabelas: {stats['numero_tabelas']}")
        print(f"  • Número de junções: {stats['numero_juncoes']}")
        print(f"  • Possui filtro WHERE: {stats['tem_filtro']}")
        print(f"  • Número de colunas na projeção: {stats['numero_colunas_projecao']}")


def exemplo_geracao_arquivo():
    """Exemplo de geração de arquivo de grafo visual"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Geração de Arquivo Visual")
    print("=" * 80)
    
    query = "SELECT nome, idade FROM clientes WHERE idade >= 18;"
    print(f"Query: {query}\n")
    
    # Parsear a query
    parsed = Parser().parse(query.upper())
    
    if parsed:
        # Criar gerador de grafo
        gerador = GrafoExecucao(parsed)
        
        # Tentar gerar grafo visual
        try:
            print("Tentando gerar grafo visual...")
            output = gerador.gerar_grafo(formato='png', nome_arquivo='exemplo_grafo')
            print(f"✅ Sucesso! Arquivo gerado: {output}")
            print("\nVocê pode abrir o arquivo PNG gerado para visualizar o grafo.")
        except ImportError as e:
            print(f"⚠️  {e}")
            print("\nPara gerar grafos visuais, instale o graphviz:")
            print("  1. pip install graphviz")
            print("  2. Instale o executável: https://graphviz.org/download/")
            
            # Alternativa: NetworkX + Matplotlib (puro Python)
            print("\nAlternativa (sem executável externo): NetworkX + Matplotlib")
            try:
                output2 = gerador.gerar_grafo_networkx('exemplo_grafo_networkx.png')
                print(f"✅ Gerado com NetworkX: {output2}")
            except ImportError as e2:
                print(f"⚠️  {e2}")
            except Exception as e2:
                print(f"❌ Erro NetworkX: {e2}")
        except Exception as e:
            print(f"❌ Erro: {e}")


def exemplo_comparacao_queries():
    """Compara estatísticas de diferentes queries"""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: Comparação de Complexidade de Queries")
    print("=" * 80)
    
    queries = [
        "SELECT * FROM usuarios;",
        "SELECT nome FROM usuarios WHERE ativo = true;",
        "SELECT u.nome, p.titulo FROM usuarios u INNER JOIN posts p ON u.id = p.user_id;",
        "SELECT u.nome, p.titulo, c.texto FROM usuarios u INNER JOIN posts p ON u.id = p.user_id INNER JOIN comentarios c ON p.id = c.post_id WHERE u.ativo = true;",
    ]
    
    print("\nComparando complexidade das queries:\n")
    
    for i, query in enumerate(queries, 1):
        parsed = Parser().parse(query.upper())
        if parsed:
            gerador = GrafoExecucao(parsed)
            stats = gerador.exibir_estatisticas()
            
            print(f"Query {i}:")
            print(f"  SQL: {query[:60]}...")
            print(f"  Tabelas: {stats['numero_tabelas']}, Junções: {stats['numero_juncoes']}, "
                  f"Filtros: {stats['tem_filtro']}, Colunas: {stats['numero_colunas_projecao']}")
            print()


def exemplo_personalizado():
    """Permite entrada personalizada do usuário"""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: Query Personalizada")
    print("=" * 80)
    
    print("\nDigite sua query SQL (ou pressione Enter para usar um exemplo):")
    query = input("> ").strip()
    
    if not query:
        query = "SELECT nome, email FROM usuarios WHERE status = 'ativo';"
        print(f"Usando exemplo: {query}")
    
    # Garantir que termina com ponto e vírgula
    if not query.endswith(";"):
        query += ";"
    
    # Parsear a query
    parsed = Parser().parse(query.upper())
    
    if parsed:
        # Criar gerador de grafo
        gerador = GrafoExecucao(parsed)
        
        # Exibir tudo
        print(gerador.gerar_ascii_tree())
        
        print("\nOrdem de Execução:")
        for i, (op, desc) in enumerate(gerador.gerar_ordem_execucao(), 1):
            print(f"  {i}. [{op}] {desc}")
        
        print("\nEstatísticas:")
        for chave, valor in gerador.exibir_estatisticas().items():
            print(f"  • {chave}: {valor}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("EXEMPLOS DE USO DO GERADOR DE GRAFOS DE EXECUÇÃO")
    print("=" * 80)
    
    # Executar todos os exemplos
    exemplo_simples()
    exemplo_com_joins()
    exemplo_geracao_arquivo()
    exemplo_comparacao_queries()
    
    # Exemplo interativo (comentado por padrão)
    # exemplo_personalizado()
    
    print("\n" + "=" * 80)
    print("FIM DOS EXEMPLOS")
    print("=" * 80)
    print("\nDica: Para executar o exemplo personalizado, descomente a linha")
    print("'exemplo_personalizado()' no final deste arquivo.\n")
