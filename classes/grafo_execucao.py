"""
Gerador de Grafo de Execução para Álgebra Relacional

Este módulo cria representações visuais da árvore de execução
de operações de álgebra relacional.
"""

try:
    from graphviz import Digraph
    GRAPHVIZ_DISPONIVEL = True
except ImportError:
    GRAPHVIZ_DISPONIVEL = False
    print("⚠️  Aviso: graphviz não está instalado. Execute: pip install graphviz")

# Backends alternativos (opcionais)
try:
    from rich.tree import Tree
    from rich.console import Console
    RICH_DISPONIVEL = True
except ImportError:
    RICH_DISPONIVEL = False

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
        self.node_counter = 0
    
    def _get_next_node_id(self) -> str:
        """Retorna o próximo ID de nó"""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def _criar_no_tabela(self, graph: 'Digraph', tabela: str) -> str:
        """
        Cria um nó para uma tabela base
        
        Args:
            graph: Objeto Digraph do graphviz
            tabela: Nome da tabela
        
        Returns:
            ID do nó criado
        """
        node_id = self._get_next_node_id()
        graph.node(node_id, tabela, shape='box', style='filled', fillcolor='lightblue')
        return node_id
    
    def _criar_no_operacao(self, graph: 'Digraph', operacao: str, label: str) -> str:
        """
        Cria um nó para uma operação de álgebra relacional
        
        Args:
            graph: Objeto Digraph do graphviz
            operacao: Símbolo da operação (σ, π, ⋈, etc)
            label: Descrição da operação
        
        Returns:
            ID do nó criado
        """
        node_id = self._get_next_node_id()
        
        # Cores diferentes para cada tipo de operação
        cores = {
            'π': ('lightgreen', 'Projeção'),
            'σ': ('lightyellow', 'Seleção'),
            '⋈': ('lightcoral', 'Junção'),
            '×': ('lightgray', 'Produto Cartesiano')
        }
        
        cor, tipo = cores.get(operacao, ('white', 'Operação'))
        node_label = f"{operacao}\n{label}"
        
        graph.node(node_id, node_label, shape='ellipse', style='filled', fillcolor=cor)
        return node_id
    
    def gerar_grafo(self, formato: str = 'png', nome_arquivo: str = 'grafo_execucao') -> str:
        """
        Gera o grafo de execução da álgebra relacional
        
        Args:
            formato: Formato do arquivo de saída (png, pdf, svg, etc)
            nome_arquivo: Nome do arquivo sem extensão
        
        Returns:
            Caminho do arquivo gerado
        """
        if not GRAPHVIZ_DISPONIVEL:
            raise ImportError("A biblioteca graphviz não está instalada. Execute: pip install graphviz")
        
        # Verifica se o executável do Graphviz está disponível
        import shutil
        if shutil.which('dot') is None:
            raise EnvironmentError(
                "O executável 'dot' do Graphviz não foi encontrado no PATH.\n"
                "Instale o Graphviz:\n"
                "  Windows: https://graphviz.org/download/ (marque 'Add to PATH')\n"
                "  Após instalar, reinicie o terminal/VSCode.\n"
                "  Ou adicione manualmente: C:\\Program Files\\Graphviz\\bin ao PATH"
            )
        
    # Cria o grafo direcionado
        graph = Digraph(comment='Grafo de Execução - Álgebra Relacional')
        graph.attr(rankdir='BT')  # Bottom to Top (das folhas para a raiz)
        graph.attr('node', fontname='Arial')
        
        # Passo 1: Criar nós para as tabelas base
        no_from = self._criar_no_tabela(graph, self.from_table)
        ultimo_no = no_from
        
        # Passo 2: Criar nós para INNER JOINs
        for join in self.inner_joins:
            # Cria nó para a tabela do join
            no_tabela_join = self._criar_no_tabela(graph, join['tabela'])
            
            # Cria nó para a operação de junção
            condicao = join['condicao']
            no_juncao = self._criar_no_operacao(graph, '⋈', condicao)
            
            # Conecta a tabela anterior e a nova tabela ao nó de junção
            graph.edge(ultimo_no, no_juncao)
            graph.edge(no_tabela_join, no_juncao)
            
            ultimo_no = no_juncao
        
        # Passo 3: Aplicar seleção (WHERE) se existir
        if self.where_clause:
            no_selecao = self._criar_no_operacao(graph, 'σ', self.where_clause)
            graph.edge(ultimo_no, no_selecao)
            ultimo_no = no_selecao
        
        # Passo 4: Aplicar projeção (SELECT)
        if self.select_cols != ['*']:
            colunas = ', '.join(self.select_cols)
            no_projecao = self._criar_no_operacao(graph, 'π', colunas)
            graph.edge(ultimo_no, no_projecao)
            ultimo_no = no_projecao
        
        # Adiciona legenda
        with graph.subgraph(name='cluster_legend') as legend:
            legend.attr(label='Legenda', style='filled', color='lightgrey')
            legend.node('leg_table', 'Tabela', shape='box', style='filled', fillcolor='lightblue')
            legend.node('leg_proj', 'π - Projeção', shape='ellipse', style='filled', fillcolor='lightgreen')
            legend.node('leg_sel', 'σ - Seleção', shape='ellipse', style='filled', fillcolor='lightyellow')
            legend.node('leg_join', '⋈ - Junção', shape='ellipse', style='filled', fillcolor='lightcoral')
        
        # Renderiza o grafo
        try:
            output_path = graph.render(nome_arquivo, format=formato, cleanup=True)
            return output_path
        except Exception as e:
            raise Exception(f"Erro ao gerar o grafo: {str(e)}")

    # =========================
    # BACKENDS ALTERNATIVOS
    # =========================

    def gerar_mermaid(self, direcao: str = 'TB', incluir_legenda: bool = True, arquivo: str | None = None) -> str:
        """
        Gera o diagrama em formato Mermaid (flowchart) sem dependências externas.

        Args:
            direcao: Direção do fluxo (TB, BT, LR, RL)
            incluir_legenda: Inclui subgrafo de legenda
            arquivo: Se informado, escreve o conteúdo em arquivo (.md ou .mmd)

        Returns:
            String com o conteúdo Mermaid
        """
        linhas: list[str] = []
        linhas.append(f"flowchart {direcao}")

        node_ids: list[str] = []
        estilos: list[tuple[str, str]] = []  # (node_id, estilo)

        def add_node(node_id: str, label: str, tipo: str):
            linhas.append(f"  {node_id}[\"{label}\"]")
            # cores: tabela azul, junção vermelha, seleção amarela, projeção verde
            cores = {
                'tabela': '#cfe8ff',
                'juncao': '#f4cccc',
                'selecao': '#fff2cc',
                'projecao': '#d9ead3'
            }
            cor = cores.get(tipo, '#ffffff')
            estilos.append((node_id, f"fill:{cor},stroke:#666,stroke-width:1px"))
            node_ids.append(node_id)

        def add_edge(a: str, b: str):
            linhas.append(f"  {a} --> {b}")

        # Tabelas e junções
        nid_counter = 0
        def next_id():
            nonlocal nid_counter
            nid_counter += 1
            return f"n{nid_counter}"

        n_from = next_id()
        add_node(n_from, self.from_table, 'tabela')
        ultimo = n_from

        for join in self.inner_joins:
            n_tab = next_id()
            add_node(n_tab, join['tabela'], 'tabela')
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

        # Estilos
        linhas.append("")
        for nid, estilo in estilos:
            linhas.append(f"  style {nid} {estilo}")

        # Legenda
        if incluir_legenda:
            linhas.extend([
                "",
                "  subgraph Legend",
                "    direction TB",
                "    l1[\"Tabela\"]",
                "    l2[\"π Projeção\"]",
                "    l3[\"σ Seleção\"]",
                "    l4[\"⋈ Junção\"]",
                "  end",
                "  style l1 fill:#cfe8ff,stroke:#666,stroke-width:1px",
                "  style l2 fill:#d9ead3,stroke:#666,stroke-width:1px",
                "  style l3 fill:#fff2cc,stroke:#666,stroke-width:1px",
                "  style l4 fill:#f4cccc,stroke:#666,stroke-width:1px",
            ])

        conteudo = "\n".join(linhas)

        if arquivo:
            try:
                import os
                wrap_md = arquivo.lower().endswith('.md')
                with open(arquivo, 'w', encoding='utf-8') as f:
                    if wrap_md:
                        f.write("```mermaid\n")
                        f.write(conteudo)
                        f.write("\n````\n" if False else "\n```\n")
                    else:
                        f.write(conteudo)
                return os.path.abspath(arquivo)
            except Exception as e:
                raise Exception(f"Não foi possível escrever o arquivo Mermaid: {e}")

        return conteudo

    def renderizar_rich_tree(self) -> bool:
        """
        Renderiza uma árvore de execução colorida no terminal usando Rich.
        Retorna True se renderizou com sucesso. Caso Rich não esteja instalado,
        levanta ImportError com instruções de instalação.
        """
        if not RICH_DISPONIVEL:
            raise ImportError("Rich não está instalado. Execute: pip install rich")

        raiz = Tree(f"[bold blue]📊 {self.from_table}")

        atual = raiz
        for join in self.inner_joins:
            atual.add(f"[bold blue]📊 {join['tabela']}")
            atual.add("│")
            atual.add(f"[bold red]⋈ Junção: {join['condicao']}")
            atual.add("│")

        if self.where_clause:
            atual.add(f"[bold yellow]σ Seleção: {self.where_clause}")
            atual.add("│")

        if self.select_cols == ['*']:
            atual.add(f"[bold green]π Projeção: * (todas as colunas)")
        else:
            cols = ', '.join(self.select_cols)
            atual.add(f"[bold green]π Projeção: {cols}")

        Console().print(raiz)
        return True

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
    
    def gerar_ascii_tree(self) -> str:
        """
        Gera uma representação em ASCII da árvore de execução
        
        Returns:
            String com a árvore em formato ASCII
        """
        linhas = []
        linhas.append("Árvore de Execução (bottom-up):")
        linhas.append("=" * 60)
        
        nivel = 0
        indent = "  "
        
        # Nível 0: Tabelas base
        linhas.append(f"{indent * nivel}📊 {self.from_table}")
        
        # Junções
        for i, join in enumerate(self.inner_joins):
            nivel += 1
            linhas.append(f"{indent * nivel}📊 {join['tabela']}")
            linhas.append(f"{indent * nivel}  │")
            linhas.append(f"{indent * nivel}  ├─ ⋈ Junção: {join['condicao']}")
            linhas.append(f"{indent * nivel}  │")
        
        # Seleção (WHERE)
        if self.where_clause:
            nivel += 1
            linhas.append(f"{indent * nivel}σ Seleção: {self.where_clause}")
            linhas.append(f"{indent * nivel}│")
        
        # Projeção (SELECT)
        if self.select_cols != ['*']:
            nivel += 1
            colunas = ', '.join(self.select_cols)
            linhas.append(f"{indent * nivel}π Projeção: {colunas}")
        else:
            nivel += 1
            linhas.append(f"{indent * nivel}π Projeção: * (todas as colunas)")
        
        linhas.append("=" * 60)
        linhas.append("↑ Resultado Final")
        
        return '\n'.join(linhas)
    
    def gerar_ordem_execucao(self) -> list:
        """
        Gera a ordem de execução das operações
        
        Returns:
            Lista de tuplas (operação, descrição)
        """
        ordem = []
        
        # 1. Scan das tabelas
        ordem.append(('SCAN', f'Tabela: {self.from_table}'))
        
        for join in self.inner_joins:
            ordem.append(('SCAN', f'Tabela: {join["tabela"]}'))
            ordem.append(('JOIN', f'Junção: {join["condicao"]}'))
        
        # 2. Seleção (WHERE)
        if self.where_clause:
            ordem.append(('SELECT', f'Filtro: {self.where_clause}'))
        
        # 3. Projeção (SELECT)
        if self.select_cols == ['*']:
            ordem.append(('PROJECT', 'Projeção: * (todas as colunas)'))
        else:
            colunas = ', '.join(self.select_cols)
            ordem.append(('PROJECT', f'Projeção: {colunas}'))
        
        return ordem
    
    def exibir_estatisticas(self) -> dict:
        """
        Retorna estatísticas sobre a query
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            'numero_tabelas': 1 + len(self.inner_joins),
            'numero_juncoes': len(self.inner_joins),
            'tem_filtro': self.where_clause is not None,
            'numero_colunas_projecao': len(self.select_cols),
            'eh_select_all': self.select_cols == ['*']
        }


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo do parser fornecido
    parsed = {
        'SELECT': ['ALUNOS.NOME', 'CURSOS.NOME', 'PROFESSORES.NOME'],
        'FROM': 'ALUNOS',
        'INNER_JOIN': [
            {'tabela': 'CURSOS', 'condicao': 'ALUNOS.CURSO_ID = CURSOS.ID'},
            {'tabela': 'PROFESSORES', 'condicao': 'CURSOS.PROFESSOR_ID = PROFESSORES.ID'}
        ],
        'WHERE': "CURSOS.NOME = 'BANCO DE DADOS'"
    }
    
    gerador = GrafoExecucao(parsed)
    
    print("\n" + "=" * 80)
    print("GRAFO DE EXECUÇÃO - ÁLGEBRA RELACIONAL")
    print("=" * 80)
    
    # Exibe árvore ASCII
    print("\n" + gerador.gerar_ascii_tree())
    
    # Exibe ordem de execução
    print("\n" + "=" * 80)
    print("ORDEM DE EXECUÇÃO:")
    print("=" * 80)
    ordem = gerador.gerar_ordem_execucao()
    for i, (op, desc) in enumerate(ordem, 1):
        print(f"{i}. [{op:8}] {desc}")
    
    # Exibe estatísticas
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DA QUERY:")
    print("=" * 80)
    stats = gerador.exibir_estatisticas()
    for chave, valor in stats.items():
        print(f"  {chave}: {valor}")
    
    # Tenta gerar o grafo visual
    if GRAPHVIZ_DISPONIVEL:
        print("\n" + "=" * 80)
        print("GERANDO GRAFO VISUAL...")
        print("=" * 80)
        try:
            output = gerador.gerar_grafo()
            print(f"✅ Grafo gerado com sucesso: {output}")
        except Exception as e:
            print(f"❌ Erro ao gerar grafo: {e}")
    else:
        print("\n⚠️  Para gerar grafos visuais, instale: pip install graphviz")
    
    print("\n" + "=" * 80)
