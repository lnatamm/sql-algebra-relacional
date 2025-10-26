class HeuristicaReducaoTuplas:
    def __init__(self, parsed_query: dict):
        self.parsed_original = parsed_query
    
    def _extrair_condicoes_por_tabela(self, where_clause: str) -> dict:
        condicoes_por_tabela = {}
        
        if not where_clause:
            return condicoes_por_tabela
        
        condicoes = where_clause.split(' AND ')
        
        for condicao in condicoes:
            condicao = condicao.strip()
            for parte in condicao.split():
                if '.' in parte and not any(op in parte for op in ['=', '>', '<', '!', 'LIKE']):
                    tabela = parte.split('.')[0]
                    if tabela not in condicoes_por_tabela:
                        condicoes_por_tabela[tabela] = []
                    condicoes_por_tabela[tabela].append(condicao)
                    break
        
        return condicoes_por_tabela
    
    def _extrair_colunas_por_tabela(self, select_cols: list) -> dict:
        colunas_por_tabela = {}
        
        if select_cols == ['*']:
            return colunas_por_tabela
        
        for col in select_cols:
            if '.' in col:
                tabela, coluna = col.split('.', 1)
                if tabela not in colunas_por_tabela:
                    colunas_por_tabela[tabela] = []
                colunas_por_tabela[tabela].append(coluna)
        
        return colunas_por_tabela
    
    def _adicionar_colunas_join(self, colunas_por_tabela: dict, inner_joins: list) -> dict:
        resultado = colunas_por_tabela.copy()
        
        for join in inner_joins:
            condicao = join['condicao']
            partes = condicao.split('=')
            for parte in partes:
                parte = parte.strip()
                if '.' in parte:
                    tabela, coluna = parte.split('.', 1)
                    coluna = coluna.strip()
                    if tabela not in resultado:
                        resultado[tabela] = []
                    if coluna not in resultado[tabela]:
                        resultado[tabela].append(coluna)
        
        return resultado
    
    def otimizar(self) -> dict:
        select_cols = self.parsed_original.get('SELECT', [])
        from_table = self.parsed_original.get('FROM', '')
        inner_joins = self.parsed_original.get('INNER_JOIN', [])
        where_clause = self.parsed_original.get('WHERE', None)
        
        condicoes_por_tabela = self._extrair_condicoes_por_tabela(where_clause)
        colunas_por_tabela = self._extrair_colunas_por_tabela(select_cols)
        colunas_por_tabela = self._adicionar_colunas_join(colunas_por_tabela, inner_joins)
        
        from_otimizado = from_table
        where_from = None
        if from_table in condicoes_por_tabela:
            where_from = ' AND '.join(condicoes_por_tabela[from_table])
        
        joins_otimizados = []
        for join in inner_joins:
            tabela = join['tabela']
            condicao_join = join['condicao']
            
            if tabela in condicoes_por_tabela:
                join_otimizado = {
                    'tabela': tabela,
                    'condicao': condicao_join,
                    'where_antecipado': ' AND '.join(condicoes_por_tabela[tabela])
                }
            else:
                join_otimizado = join.copy()
            
            joins_otimizados.append(join_otimizado)
        
        parsed_otimizado = {
            'SELECT': select_cols,
            'FROM': from_otimizado,
            'INNER_JOIN': joins_otimizados,
            'WHERE': where_from,
            '_otimizacao': {
                'condicoes_por_tabela': condicoes_por_tabela,
                'colunas_por_tabela': colunas_por_tabela
            }
        }
        
        return parsed_otimizado