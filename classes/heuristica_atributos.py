class HeuristicaReducaoAtributos:
    def __init__(self, parsed_query: dict):
        self.parsed_original = parsed_query

    def _extrair_colunas_necessarias(self, texto: str) -> list:
        """Extrai todas as colunas (Tabela.Coluna) de um texto"""
        colunas = []
        if not texto:
            return colunas
        
        # Remove parênteses e quebra em palavras
        palavras = texto.replace('(', '').replace(')', '').split()
        
        for palavra in palavras:
            # Se tem ponto e não é um operador, é uma coluna
            if '.' in palavra and not any(op in palavra for op in ['=', '>', '<', '!', 'LIKE']):
                # Remove possíveis vírgulas ou aspas
                coluna = palavra.strip(',').strip("'").strip('"')
                if coluna:
                    colunas.append(coluna)
        
        return colunas

    def _agrupar_por_tabela(self, colunas: list) -> dict:
        """Agrupa colunas por tabela"""
        resultado = {}
        for col in colunas:
            if '.' in col:
                tabela, coluna = col.split('.', 1)
                if tabela not in resultado:
                    resultado[tabela] = set()
                resultado[tabela].add(coluna)
        return resultado

    def otimizar(self) -> dict:
        """Otimiza a query aplicando projeções o mais cedo possível"""
        select_cols = self.parsed_original.get('SELECT', [])
        from_table = self.parsed_original.get('FROM', '')
        inner_joins = self.parsed_original.get('INNER_JOIN', [])
        where_clause = self.parsed_original.get('WHERE', None)
        from_where_antecipado = self.parsed_original.get('FROM_WHERE_ANTECIPADO', None)

        # Coleta todas as colunas necessárias
        todas_colunas = []
        
        # Colunas do SELECT
        for col in select_cols:
            if '.' in col:
                todas_colunas.append(col)
        
        # Colunas do WHERE principal
        todas_colunas.extend(self._extrair_colunas_necessarias(where_clause))
        
        # Colunas do WHERE antecipado do FROM
        todas_colunas.extend(self._extrair_colunas_necessarias(from_where_antecipado))
        
        # Colunas dos JOINs
        for join in inner_joins:
            # Condição do JOIN
            todas_colunas.extend(self._extrair_colunas_necessarias(join['condicao']))
            
            # WHERE antecipado do JOIN
            if 'where_antecipado' in join:
                todas_colunas.extend(self._extrair_colunas_necessarias(join['where_antecipado']))
        
        # Remove duplicatas e agrupa por tabela
        todas_colunas = list(set(todas_colunas))
        colunas_por_tabela = self._agrupar_por_tabela(todas_colunas)

        # Adiciona projeções aos JOINs
        joins_otimizados = []
        for join in inner_joins:
            tabela = join['tabela']
            join_otimizado = {
                'tabela': tabela,
                'condicao': join['condicao']
            }
            
            # Preserva where_antecipado se existir
            if 'where_antecipado' in join:
                join_otimizado['where_antecipado'] = join['where_antecipado']
            
            # Adiciona projeção antecipada se houver colunas para esta tabela
            if tabela in colunas_por_tabela:
                join_otimizado['projecao_antecipada'] = sorted(colunas_por_tabela[tabela])
            
            joins_otimizados.append(join_otimizado)

        # Constrói o resultado mantendo a estrutura padrão
        resultado = {
            'SELECT': select_cols,
            'FROM': from_table,
            'INNER_JOIN': joins_otimizados
        }
        
        # Adiciona WHERE somente se houver valor
        if where_clause:
            resultado['WHERE'] = where_clause
        
        # Preserva FROM_WHERE_ANTECIPADO se existir
        if from_where_antecipado:
            resultado['FROM_WHERE_ANTECIPADO'] = from_where_antecipado
        
        # Adiciona projeção antecipada para FROM se houver
        if from_table in colunas_por_tabela:
            resultado['FROM_PROJECAO_ANTECIPADA'] = sorted(colunas_por_tabela[from_table])
        
        return resultado