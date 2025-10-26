"""
Otimizador de Consultas - Heurística de Redução de Tuplas

Implementa 3 heurísticas simples:
1. Seleção precoce: Move WHERE para antes das junções
2. Projeção precoce: Remove colunas desnecessárias cedo
3. Junções restritivas primeiro: Ordena junções por tamanho estimado
"""


class HeuristicaReducaoTuplas:
    """Otimizador simples de consultas usando heurísticas de redução de tuplas."""
    
    def __init__(self, parsed_query: dict, estatisticas: dict = None):
        self.parsed = parsed_query
        self.estatisticas = estatisticas or {}
    
    def otimizar(self) -> dict:
        """Aplica as 3 heurísticas e retorna o plano otimizado."""
        
        # 1. Separar condições WHERE por tabela
        condicoes = self._separar_where()
        
        # 2. Identificar colunas necessárias
        colunas = self._colunas_necessarias()
        
        # 3. Reordenar junções
        joins_ordenados = self._ordenar_joins()
        
        # Criar parsed_query otimizado (para o grafo usar)
        parsed_otimizado = self._criar_parsed_otimizado(condicoes, joins_ordenados)
        
        return {
            'algebra_otimizada': self._gerar_algebra(condicoes, colunas, joins_ordenados),
            'explicacao': self._gerar_explicacao(condicoes, colunas, joins_ordenados),
            'query_otimizada': parsed_otimizado,
            'condicoes_por_tabela': condicoes,
            'colunas_necessarias': colunas
        }
    
    def _separar_where(self) -> dict:
        """Separa WHERE em condições por tabela."""
        where = self.parsed.get('WHERE', '')
        if not where:
            return {}
        
        condicoes = {}
        todas_tabelas = {self.parsed['FROM']} | {j['tabela'] for j in self.parsed.get('INNER_JOIN', [])}
        
        for condicao in where.split('AND'):
            condicao = condicao.strip()
            for tabela in todas_tabelas:
                if tabela in condicao:
                    condicoes.setdefault(tabela, []).append(condicao)
                    break
        
        return condicoes
    
    def _colunas_necessarias(self) -> dict:
        """Identifica colunas necessárias por tabela."""
        colunas = {}
        
        # Colunas do SELECT
        for col in self.parsed.get('SELECT', []):
            if '.' in col:
                tabela, coluna = col.split('.', 1)
                colunas.setdefault(tabela, []).append(coluna)
        
        return colunas
    
    def _ordenar_joins(self) -> list:
        """Ordena junções por tamanho estimado (menor primeiro)."""
        joins = self.parsed.get('INNER_JOIN', []).copy()
        
        if len(joins) > 1:
            joins.sort(key=lambda j: self.estatisticas.get(j['tabela'], {}).get('num_tuplas', 1000))
        
        return joins
    
    def _criar_parsed_otimizado(self, condicoes: dict, joins: list) -> dict:
        """Cria um parsed_query modificado refletindo as otimizações."""
        # Copia a estrutura original
        otimizado = {
            'SELECT': self.parsed.get('SELECT', []),
            'FROM': self.parsed.get('FROM', ''),
            'INNER_JOIN': joins,  # Joins reordenados
            'WHERE': None  # Será removido pois aplicamos seleção precoce
        }
        
        # Se não houver condições aplicadas, mantém WHERE original
        if not condicoes:
            otimizado['WHERE'] = self.parsed.get('WHERE')
        
        return otimizado
    
    def _gerar_algebra(self, condicoes: dict, colunas: dict, joins: list) -> str:
        """Gera expressão de álgebra relacional otimizada."""
        from_table = self.parsed['FROM']
        
        # Tabela inicial com filtro PRECOCE
        expr = from_table
        if from_table in condicoes:
            filtro = ' AND '.join(condicoes[from_table])
            expr = f"σ_{{{filtro}}}({expr})"
        
        # Projeção precoce
        if from_table in colunas:
            cols = ', '.join(colunas[from_table])
            expr = f"π_{{{cols}}}({expr})"
        
        # Junções REORDENADAS
        for join in joins:
            tabela = join['tabela']
            expr_tabela = tabela
            
            # Seleção PRECOCE em cada tabela
            if tabela in condicoes:
                filtro = ' AND '.join(condicoes[tabela])
                expr_tabela = f"σ_{{{filtro}}}({expr_tabela})"
            
            # Projeção PRECOCE em cada tabela
            if tabela in colunas:
                cols = ', '.join(colunas[tabela])
                expr_tabela = f"π_{{{cols}}}({expr_tabela})"
            
            expr = f"({expr} ⋈_{{{join['condicao']}}} {expr_tabela})"
        
        # Projeção final
        select_cols = self.parsed.get('SELECT', [])
        if select_cols != ['*']:
            cols = ', '.join(select_cols)
            expr = f"π_{{{cols}}}({expr})"
        
        return expr
    
    def _gerar_explicacao(self, condicoes: dict, colunas: dict, joins: list) -> list:
        """Gera lista de otimizações aplicadas."""
        explicacao = []
        
        if condicoes:
            explicacao.append("✓ Heurística 1: Seleção precoce aplicada (filtros movidos para ANTES das junções)")
            for tab, conds in condicoes.items():
                explicacao.append(f"  → Filtro aplicado em {tab} antes da junção: {' AND '.join(conds)}")
        
        if colunas:
            explicacao.append("✓ Heurística 2: Projeção precoce aplicada (colunas desnecessárias removidas cedo)")
            for tab, cols in colunas.items():
                explicacao.append(f"  → Apenas colunas necessárias de {tab}: {', '.join(cols)}")
        
        if len(joins) > 1:
            original_order = [j['tabela'] for j in self.parsed.get('INNER_JOIN', [])]
            new_order = [j['tabela'] for j in joins]
            
            if original_order != new_order:
                explicacao.append("✓ Heurística 3: Junções reordenadas (mais seletivas primeiro)")
                explicacao.append(f"  → Ordem original: {' → '.join(original_order)}")
                explicacao.append(f"  → Ordem otimizada: {' → '.join(new_order)}")
            else:
                explicacao.append("✓ Heurística 3: Ordem de junções já está ótima")
        
        if not explicacao:
            explicacao.append("ℹ️ Nenhuma otimização aplicável para esta query")
        
        return explicacao
    
    def imprimir_resultado(self):
        """Imprime resultado de forma formatada."""
        resultado = self.otimizar()
        
        print("\n" + "=" * 70)
        print("OTIMIZAÇÃO - HEURÍSTICA DE REDUÇÃO DE TUPLAS")
        print("=" * 70)
        
        print("\n💡 Otimizações Aplicadas:")
        for exp in resultado['explicacao']:
            print(f"  {exp}")
        
        print("\n📊 Álgebra Relacional Otimizada:")
        print(f"  {resultado['algebra_otimizada']}")
        
        print("\n" + "=" * 70)


# Exemplo de uso
if __name__ == "__main__":
    parsed = {
        'SELECT': ['ALUNOS.NOME', 'CURSOS.NOME'],
        'FROM': 'ALUNOS',
        'INNER_JOIN': [
            {'tabela': 'CURSOS', 'condicao': 'ALUNOS.CURSO_ID = CURSOS.ID'}
        ],
        'WHERE': "ALUNOS.IDADE > 18 AND CURSOS.NOME = 'BD'"
    }
    
    estatisticas = {
        'ALUNOS': {'num_tuplas': 10000},
        'CURSOS': {'num_tuplas': 50}
    }
    
    otimizador = HeuristicaReducaoTuplas(parsed, estatisticas)
    otimizador.imprimir_resultado()
