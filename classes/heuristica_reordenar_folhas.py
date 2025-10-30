class HeuristicaReordenarFolhas:
    """
    Heurística simples para reordenar os nós folha (tabelas base/join) da
    árvore de consulta. A ideia é priorizar (colocar mais cedo na lista de
    INNER_JOIN) as tabelas que aparentam ser mais seletivas, com base em:

    - presença de condições antecipadas ('where_antecipado')
    - número de condições (separadas por 'AND') para cada tabela
    - presença de projeção antecipada ('projecao_antecipada')
    - menções da tabela nas condições globais (WHERE ou FROM_WHERE_ANTECIPADO)

    Observação: esta é uma heurística leve e segura para junções internas (INNER JOIN).
    Não altera a semântica das junções internas, apenas redefine a ordem das
    operações de junção para favorecer scans/filtragens mais seletivas primeiro.
    """

    SEPARADOR_AND = ' AND '

    def __init__(self, parsed_query: dict):
        self.parsed_original = parsed_query or {}

    def _contar_condicoes(self, texto: str) -> int:
        if not texto:
            return 0
        return len([c for c in texto.split(self.SEPARADOR_AND) if c.strip()])

    def _score_para_join(self, join: dict, where_global: str, from_where_antecipado: str) -> int:
        """Calcula uma pontuação simples para um join com base em sinais de seletividade.

        Pontuação heurística (valores arbitrários, calibráveis):
        - where_antecipado: +5 por condição
        - projecao_antecipada: +1 por coluna projetada (reduz custo de transmissão)
        - ocorrência do nome da tabela em WHERE/FROM_WHERE_ANTECIPADO/condicao: +1 por ocorrência
        - presença de condição complexa na condicao do join: +1
        """
        score = 0

        tabela = join.get('tabela', '')

        # where antecipado do próprio join
        if 'where_antecipado' in join and join['where_antecipado']:
            score += 5 * self._contar_condicoes(join['where_antecipado'])

        # projecao antecipada (reduz tamanho das tuplas)
        if 'projecao_antecipada' in join and join['projecao_antecipada']:
            try:
                score += 1 * len(join['projecao_antecipada'])
            except Exception:
                # se estiver em formato inesperado, ignore
                pass

        # conta menções ao nome da tabela nas cláusulas globais e na condição do join
        cond = join.get('condicao', '') or ''
        chamadas = 0
        for texto in (where_global or '', from_where_antecipado or '', cond):
            if not texto:
                continue
            # conta ocorrências simples do nome da tabela seguido de ponto (TABELA.)
            chamadas += texto.count(f"{tabela}.")

        score += chamadas

        # se a condição do join tem um '=' (padrão de equi-join), dá pequeno bônus
        if '=' in cond:
            score += 1

        return score

    def otimizar(self) -> dict:
        """Retorna um novo parsed_query com a lista 'INNER_JOIN' reordenada.

        A função preserva as demais chaves do dicionário. Caso não haja INNER_JOIN,
        a função retorna o parsed original inalterado.
        """
        parsed = dict(self.parsed_original) if self.parsed_original else {}

        inner_joins = list(parsed.get('INNER_JOIN', []))
        if not inner_joins:
            return parsed

        where_global = parsed.get('WHERE', None)
        from_where_antecipado = parsed.get('FROM_WHERE_ANTECIPADO', None)

        # Calcula score para cada join
        scored = []
        for join in inner_joins:
            try:
                s = self._score_para_join(join, where_global, from_where_antecipado)
            except Exception:
                s = 0
            scored.append((s, join))

        # Ordena em ordem decrescente de score: tabelas mais seletivas primeiro
        scored.sort(key=lambda x: x[0], reverse=True)

        joins_ordenados = [j for (_s, j) in scored]

        parsed_otimizado = dict(parsed)
        parsed_otimizado['INNER_JOIN'] = joins_ordenados

        return parsed_otimizado


if __name__ == '__main__':
    # Exemplo rápido
    parsed = {
        'SELECT': ['A.COL', 'B.COL'],
        'FROM': 'A',
        'INNER_JOIN': [
            {'tabela': 'B', 'condicao': 'A.id = B.a_id'},
            {'tabela': 'C', 'condicao': 'B.c_id = C.id', 'where_antecipado': "C.flag = 1"}
        ],
        'WHERE': "B.x > 10 AND C.flag = 1"
    }

    h = HeuristicaReordenarFolhas(parsed)
    out = h.otimizar()
    print(out)
