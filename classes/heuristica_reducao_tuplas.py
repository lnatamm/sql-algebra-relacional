class HeuristicaReducaoTuplas:
    # Constante para o separador AND
    SEPARADOR_AND = ' AND '
    
    def __init__(self, parsed_query: dict):
        self.parsed_original = parsed_query
    
    def _extrair_condicoes_por_tabela(self, where_clause: str) -> dict:
        """Extrai condições do WHERE agrupadas por tabela"""
        condicoes_por_tabela = {}
        
        if not where_clause:
            return condicoes_por_tabela
        
        condicoes = where_clause.split(self.SEPARADOR_AND)
        
        for condicao in condicoes:
            condicao = condicao.strip()
            # Identifica qual tabela está sendo filtrada
            for parte in condicao.split():
                if '.' in parte and not any(op in parte for op in ['=', '>', '<', '!', 'LIKE']):
                    tabela = parte.split('.')[0]
                    if tabela not in condicoes_por_tabela:
                        condicoes_por_tabela[tabela] = []
                    condicoes_por_tabela[tabela].append(condicao)
                    break
        
        return condicoes_por_tabela
    
    def otimizar(self) -> dict:
        """Otimiza a query aplicando seleções o mais cedo possível"""
        select_cols = self.parsed_original.get('SELECT', [])
        from_table = self.parsed_original.get('FROM', '')
        inner_joins = self.parsed_original.get('INNER_JOIN', [])
        where_clause = self.parsed_original.get('WHERE', None)
        
        # Identifica quais condições podem ser aplicadas antecipadamente
        condicoes_por_tabela = self._extrair_condicoes_por_tabela(where_clause)
        
        # Cria nova estrutura de JOINs com seleções antecipadas
        joins_otimizados = []
        condicoes_antecipadas = []  # Rastreia condições que foram antecipadas
        
        for join in inner_joins:
            tabela = join['tabela']
            join_otimizado = {
                'tabela': tabela,
                'condicao': join['condicao']
            }
            
            # Se há condições para esta tabela, adiciona where_antecipado
            if tabela in condicoes_por_tabela:
                join_otimizado['where_antecipado'] = self.SEPARADOR_AND.join(condicoes_por_tabela[tabela])
                condicoes_antecipadas.extend(condicoes_por_tabela[tabela])
            
            joins_otimizados.append(join_otimizado)
        
        # Adiciona condições da tabela FROM às antecipadas
        if from_table in condicoes_por_tabela:
            condicoes_antecipadas.extend(condicoes_por_tabela[from_table])
        
        # Remove do WHERE as condições que foram antecipadas
        where_atualizado = None
        if where_clause:
            condicoes_originais = [c.strip() for c in where_clause.split(self.SEPARADOR_AND)]
            condicoes_restantes = [c for c in condicoes_originais if c not in condicoes_antecipadas]
            if condicoes_restantes:
                where_atualizado = self.SEPARADOR_AND.join(condicoes_restantes)
        
        # Constrói o parsed otimizado mantendo a estrutura padrão
        parsed_otimizado = {
            'SELECT': select_cols,
            'FROM': from_table,
            'INNER_JOIN': joins_otimizados
        }
        
        # Adiciona WHERE somente se houver condições restantes
        if where_atualizado:
            parsed_otimizado['WHERE'] = where_atualizado
        
        # Se a tabela FROM tem condições, adiciona where_antecipado
        if from_table in condicoes_por_tabela:
            parsed_otimizado['FROM_WHERE_ANTECIPADO'] = self.SEPARADOR_AND.join(condicoes_por_tabela[from_table])
        
        return parsed_otimizado