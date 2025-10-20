# SQL para Álgebra Relacional - Gerador de Grafos

Este projeto converte queries SQL para notação de álgebra relacional e gera grafos visuais da árvore de execução.

## Funcionalidades

### 1. Parser SQL
- Valida sintaxe de queries SQL
- Suporta SELECT, FROM, INNER JOIN, WHERE
- Retorna estrutura parseada da query

### 2. Conversor para Álgebra Relacional
Converte SQL para notação de álgebra relacional usando:
- **σ (sigma)**: Seleção (WHERE)
- **π (pi)**: Projeção (SELECT)
- **⋈ (bowtie)**: Junção (INNER JOIN)

### 3. Gerador de Grafos de Execução
Cria representações visuais da árvore de execução com:
- **Árvore ASCII**: Visualização em texto
- **Ordem de Execução**: Lista sequencial de operações
- **Estatísticas**: Métricas sobre a query
- **Grafo Visual (Graphviz)**: Imagem PNG/PDF/SVG (requer graphviz)
- **Alternativas mais simples**:
  - Mermaid: exporta string para usar em Markdown (sem dependências)
  - Rich: árvore colorida no terminal (pip install rich)
  - NetworkX+Matplotlib: gera PNG (pip install networkx matplotlib)

## Instalação

### Dependências Básicas
```bash
# O projeto funciona sem dependências externas para funcionalidades básicas
python main.py
```

### Para Grafos Visuais (Opcional)
```bash
# Instalar biblioteca Python
pip install graphviz

# Instalar executável Graphviz:
# Windows: https://graphviz.org/download/ (adicionar ao PATH)
# Linux: sudo apt-get install graphviz
# Mac: brew install graphviz

# Alternativas sem executável externo
pip install rich
pip install networkx matplotlib
```

## Uso

### Executar o programa
```bash
python main.py
```

### Exemplo de Saída

Para a query:
```sql
SELECT Alunos.nome, Cursos.nome 
FROM Alunos 
INNER JOIN Cursos ON Alunos.curso_id = Cursos.id 
WHERE Cursos.nome = 'Banco de Dados';
```

**Álgebra Relacional:**
```
π_{ALUNOS.NOME, CURSOS.NOME}(σ_{CURSOS.NOME = 'BANCO DE DADOS'}((ALUNOS ⋈_{ALUNOS.CURSO_ID = CURSOS.ID} CURSOS)))
```

**Árvore de Execução (ASCII):**
```
  📊 ALUNOS
    📊 CURSOS
      │
      ├─ ⋈ Junção: ALUNOS.CURSO_ID = CURSOS.ID
      │
      σ Seleção: CURSOS.NOME = 'BANCO DE DADOS'
      │
      π Projeção: ALUNOS.NOME, CURSOS.NOME
```

**Ordem de Execução:**
```
1. [SCAN    ] Tabela: ALUNOS
2. [SCAN    ] Tabela: CURSOS
3. [JOIN    ] Junção: ALUNOS.CURSO_ID = CURSOS.ID
4. [SELECT  ] Filtro: CURSOS.NOME = 'BANCO DE DADOS'
5. [PROJECT ] Projeção: ALUNOS.NOME, CURSOS.NOME
```

## Estrutura do Projeto

```
sql-algebra-relacional/
│
├── main.py                    # Arquivo principal
├── consts.py                  # Constantes e padrões regex
│
└── classes/
    ├── parser.py              # Parser de SQL
    ├── algebra_relacional.py  # Conversor para álgebra relacional
    └── grafo_execucao.py      # Gerador de grafos de execução
```

## API

### GrafoExecucao

```python
from classes.parser import Parser
from classes.grafo_execucao import GrafoExecucao

# Parsear query
parsed = Parser().parse("SELECT * FROM usuarios WHERE idade > 18;")

# Criar gerador de grafo
gerador = GrafoExecucao(parsed)

# Gerar árvore ASCII
print(gerador.gerar_ascii_tree())

# Obter ordem de execução
ordem = gerador.gerar_ordem_execucao()

# Obter estatísticas
stats = gerador.exibir_estatisticas()

# Gerar grafo visual (requer graphviz)
gerador.gerar_grafo(formato='png', nome_arquivo='meu_grafo')

# Exportar Mermaid (sem dependências)
mermaid = gerador.gerar_mermaid(direcao='BT', incluir_legenda=True)
print(mermaid)

# Árvore colorida no terminal (Rich)
try:
  gerador.renderizar_rich_tree()
except ImportError:
  print("Instale: pip install rich")

# PNG com NetworkX (sem binários externos)
try:
  caminho = gerador.gerar_grafo_networkx('meu_grafo_nx.png')
  print('Gerado:', caminho)
except ImportError:
  print('Instale: pip install networkx matplotlib')
```

### Formatos de Saída Suportados
- `png` - Imagem PNG (padrão)
- `pdf` - Documento PDF
- `svg` - Gráfico vetorial SVG
- `jpg` - Imagem JPEG

## Características dos Grafos Visuais

- **Nós Azuis**: Tabelas base
- **Nós Verdes**: Operação de Projeção (π)
- **Nós Amarelos**: Operação de Seleção (σ)
- **Nós Vermelhos**: Operação de Junção (⋈)
- **Fluxo Bottom-Up**: Das tabelas base até o resultado final

## Limitações

- Suporta apenas INNER JOIN (não LEFT, RIGHT, FULL JOIN)
- Não suporta subconsultas
- Não suporta GROUP BY, HAVING, ORDER BY
- Não suporta funções agregadas (COUNT, SUM, etc)
- Condições WHERE simples (sem AND/OR complexos)

## Exemplos Adicionais

### Query Simples
```python
query = "SELECT nome, idade FROM pessoas WHERE idade >= 18;"
```

### Query com Multiple Joins
```python
query = """
SELECT A.nome, B.titulo, C.departamento 
FROM empregados A 
INNER JOIN projetos B ON A.projeto_id = B.id 
INNER JOIN departamentos C ON B.dept_id = C.id 
WHERE C.ativo = true;
"""
```

## Contribuindo

Sinta-se à vontade para abrir issues ou pull requests para melhorias!

## Licença

Este projeto é de código aberto para fins educacionais.

## 📝 Notas

### Documentação gerada utilizando inteligência artificial.