import re
from consts import PADRAO, PALAVRAS_RESERVADAS, TABELAS, COLUNAS
 
class Parser:
    
    def __init__(self):
        pass

    def _hasPontoVirgula(self, query: str) -> bool:
        if query.endswith(";"):
            return True
        else:
            return False

    def _hasSelect(self, query: str) -> bool:
        if query.startswith("SELECT "):
            return True
        else:
            return False

    def _hasSintaxError(self, query: str) -> bool:
        match = re.match(PADRAO, query)
        if not match:
            return True
        else:
            return False
    
    def _validade_table_and_columns(self, sentence: str):
        table_valid = False
        column_valid = False
        for word in sentence.split(" "):
            if word == "" or word.upper() in {"AND", "OR", "=", "<", ">", "<=", ">=", "!="}:
                continue
            left_word = word.split(".")[0] if "." in word else word
            right_word = word.split(".")[1] if "." in word else None
            
            for tabela in TABELAS:
                if (left_word.upper() == tabela.upper()) or left_word is None:
                    table_valid = True
                    break
            for coluna in COLUNAS:
                if (right_word and coluna.upper()) or right_word is None:
                    column_valid = True
                    break
        if not table_valid or not column_valid:
            raise ValueError("Tabela ou coluna inválida encontrada.")

    def parse(self, query: str) -> dict | None:

        query = query.strip()
        query_upper = query.upper()
        query_clean = query_upper.rstrip(";").strip()

        if not self._hasPontoVirgula(query_upper):
            print("❌ Faltando ponto e virgula no final da query!")
            return None

        if not self._hasSelect(query_upper):
            print("❌ Faltando 'SELECT' no início da query!")
            return None

        if self._hasSintaxError(query_clean):
            print("❌ Há algum erro de sintax na query!")
            return None
        
        match = re.match(PADRAO, query_clean)

        # Parse das colunas
        colunas_raw = match.group("select")
        colunas = [col.strip() for col in colunas_raw.split(",")]

        if len(colunas) > 1 and "*" in colunas:
            print("❌ O simbolo '*' não pode ser combinado com outras colunas.")
            return None

        for col in colunas:
            if col == "*":
                continue

            col_upper = col.strip().upper()

            if col_upper in PALAVRAS_RESERVADAS:
                print(f"❌ Nome de coluna inválido: '{col}'")
                return None

            if " " in col:
                print(f"❌ Erro de sintaxe: espaço indevido na coluna '{col}'")
                return None

            if "." in col:
                partes = col.split(".")
                if len(partes) != 2 or not all(p.isidentifier() for p in partes):
                    print(f"❌ Coluna com formato inválido (muitos pontos ou nome incorreto): '{col}'")
                    return None
            elif not col.isidentifier():
                print(f"❌ Nome de coluna inválido: '{col}'")
                return None


        # Parse do FROM
        tabela_from = match.group("from")
        if not tabela_from.isidentifier():
            print(f"❌ Nome de tabela inválido: {tabela_from}")
            return None

        # Parse de INNER JOINs
        inner_joins = []
        joins_raw = match.group("joins")
        if joins_raw:
            join_padrao = r"INNER\s+JOIN\s+(\w+)\s+ON\s+(\w+\.\w+\s*=\s*\w+\.\w+)"
            for join_match in re.finditer(join_padrao, joins_raw):
                tabela_join = join_match.group(1)
                condicao_join = join_match.group(2)
                if not tabela_join.isidentifier() or "=" not in condicao_join:
                    print(f"❌ INNER JOIN inválido: {join_match.group(0)}")
                    return None
                inner_joins.append({
                    "tabela": tabela_join,
                    "condicao": condicao_join
                })

        # Parse do WHERE
        where_clause = match.group("where") if match.group("where") else None
        if where_clause:
            where_clause = where_clause.strip()
            if not where_clause:
                print("❌ Condição WHERE está vazia.")
                return None

        for select in colunas:
            self._validade_table_and_columns(select)
        for join in inner_joins:
            self._validade_table_and_columns(join["condicao"])
            self._validade_table_and_columns(join["tabela"])
        self._validade_table_and_columns(where_clause)

        print("✅ Query sintaticamente válida.")
        return {
            "SELECT": colunas,
            "FROM": tabela_from,
            "INNER_JOIN": inner_joins,
            "WHERE": where_clause
        }
