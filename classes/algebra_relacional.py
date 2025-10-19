"""
Conversor de SQL Parser para Álgebra Relacional

Este módulo converte um dicionário parseado de SQL para notação de álgebra relacional.

Operadores usados:
- σ (sigma): Seleção (WHERE)
- π (pi): Projeção (SELECT)
- ⋈ (bowtie): Junção natural/inner join
- × (times): Produto cartesiano
"""

class AlgebraRelacional:
    """Classe para converter SQL parseado em álgebra relacional"""
    
    def __init__(self, parsed_query: dict):
        """
        Inicializa o conversor com uma query parseada
        
        Args:
            parsed_query: Dicionário retornado pelo parseQuery()
        """
        self.parsed = parsed_query
        self.select_cols = parsed_query.get('SELECT', [])
        self.from_table = parsed_query.get('FROM', '')
        self.inner_joins = parsed_query.get('INNER_JOIN', [])
        self.where_clause = parsed_query.get('WHERE', None)
    
    def _formatar_condicao(self, condicao: str) -> str:
        """
        Formata uma condição para notação de álgebra relacional
        
        Args:
            condicao: String com a condição (ex: "ALUNOS.CURSO_ID = CURSOS.ID")
        
        Returns:
            String formatada
        """
        return condicao.strip()
    
    def _criar_juncao(self) -> str:
        """
        Cria a expressão de junção (⋈) para os INNER JOINs
        
        Returns:
            String com a expressão de junção
        """
        # Começa com a tabela FROM
        resultado = self.from_table
        
        # Adiciona cada INNER JOIN
        for join in self.inner_joins:
            tabela = join['tabela']
            condicao = self._formatar_condicao(join['condicao'])
            resultado = f"({resultado} ⋈_{{{condicao}}} {tabela})"
        
        return resultado
    
    def _criar_selecao(self, expressao_base: str) -> str:
        """
        Aplica a operação de seleção (σ) se houver WHERE
        
        Args:
            expressao_base: Expressão base (junções)
        
        Returns:
            String com seleção aplicada
        """
        if self.where_clause:
            condicao = self._formatar_condicao(self.where_clause)
            return f"σ_{{{condicao}}}({expressao_base})"
        return expressao_base
    
    def _criar_projecao(self, expressao_base: str) -> str:
        """
        Aplica a operação de projeção (π) para o SELECT
        
        Args:
            expressao_base: Expressão com junções e seleções
        
        Returns:
            String com projeção aplicada
        """
        # Se for SELECT *, não precisa de projeção explícita
        if self.select_cols == ['*']:
            return expressao_base
        
        colunas = ', '.join(self.select_cols)
        return f"π_{{{colunas}}}({expressao_base})"
    
    def converter(self) -> str:
        """
        Converte a query parseada para álgebra relacional
        
        A ordem de aplicação é:
        1. Produto cartesiano e junções (⋈)
        2. Seleção (σ) - aplica WHERE
        3. Projeção (π) - aplica SELECT
        
        Returns:
            String com a expressão em álgebra relacional
        """
        # Passo 1: Criar junções
        expr_juncoes = self._criar_juncao()
        
        # Passo 2: Aplicar seleção (WHERE)
        expr_selecao = self._criar_selecao(expr_juncoes)
        
        # Passo 3: Aplicar projeção (SELECT)
        expr_final = self._criar_projecao(expr_selecao)
        
        return expr_final
    
    def converter_detalhado(self) -> dict:
        """
        Converte para álgebra relacional com detalhamento de cada passo
        
        Returns:
            Dicionário com cada etapa da conversão
        """
        expr_juncoes = self._criar_juncao()
        expr_selecao = self._criar_selecao(expr_juncoes)
        expr_final = self._criar_projecao(expr_selecao)
        
        return {
            'etapa_1_juncoes': expr_juncoes,
            'etapa_2_selecao': expr_selecao,
            'etapa_3_projecao': expr_final,
            'expressao_final': expr_final
        }
    
    def __str__(self) -> str:
        """Retorna a expressão em álgebra relacional"""
        return self.converter()


def sql_para_algebra(parsed_query: dict) -> str:
    """
    Função auxiliar para converter SQL parseado em álgebra relacional
    
    Args:
        parsed_query: Dicionário retornado pelo parseQuery()
    
    Returns:
        String com a expressão em álgebra relacional
    """
    conversor = AlgebraRelacional(parsed_query)
    return conversor.converter()


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
    
    print("=" * 80)
    print("CONVERSÃO DE SQL PARA ÁLGEBRA RELACIONAL")
    print("=" * 80)
    print("\nQuery Parseada:")
    print(parsed)
    
    conversor = AlgebraRelacional(parsed)
    
    print("\n" + "-" * 80)
    print("CONVERSÃO DETALHADA:")
    print("-" * 80)
    detalhado = conversor.converter_detalhado()
    print(f"\n1. Junções (⋈):")
    print(f"   {detalhado['etapa_1_juncoes']}")
    print(f"\n2. Seleção (σ) - WHERE:")
    print(f"   {detalhado['etapa_2_selecao']}")
    print(f"\n3. Projeção (π) - SELECT:")
    print(f"   {detalhado['etapa_3_projecao']}")
    
    print("\n" + "=" * 80)
    print("EXPRESSÃO FINAL EM ÁLGEBRA RELACIONAL:")
    print("=" * 80)
    print(f"\n{conversor.converter()}")
    print("\n" + "=" * 80)
