class HeuristicaReducaoAtributos:
    def __init__(self, parsed_query: dict):
        self.parsed_original = parsed_query

    def _extrair_colunas_where(self, where_clause: str) -> list:
        colunas = []
        if not where_clause:
            return colunas
        
        for parte in where_clause.replace('(', '').replace(')', '').split():
            if '.' in parte and not any(op in parte for op in ['=', '>', '<', '!', 'LIKE']):
                colunas.append(parte.strip())
        return colunas

    def _extrair_colunas_join(self, inner_joins: list) -> list:
        colunas = []
        for join in inner_joins:
            condicao = join['condicao']
            # Extrair também where_antecipado se existir
            if 'where_antecipado' in join:
                for parte in join['where_antecipado'].replace('(', '').replace(')', '').split():
                    if '.' in parte and not any(op in parte for op in ['=', '>', '<', '!', 'LIKE']):
                        colunas.append(parte.strip())
            
            for parte in condicao.replace('(', '').replace(')', '').split('='):
                parte = parte.strip()
                if '.' in parte:
                    colunas.append(parte)
        return colunas

    def _agrupar_por_tabela(self, colunas: list) -> dict:
        resultado = {}
        for col in colunas:
            if '.' in col:
                tabela, coluna = col.split('.', 1)
                if tabela not in resultado:
                    resultado[tabela] = set()
                resultado[tabela].add(coluna)
        return resultado

    def otimizar(self) -> dict:
        select_cols = self.parsed_original.get('SELECT', [])
        from_table = self.parsed_original.get('FROM', '')
        inner_joins = self.parsed_original.get('INNER_JOIN', [])
        where_clause = self.parsed_original.get('WHERE', None)

        colunas_select = [c for c in select_cols if '.' in c]
        colunas_where = self._extrair_colunas_where(where_clause)
        colunas_join = self._extrair_colunas_join(inner_joins)

        todas_colunas = list(set(colunas_select + colunas_where + colunas_join))
        colunas_por_tabela = self._agrupar_por_tabela(todas_colunas)

        # Adicionar projeções para cada join
        joins_com_projecao = []
        for join in inner_joins:
            tabela = join['tabela']
            join_atualizado = join.copy()
            
            # Adicionar projeção de colunas para esta tabela
            if tabela in colunas_por_tabela:
                join_atualizado['projecao_antecipada'] = list(colunas_por_tabela[tabela])
            
            joins_com_projecao.append(join_atualizado)

        # Manter estrutura compatível com outras heurísticas
        return {
            'SELECT': select_cols,
            'FROM': from_table,
            'INNER_JOIN': joins_com_projecao,
            'WHERE': where_clause,
            '_otimizacao_atributos': {
                'colunas_por_tabela': {t: list(cols) for t, cols in colunas_por_tabela.items()},
                'colunas_select': colunas_select,
                'colunas_where': colunas_where,
                'colunas_join': colunas_join
            }
        }