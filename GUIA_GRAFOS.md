# Guia Completo: Gerador de Grafos de Execução

## 📊 Funcionalidades Implementadas

### 1. **Classe GrafoExecucao**
Localização: `classes/grafo_execucao.py`

#### Métodos Principais:

##### `gerar_ascii_tree()` → str
Gera uma árvore de execução em formato ASCII/texto.

**Exemplo de saída:**
```
Árvore de Execução (bottom-up):
============================================================
📊 ALUNOS
  📊 CURSOS
    │
    ├─ ⋈ Junção: ALUNOS.CURSO_ID = CURSOS.ID
    │
    σ Seleção: CURSOS.NOME = 'BANCO DE DADOS'
    │
    π Projeção: ALUNOS.NOME, CURSOS.NOME
============================================================
↑ Resultado Final
```

##### `gerar_ordem_execucao()` → list[tuple]
Retorna a sequência de operações que serão executadas.

**Exemplo de retorno:**
```python
[
    ('SCAN', 'Tabela: ALUNOS'),
    ('SCAN', 'Tabela: CURSOS'),
    ('JOIN', 'Junção: ALUNOS.CURSO_ID = CURSOS.ID'),
    ('SELECT', 'Filtro: IDADE >= 18'),
    ('PROJECT', 'Projeção: NOME, IDADE')
]
```

##### `exibir_estatisticas()` → dict
Fornece métricas sobre a complexidade da query.

**Exemplo de retorno:**
```python
{
    'numero_tabelas': 3,
    'numero_juncoes': 2,
    'tem_filtro': True,
    'numero_colunas_projecao': 3,
    'eh_select_all': False
}
```

##### `gerar_grafo(formato='png', nome_arquivo='grafo')` → str
Gera um arquivo visual do grafo com Graphviz (requer executável `dot`).

**Formatos suportados:** `png`, `pdf`, `svg`, `jpg`

**Retorna:** Caminho do arquivo gerado

##### `gerar_mermaid(direcao='TB', incluir_legenda=True, arquivo=None)` → str
Exporta o diagrama como Mermaid (flowchart), sem dependências externas. Pode salvar em `.md` ou `.mmd`.

##### `renderizar_rich_tree()` → bool
Renderiza árvore colorida no terminal com Rich. Requer `pip install rich`.

##### `gerar_grafo_networkx(nome_arquivo='grafo_networkx.png')` → str
Gera PNG usando NetworkX + Matplotlib (puro Python). Requer `pip install networkx matplotlib`.

---

## 🚀 Como Usar

### Uso Básico

```python
from classes.parser import Parser
from classes.grafo_execucao import GrafoExecucao

# 1. Parsear a query SQL
query = "SELECT nome, idade FROM usuarios WHERE idade >= 18;"
parsed = Parser().parse(query.upper())

# 2. Criar o gerador de grafo
gerador = GrafoExecucao(parsed)

# 3. Gerar visualizações
print(gerador.gerar_ascii_tree())
```

### Uso Completo

```python
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao

query = """
SELECT A.nome, B.titulo 
FROM autores A 
INNER JOIN livros B ON A.id = B.autor_id 
WHERE B.ano > 2020;
"""

# Parser
parsed = Parser().parse(query.upper())

if parsed:
    # Álgebra Relacional
    algebra = AlgebraRelacional(parsed)
    print("Expressão:", algebra.converter())
    
    # Grafo de Execução
    grafo = GrafoExecucao(parsed)
    
    # Árvore ASCII
    print(grafo.gerar_ascii_tree())
    
    # Ordem de execução
    for i, (op, desc) in enumerate(grafo.gerar_ordem_execucao(), 1):
        print(f"{i}. {op}: {desc}")
    
    # Estatísticas
    stats = grafo.exibir_estatisticas()
    print(f"Complexidade: {stats['numero_tabelas']} tabelas, "
          f"{stats['numero_juncoes']} junções")
    
      # Arquivo visual (Graphviz, opcional)
      try:
        arquivo = grafo.gerar_grafo('png', 'meu_grafo')
        print(f"Grafo salvo em: {arquivo}")
      except ImportError:
        print("Instale graphviz para gerar arquivos visuais")

      # Mermaid (sem dependências)
      print(grafo.gerar_mermaid(direcao='BT', incluir_legenda=True))

      # Rich (terminal colorido)
      try:
        grafo.renderizar_rich_tree()
      except ImportError:
        print("Instale: pip install rich")

      # NetworkX (PNG puro Python)
      try:
        print('PNG (NX):', grafo.gerar_grafo_networkx('meu_grafo_nx.png'))
      except ImportError:
        print('Instale: pip install networkx matplotlib')
```

---

## 📁 Arquivos Criados

### `classes/grafo_execucao.py`
Implementação principal da classe GrafoExecucao com todos os métodos.

### `main.py` (atualizado)
Agora inclui geração automática de grafos para cada query processada.

### `exemplos_grafo.py`
Arquivo com 5 exemplos de uso:
1. Query simples
2. Query com múltiplas junções
3. Geração de arquivo visual
4. Comparação de complexidade
5. Query personalizada (interativo)

