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
        inner_joins = self.parsed_original.get('INNER_JOIN', [])
        where_clause = self.parsed_original.get('WHERE', None)

        colunas_select = [c for c in select_cols if '.' in c]
        colunas_where = self._extrair_colunas_where(where_clause)
        colunas_join = self._extrair_colunas_join(inner_joins)

        todas_colunas = list(set(colunas_select + colunas_where + colunas_join))

        colunas_por_tabela = self._agrupar_por_tabela(todas_colunas)

        return {
            'projecoes_otimizadas': {t: list(cols) for t, cols in colunas_por_tabela.items()},
            '_detalhes': {
                'colunas_select': colunas_select,
                'colunas_where': colunas_where,
                'colunas_join': colunas_join
            }
        }