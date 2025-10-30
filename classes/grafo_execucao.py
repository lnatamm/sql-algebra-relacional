"""
Gerador de Grafo de Execução para Álgebra Relacional

Este módulo cria representações visuais da árvore de execução
de operações de álgebra relacional.
"""

try:
    import networkx as nx  # type: ignore
    import matplotlib.pyplot as plt  # type: ignore
    NETWORKX_DISPONIVEL = True
except Exception:
    NETWORKX_DISPONIVEL = False


class GrafoExecucao:
    """Classe para gerar grafos de execução de álgebra relacional"""
    
    def __init__(self, parsed_query: dict):
        """
        Inicializa o gerador de grafo
        
        Args:
            parsed_query: Dicionário retornado pelo Parser
        """
        self.parsed = parsed_query
        self.select_cols = parsed_query.get('SELECT', [])
        self.from_table = parsed_query.get('FROM', '')
        self.inner_joins = parsed_query.get('INNER_JOIN', [])
        self.where_clause = parsed_query.get('WHERE', None)

    def gerar_grafo_networkx(self, nome_arquivo: str = 'grafo_networkx.png') -> str:
        """
        Gera uma imagem PNG usando NetworkX + Matplotlib (puro Python, sem binários externos).
        Requer as bibliotecas opcionais `networkx` e `matplotlib`.
        """
        if not NETWORKX_DISPONIVEL:
            raise ImportError("Dependências ausentes. Instale: pip install networkx matplotlib")

        G = nx.DiGraph()

        # Criar nós
        def add_node(nid: str, label: str, tipo: str):
            G.add_node(nid, label=label, tipo=tipo)

        # Criar arestas
        def add_edge(a: str, b: str):
            G.add_edge(a, b)

        nid_counter = 0
        def next_id():
            nonlocal nid_counter
            nid_counter += 1
            return f"n{nid_counter}"

        n_from = next_id()
        add_node(n_from, self.from_table, 'tabela')
        ultimo = n_from
        
        # Adicionar projeção antecipada para a tabela FROM (se existir)
        from_projecao_antecipada = self.parsed.get('FROM_PROJECAO_ANTECIPADA', None)
        if from_projecao_antecipada:
            n_proj_from = next_id()
            cols_proj = ', '.join(from_projecao_antecipada)
            add_node(n_proj_from, f"π {cols_proj}", 'projecao')
            add_edge(ultimo, n_proj_from)
            ultimo = n_proj_from
        
        # Adicionar seleção antecipada para a tabela FROM (se existir)
        from_where_antecipado = self.parsed.get('FROM_WHERE_ANTECIPADO', None)
        if from_where_antecipado:
            n_sel_from = next_id()
            add_node(n_sel_from, f"σ {from_where_antecipado}", 'selecao')
            add_edge(ultimo, n_sel_from)
            ultimo = n_sel_from

        for join in self.inner_joins:
            n_tab = next_id()
            add_node(n_tab, join['tabela'], 'tabela')
            
            # Se tem projecao_antecipada, adiciona nó de projeção
            if 'projecao_antecipada' in join:
                n_proj_antecipada = next_id()
                cols_proj = ', '.join(join['projecao_antecipada'])
                add_node(n_proj_antecipada, f"π {cols_proj}", 'projecao')
                add_edge(n_tab, n_proj_antecipada)
                n_tab = n_proj_antecipada  # Atualiza para usar o nó de projeção
            
            # Se tem where_antecipado, adiciona nó de seleção antes da junção
            if 'where_antecipado' in join:
                n_sel_antecipada = next_id()
                add_node(n_sel_antecipada, f"σ {join['where_antecipado']}", 'selecao')
                add_edge(n_tab, n_sel_antecipada)
                n_tab = n_sel_antecipada  # Atualiza para usar o nó de seleção
            
            n_join = next_id()
            add_node(n_join, f"⋈ {join['condicao']}", 'juncao')
            add_edge(ultimo, n_join)
            add_edge(n_tab, n_join)
            ultimo = n_join

        if self.where_clause:
            n_sel = next_id()
            add_node(n_sel, f"σ {self.where_clause}", 'selecao')
            add_edge(ultimo, n_sel)
            ultimo = n_sel

        if self.select_cols != ['*']:
            cols = ', '.join(self.select_cols)
            n_proj = next_id()
            add_node(n_proj, f"π {cols}", 'projecao')
            add_edge(ultimo, n_proj)
            ultimo = n_proj

        # Layout simples (spring)
        pos = nx.spring_layout(G, seed=42)

        # Cores por tipo
        color_map = {
            'tabela': '#cfe8ff',
            'juncao': '#f4cccc',
            'selecao': '#fff2cc',
            'projecao': '#d9ead3',
        }
        node_colors = [color_map.get(G.nodes[n].get('tipo', ''), '#ffffff') for n in G.nodes]
        labels = {n: G.nodes[n].get('label', n) for n in G.nodes}

        plt.figure(figsize=(10, 8))
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500, edgecolors='#666')
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=15, edge_color='#888')
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        plt.axis('off')

        try:
            plt.tight_layout()
            plt.savefig(nome_arquivo, dpi=180)
            plt.close()
        except Exception as e:
            plt.close()
            raise Exception(f"Erro ao salvar imagem NetworkX: {e}")

        import os
        return os.path.abspath(nome_arquivo)
