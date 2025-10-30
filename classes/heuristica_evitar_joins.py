import re


class HeuristicaEvitarProdutoCartesiano:
	"""
	Heurística para reduzir/evitar produtos cartesianos:

	- Extrai condições de junção do WHERE do tipo `T1.col = T2.col` e as associa
	  ao JOIN apropriado (se possível), removendo-as do WHERE.
	- Reordena a lista `INNER_JOIN` colocando primeiro os joins que têm condição
	  e deixando joins sem condição (prováveis produtos cartesianos) para o fim.

	Observações e limitações:
	- A heurística procura apenas por igualdades entre colunas com a forma
	  `TABELA.COLUNA = TABELA2.COLUNA` (sem alias). Se o parser suporta aliases,
	  seria necessário ajustar a detecção.
	- Só altera a estrutura quando encontrar condições de junção explícitas no
	  WHERE; caso contrário, limita-se a reordenar joins sem condição para o final
	  (estratégia conservadora para adiar produtos cartesianos).
	"""

	SEPARADOR_AND = ' AND '

	# Regex para extrair igualdades entre duas colunas: TABELA.COL = TABELA2.COL
	RE_EQUIJOIN = re.compile(r"([A-Z0-9_]+)\.([A-Z0-9_]+)\s*=\s*([A-Z0-9_]+)\.([A-Z0-9_]+)")

	def __init__(self, parsed_query: dict):
		self.parsed_original = parsed_query or {}

	def _extrair_condicoes_where(self, where_clause: str) -> list:
		if not where_clause:
			return []
		return [c.strip() for c in where_clause.split(self.SEPARADOR_AND) if c.strip()]

	def _encontrar_join_para_tabelas(self, inner_joins: list, t1: str, t2: str):
		"""Retorna índice do join mais apropriado para associar a condição entre t1 e t2.

		Estratégia simples:
		- Se houver um join cuja tabela é exatamente t1 ou t2, retorna esse índice.
		- Caso haja múltiplos, prefere join que já contenha referência à outra tabela
		  na sua condição (sinal que este join conecta as duas tabelas).
		- Senão, retorna a primeira ocorrência.
		"""
		candidatos = []
		for idx, j in enumerate(inner_joins):
			tabela = j.get('tabela', '')
			if tabela == t1 or tabela == t2:
				candidatos.append((idx, j))

		if not candidatos:
			return None

		# Se algum candidato já tem condicao que menciona a outra tabela, escolha-o
		for idx, j in candidatos:
			cond = j.get('condicao', '') or ''
			if t1 != j.get('tabela', '') and f"{t1}." in cond:
				return idx
			if t2 != j.get('tabela', '') and f"{t2}." in cond:
				return idx

		# Caso padrão: retorna o primeiro candidato
		return candidatos[0][0]

	def otimizar(self) -> dict:
		parsed = dict(self.parsed_original) if self.parsed_original else {}

		inner_joins = list(parsed.get('INNER_JOIN', []))
		if not inner_joins:
			return parsed

		where_clause = parsed.get('WHERE', None)
		condicoes = self._extrair_condicoes_where(where_clause)

		usadas = set()

		# Tentar associar equijoins do WHERE aos JOINs
		for i, cond in enumerate(condicoes):
			m = self.RE_EQUIJOIN.search(cond)
			if not m:
				continue

			t1, c1, t2, c2 = m.group(1), m.group(2), m.group(3), m.group(4)

			idx = self._encontrar_join_para_tabelas(inner_joins, t1, t2)
			if idx is None:
				continue

			join = inner_joins[idx]

			# Se a condição já estiver presente, apenas marque como usada
			if cond in (join.get('condicao') or ''):
				usadas.add(i)
				continue

			# Anexa a condição ao join (preservando possível condicao existente)
			if join.get('condicao'):
				# evita duplicar
				if cond not in join['condicao']:
					join['condicao'] = f"{join['condicao']}{self.SEPARADOR_AND}{cond}"
			else:
				join['condicao'] = cond

			inner_joins[idx] = join
			usadas.add(i)

		# Reconstrói WHERE com as condições não usadas
		restantes = [c for idx, c in enumerate(condicoes) if idx not in usadas]
		parsed_atualizado = dict(parsed)
		if restantes:
			parsed_atualizado['WHERE'] = self.SEPARADOR_AND.join(restantes)
		else:
			parsed_atualizado['WHERE'] = None

		# Reordena INNER_JOIN: primeiros joins com condicao, depois sem condicao
		with_cond = [j for j in inner_joins if j.get('condicao')]
		without_cond = [j for j in inner_joins if not j.get('condicao')]
		parsed_atualizado['INNER_JOIN'] = with_cond + without_cond

		return parsed_atualizado


if __name__ == '__main__':
	exemplo = {
		'SELECT': ['A.X', 'B.Y', 'C.Z'],
		'FROM': 'A',
		'INNER_JOIN': [
			{'tabela': 'B', 'condicao': ''},
			{'tabela': 'C', 'condicao': ''}
		],
		'WHERE': 'A.id = B.a_id AND B.c_id = C.id AND A.flag = 1'
	}

	h = HeuristicaEvitarProdutoCartesiano(exemplo)
	out = h.otimizar()
	print(out)