### `README.md`
Documentação completa do projeto.

### `requirements.txt`
Lista de dependências (graphviz).

### `GUIA_GRAFOS.md` (este arquivo)
Guia de referência rápida.

---

## 🎨 Visualização dos Grafos Visuais

Quando o graphviz está instalado, os grafos gerados incluem:

### Cores dos Nós:
- 🔵 **Azul claro** - Tabelas base (dados de entrada)
- 🟢 **Verde claro** - Operação π (Projeção/SELECT)
- 🟡 **Amarelo claro** - Operação σ (Seleção/WHERE)
- 🔴 **Vermelho claro** - Operação ⋈ (Junção/JOIN)

### Estrutura:
- **Fluxo:** Bottom-up (das folhas para a raiz)
- **Direção:** Das tabelas base até o resultado final
- **Legenda:** Incluída automaticamente no canto do grafo

---

## 🔧 Instalação do Graphviz (Opcional)

### Para Windows:
```powershell
# 1. Instalar biblioteca Python
pip install graphviz

# 2. Baixar e instalar executável
# https://graphviz.org/download/
# Importante: Adicionar ao PATH durante instalação
```

### Para Linux:
```bash
# 1. Instalar biblioteca Python
pip install graphviz

# 2. Instalar executável
sudo apt-get install graphviz
```

### Para Mac:
```bash
# 1. Instalar biblioteca Python
pip install graphviz

# 2. Instalar executável
brew install graphviz
```

---

## 📊 Exemplos de Saída

### Query Simples
```sql
SELECT nome FROM usuarios;
```

**Saída:**
```
📊 USUARIOS
  π Projeção: NOME
```

### Query com Filtro
```sql
SELECT * FROM produtos WHERE preco > 100;
```

**Saída:**
```
📊 PRODUTOS
  σ Seleção: PRECO > 100
  │
  π Projeção: * (todas as colunas)
```

### Query com Join
```sql
SELECT u.nome, p.titulo 
FROM usuarios u 
INNER JOIN posts p ON u.id = p.user_id;
```

**Saída:**
```
📊 USUARIOS
  📊 POSTS
    │
    ├─ ⋈ Junção: U.ID = P.USER_ID
    │
    π Projeção: U.NOME, P.TITULO
```

---

## ⚡ Dicas de Uso

1. **Sempre em maiúsculas:** O parser converte automaticamente para uppercase
2. **Ponto e vírgula:** Obrigatório no final de cada query
3. **Grafos ASCII:** Funcionam sem dependências externas
4. **Grafos visuais:** Requerem graphviz instalado
5. **Múltiplos formatos:** Use `formato='pdf'` ou `formato='svg'` conforme necessário

---

## 🐛 Solução de Problemas

### "graphviz não está instalado"
- Instale com: `pip install graphviz`
- Instale o executável do sistema (veja seção de instalação)

### "Erro ao gerar grafo visual"
- Verifique se o executável do graphviz está no PATH
- No Windows, pode ser necessário reiniciar o terminal após instalação

### "Query sintaticamente inválida"
- Verifique se há ponto e vírgula no final
- Confira se todas as palavras-chave estão corretas
- O parser tem limitações (veja README.md)

---

## 📚 Arquitetura

```
Query SQL
    ↓
Parser (classes/parser.py)
    ↓
Dict Parseado
    ↓ → AlgebraRelacional (classes/algebra_relacional.py)
    ↓ → GrafoExecucao (classes/grafo_execucao.py)
    ↓
Visualizações:
  - Árvore ASCII
  - Ordem de execução
  - Estatísticas
  - Grafo visual (PNG/PDF/SVG)
```

---

## 🎯 Casos de Uso

1. **Educação:** Ensinar conceitos de álgebra relacional
2. **Debug:** Visualizar o plano de execução de queries
3. **Otimização:** Identificar operações custosas
4. **Documentação:** Gerar diagramas para documentar queries
5. **Comparação:** Analisar diferenças entre queries similares

---

## 📝 Limitações Atuais

- Suporta apenas INNER JOIN
- Não suporta subconsultas
- WHERE simples (sem AND/OR complexos)
- Não suporta GROUP BY, HAVING, ORDER BY
- Não suporta funções agregadas

---

## 🔮 Possíveis Melhorias Futuras

- [ ] Suporte a LEFT/RIGHT/FULL JOIN
- [ ] Subconsultas
- [ ] Operadores AND/OR no WHERE
- [ ] GROUP BY e funções agregadas
- [ ] Estimativa de custo de operações
- [ ] Otimização automática de queries
- [ ] Exportar para outros formatos (JSON, XML)
- [ ] Interface web interativa

---

## 📞 Suporte

Para dúvidas ou sugestões sobre o gerador de grafos, consulte:
- `README.md` - Documentação geral
- `exemplos_grafo.py` - Exemplos práticos
- Código fonte em `classes/grafo_execucao.py`

---

## 📄 Notas

**Versão:** 1.0  
**Data:** Outubro 2025  
**Autor:** Sistema de Conversão SQL → Álgebra Relacional<br>
**Documentação gerada utilizando inteligência artificial.**