# 🚀 Início Rápido - Gerador de Grafos

## ✅ O Projeto Já Funciona!

**Boas notícias:** O projeto funciona **perfeitamente** sem o Graphviz! Você já tem acesso a todas as funcionalidades principais.

---

## 📋 O Que Você Pode Fazer AGORA

### 1. Executar o Programa Principal
```powershell
python main.py
```

**Você terá:**
- ✅ Parser de SQL
- ✅ Conversão para álgebra relacional
- ✅ Árvore de execução ASCII
- ✅ Ordem de execução detalhada
- ✅ Estatísticas da query

### 2. Ver Exemplos
```powershell
python exemplos_grafo.py
```

---

## 🎨 Sobre os Grafos Visuais (Opcional)

Os grafos visuais PNG/PDF/SVG são **opcionais** e **extras**. O projeto funciona 100% sem eles!

### Quando Usar Grafos Visuais?
- 📊 Apresentações
- 📄 Documentação
- 📝 Relatórios

### Quando Usar Grafos ASCII?
- 💻 Desenvolvimento diário
- 🐛 Debugging
- 🚀 Console/Terminal
- ⚡ Velocidade

---

## 🔧 Quer Grafos Visuais? (Opcional)

### Opção 1: Diagnóstico Automático
```powershell
python diagnostico_graphviz.py
```
O script irá guiá-lo na instalação.

### Opção 2: Instalação Manual Rápida

1. **Baixar e Instalar:**
   - https://graphviz.org/download/
   - Marque "Add to PATH" durante instalação
   - Reinicie o VS Code

2. **Verificar:**
   ```powershell
   dot -V
   ```

3. **Testar:**
   ```powershell
   python teste_grafo_visual.py
   ```

### Opção 3: Workaround (Sem modificar PATH)
```powershell
python teste_workaround.py
```

---

## 📚 Guias Disponíveis

| Arquivo | Quando Usar |
|---------|-------------|
| `README.md` | Documentação completa do projeto |
| `GUIA_GRAFOS.md` | Referência da API de grafos |
| `SOLUCAO_PROBLEMAS.md` | Problemas com Graphviz |
| `INICIO_RAPIDO.md` | Este arquivo - começar agora! |

---

## 🎯 Exemplos Rápidos

### Exemplo 1: Uso Básico
```python
from classes.parser import Parser
from classes.grafo_execucao import GrafoExecucao

# Sua query SQL
query = "SELECT nome, idade FROM usuarios WHERE idade >= 18;"

# Parse
parsed = Parser().parse(query.upper())

# Gerar grafo
gerador = GrafoExecucao(parsed)

# Visualizar (funciona sempre, sem graphviz)
print(gerador.gerar_ascii_tree())
```

**Saída:**
```
Árvore de Execução (bottom-up):
============================================================
📊 USUARIOS
  σ Seleção: IDADE >= 18
  │
    π Projeção: NOME, IDADE
============================================================
↑ Resultado Final
```

### Exemplo 2: Análise Completa
```python
from classes.parser import Parser
from classes.algebra_relacional import AlgebraRelacional
from classes.grafo_execucao import GrafoExecucao

query = "SELECT * FROM produtos WHERE preco > 100;"
parsed = Parser().parse(query.upper())

if parsed:
    # 1. Álgebra Relacional
    algebra = AlgebraRelacional(parsed)
    print("Expressão:", algebra.converter())
    # Saída: σ_{PRECO > 100}(PRODUTOS)
    
    # 2. Grafo de Execução
    grafo = GrafoExecucao(parsed)
    
    # Árvore ASCII
    print(grafo.gerar_ascii_tree())
    
    # Ordem de execução
    for i, (op, desc) in enumerate(grafo.gerar_ordem_execucao(), 1):
        print(f"{i}. {op}: {desc}")
    # Saída:
    # 1. SCAN: Tabela: PRODUTOS
    # 2. SELECT: Filtro: PRECO > 100
    # 3. PROJECT: Projeção: * (todas as colunas)
    
    # Estatísticas
    stats = grafo.exibir_estatisticas()
    print(f"Tabelas: {stats['numero_tabelas']}")
    print(f"Junções: {stats['numero_juncoes']}")
    print(f"Tem filtro: {stats['tem_filtro']}")
```

---

## 🎓 Conceitos de Álgebra Relacional

### Operadores Usados

| Símbolo | Nome | SQL Equivalente | Exemplo |
|---------|------|-----------------|---------|
| **σ** | Seleção | WHERE | σ_{idade>18}(usuarios) |
| **π** | Projeção | SELECT | π_{nome,email}(usuarios) |
| **⋈** | Junção | INNER JOIN | A ⋈_{id=fk} B |

### Ordem de Execução (Bottom-Up)

```
1. 📊 Tabelas Base (FROM)
        ↓
2. ⋈  Junções (INNER JOIN)
        ↓
3. σ  Seleção (WHERE)
        ↓
4. π  Projeção (SELECT)
        ↓
   Resultado Final
```

---

## 💡 Dicas Importantes

### ✅ Faça Isso
- Use grafos ASCII para desenvolvimento
- Execute `main.py` para ver exemplos
- Consulte `GUIA_GRAFOS.md` para referência
- Leia `SOLUCAO_PROBLEMAS.md` se tiver erros

### ❌ Evite Isso
- Não se preocupe com graphviz agora (é opcional!)
- Não tente gerar PDF/PNG sem graphviz instalado
- Não complique - comece simples!

---

## 🚦 Checklist de Primeiros Passos

- [ ] Execute `python main.py`
- [ ] Veja os exemplos em `exemplos_grafo.py`
- [ ] Teste com sua própria query
- [ ] Explore as visualizações ASCII
- [ ] (Opcional) Instale graphviz para PDFs

---

## 🎉 Pronto para Começar!

Execute agora:
```powershell
python main.py
```

E veja a mágica acontecer! ✨

---

## 📞 Precisa de Ajuda?

| Problema | Solução |
|----------|---------|
| Erro de sintaxe SQL | Verifique ponto-e-vírgula e palavras-chave |
| Erro com graphviz | Abra `SOLUCAO_PROBLEMAS.md` |
| Dúvidas sobre API | Consulte `GUIA_GRAFOS.md` |
| Entender o projeto | Leia `README.md` |

---

## 📄 Notas
### Documentação gerada utilizando inteligência artificial.
