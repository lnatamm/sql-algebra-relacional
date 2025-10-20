# 🔧 Solução de Problemas - Graphviz

## Erro: "failed to execute WindowsPath('dot')"

Este erro significa que a **biblioteca Python** está instalada, mas o **executável do sistema** não está acessível.

---

## 🎯 Solução Rápida (Recomendada)

### 1. Diagnóstico Automático
Execute este comando para identificar o problema:

```powershell
python diagnostico_graphviz.py
```

O script irá:
- ✅ Verificar se a biblioteca Python está instalada
- ✅ Verificar se o executável está no PATH
- ✅ Procurar instalações do Graphviz no sistema
- ✅ Sugerir soluções específicas para seu caso

---

## 📥 Instalação Completa do Graphviz

### Passo 1: Instalar Biblioteca Python
```powershell
pip install graphviz
```

### Passo 2: Instalar Executável do Sistema

#### Opção A: Instalador Oficial (Recomendado)

1. **Baixar:**
   - Acesse: https://graphviz.org/download/
   - Clique em "Windows install packages"
   - Baixe o instalador `.exe` ou `.msi` mais recente

2. **Instalar:**
   - Execute o instalador
   - ⚠️ **IMPORTANTE:** Marque a opção **"Add Graphviz to the system PATH for all users"**
   - Complete a instalação

3. **Reiniciar:**
   - Feche **completamente** o VS Code
   - Abra novamente o VS Code
   - Abra um novo terminal

4. **Verificar:**
   ```powershell
   dot -V
   ```
   Deve mostrar a versão instalada

#### Opção B: Via Chocolatey (Se você usa)
```powershell
choco install graphviz
```

### Passo 3: Testar
```powershell
python teste_grafo_visual.py
```

---

## 🛠️ Soluções Alternativas

### Solução 1: Adicionar ao PATH Manualmente (Permanente)

Se o Graphviz está instalado mas não está no PATH:

1. **Encontrar o diretório de instalação:**
   - Geralmente: `C:\Program Files\Graphviz\bin`
   - Ou execute: `python diagnostico_graphviz.py`

2. **Adicionar ao PATH do Sistema:**

   **Via Interface:**
   - Pressione `Win + R`, digite `sysdm.cpl` e pressione Enter
   - Vá na aba "Avançado"
   - Clique em "Variáveis de Ambiente"
   - Em "Variáveis do sistema", selecione "Path"
   - Clique em "Editar"
   - Clique em "Novo"
   - Adicione: `C:\Program Files\Graphviz\bin` (ou seu caminho)
   - Clique "OK" em todas as janelas

   **Via PowerShell (Administrador):**
   ```powershell
   [System.Environment]::SetEnvironmentVariable('Path', $env:Path + ';C:\Program Files\Graphviz\bin', 'Machine')
   ```

3. **Reiniciar VS Code completamente**

### Solução 2: Workaround Temporário (Sem modificar PATH)

Use o script de workaround:

```powershell
python teste_workaround.py
```

Se funcionar, você pode adicionar estas linhas **NO INÍCIO** do `main.py`:

```python
import os

# Adicionar Graphviz ao PATH temporariamente
graphviz_path = r"C:\Program Files\Graphviz\bin"
if os.path.exists(graphviz_path):
    os.environ['PATH'] = graphviz_path + os.pathsep + os.environ['PATH']
```

### Solução 3: Usar Apenas Visualizações ASCII (Sem Graphviz)

O projeto funciona perfeitamente **sem** graphviz! Você terá:

✅ Árvore ASCII
✅ Ordem de execução
✅ Estatísticas
✅ Álgebra relacional

Apenas os arquivos PNG/PDF/SVG não serão gerados.

```python
from classes.parser import Parser
from classes.grafo_execucao import GrafoExecucao

query = "SELECT * FROM usuarios WHERE idade >= 18;"
parsed = Parser().parse(query.upper())

gerador = GrafoExecucao(parsed)

# Estas funções funcionam SEM graphviz
print(gerador.gerar_ascii_tree())
print(gerador.gerar_ordem_execucao())
print(gerador.exibir_estatisticas())

# Apenas esta requer graphviz
# gerador.gerar_grafo('png', 'arquivo')  # Comentar se não tiver graphviz
```

---

## 🔍 Verificação Final

Após instalar, execute cada comando para confirmar:

```powershell
# 1. Verificar biblioteca Python
python -c "import graphviz; print(graphviz.__version__)"

# 2. Verificar executável
dot -V

# 3. Diagnóstico completo
python diagnostico_graphviz.py

# 4. Teste final
python teste_grafo_visual.py
```

Todos devem funcionar sem erros!

---

## ❓ Perguntas Frequentes

### P: Instalei mas ainda dá erro
**R:** Você precisa **reiniciar completamente o VS Code** após a instalação. Feche todas as janelas e abra novamente.

### P: O instalador não tem opção de adicionar ao PATH
**R:** Alguns instaladores mais antigos não têm essa opção. Adicione manualmente (veja Solução 1 acima).

### P: Não quero instalar o Graphviz
**R:** Sem problemas! Use apenas as visualizações ASCII. Elas são completas e funcionam perfeitamente.

### P: O executável 'dot' não é reconhecido
**R:** O PATH não foi atualizado. Tente:
1. Reiniciar o terminal
2. Reiniciar o VS Code
3. Verificar se adicionou o caminho correto (deve incluir `/bin`)

### P: Dá erro "Access Denied" ao adicionar ao PATH
**R:** Execute o PowerShell como Administrador ou use o workaround temporário.

---

## 📚 Arquivos de Ajuda

- **`diagnostico_graphviz.py`** - Diagnóstico automático
- **`teste_workaround.py`** - Solução temporária
- **`teste_grafo_visual.py`** - Teste de geração de grafos
- **`SOLUCAO_PROBLEMAS.md`** - Este arquivo

---

## 💡 Dica

Se você só precisa dos grafos ocasionalmente, use os **grafos ASCII**. Eles são:
- ✅ Mais rápidos
- ✅ Funcionam em qualquer lugar
- ✅ Não requerem instalações extras
- ✅ Ideais para debugging e console

Para apresentações e documentação, use os grafos visuais PNG/PDF.

---

## 🆘 Ainda com Problemas?

1. Execute: `python diagnostico_graphviz.py`
2. Copie toda a saída
3. Isso ajudará a identificar exatamente qual é o problema

---

**Última atualização:** Outubro 2025

## 📄 Notas
### Documentação gerada utilizando inteligência artificial.