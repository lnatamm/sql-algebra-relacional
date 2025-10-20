"""
Script de diagnóstico e instalação do Graphviz
Este script ajuda a identificar problemas com a instalação do Graphviz
"""

import sys
import shutil
import subprocess
import os

def verificar_python_graphviz():
    """Verifica se a biblioteca Python está instalada"""
    try:
        import graphviz
        print("✅ Biblioteca Python 'graphviz' está instalada")
        print(f"   Versão: {graphviz.__version__}")
        return True
    except ImportError:
        print("❌ Biblioteca Python 'graphviz' NÃO está instalada")
        print("   Solução: pip install graphviz")
        return False

def verificar_executavel_graphviz():
    """Verifica se o executável do Graphviz está no PATH"""
    dot_path = shutil.which('dot')
    if dot_path:
        print(f"✅ Executável 'dot' encontrado em: {dot_path}")
        try:
            result = subprocess.run(['dot', '-V'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            version_info = result.stderr.strip() if result.stderr else result.stdout.strip()
            print(f"   Versão: {version_info}")
        except Exception as e:
            print(f"   ⚠️  Aviso: Não foi possível verificar versão: {e}")
        return True
    else:
        print("❌ Executável 'dot' NÃO encontrado no PATH")
        return False

def mostrar_path_atual():
    """Mostra os diretórios no PATH do sistema"""
    print("\n📂 Diretórios no PATH do sistema:")
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    
    # Procura por Graphviz
    graphviz_dirs = [d for d in path_dirs if 'graphviz' in d.lower()]
    
    if graphviz_dirs:
        print("   Diretórios relacionados ao Graphviz encontrados:")
        for d in graphviz_dirs:
            exists = "✅" if os.path.exists(d) else "❌"
            print(f"   {exists} {d}")
    else:
        print("   ⚠️  Nenhum diretório do Graphviz encontrado no PATH")
    
    return graphviz_dirs

def procurar_graphviz_instalado():
    """Procura por instalações do Graphviz no sistema"""
    print("\n🔍 Procurando por instalações do Graphviz...")
    
    possiveis_locais = [
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
        r"C:\Graphviz\bin",
        os.path.expanduser("~\\Graphviz\\bin"),
    ]
    
    encontrados = []
    for local in possiveis_locais:
        dot_exe = os.path.join(local, 'dot.exe')
        if os.path.exists(dot_exe):
            print(f"   ✅ Encontrado: {local}")
            encontrados.append(local)
        else:
            print(f"   ❌ Não encontrado: {local}")
    
    return encontrados

def sugerir_solucao(py_ok, exe_ok, graphviz_instalados):
    """Sugere soluções baseado no diagnóstico"""
    print("\n" + "=" * 80)
    print("💡 SOLUÇÕES RECOMENDADAS")
    print("=" * 80)
    
    if not py_ok and not exe_ok:
        print("\n📦 PASSO 1: Instalar biblioteca Python")
        print("   Execute no terminal:")
        print("   pip install graphviz")
        print("\n📦 PASSO 2: Instalar executável Graphviz")
        print("   1. Baixe em: https://graphviz.org/download/")
        print("   2. Execute o instalador")
        print("   3. IMPORTANTE: Marque a opção 'Add Graphviz to the system PATH'")
        print("   4. Reinicie o VS Code após a instalação")
        
    elif py_ok and not exe_ok:
        if graphviz_instalados:
            print("\n⚙️  Graphviz está instalado mas NÃO está no PATH!")
            print("\n   SOLUÇÃO RÁPIDA - Adicionar ao PATH manualmente:")
            print("\n   No PowerShell (execute como Administrador):")
            for local in graphviz_instalados:
                print(f"   [System.Environment]::SetEnvironmentVariable('Path', $env:Path + ';{local}', 'Machine')")
            print("\n   Depois, reinicie o VS Code completamente (fechar e abrir).")
            
            print("\n   ALTERNATIVA - Usar caminho completo no código:")
            print("   Adicione estas linhas no início do seu script:")
            print("   import os")
            for local in graphviz_instalados:
                print(f"   os.environ['PATH'] += os.pathsep + r'{local}'")
        else:
            print("\n📦 Graphviz NÃO está instalado no sistema")
            print("\n   INSTALAÇÃO:")
            print("   1. Baixe em: https://graphviz.org/download/")
            print("   2. Escolha: 'Windows install packages' → 'Stable Windows install packages'")
            print("   3. Baixe o arquivo .exe ou .msi mais recente")
            print("   4. Execute o instalador")
            print("   5. IMPORTANTE: Marque 'Add Graphviz to the system PATH for all users'")
            print("   6. Complete a instalação")
            print("   7. Reinicie o VS Code")
            
    else:
        print("\n✅ Tudo está configurado corretamente!")
        print("   Você pode gerar grafos visuais sem problemas.")

def gerar_script_temporario(graphviz_instalados):
    """Gera um script Python para contornar o problema temporariamente"""
    if not graphviz_instalados:
        return
    
    print("\n" + "=" * 80)
    print("🔧 SOLUÇÃO TEMPORÁRIA")
    print("=" * 80)
    print("\nAdicione estas linhas NO INÍCIO dos seus scripts Python:")
    print("\n```python")
    print("import os")
    print("import sys")
    for local in graphviz_instalados:
        print(f"os.environ['PATH'] += os.pathsep + r'{local}'")
    print("```")
    print("\nIsso permite usar o Graphviz sem modificar o PATH do sistema.")

def main():
    print("=" * 80)
    print("🔍 DIAGNÓSTICO DA INSTALAÇÃO DO GRAPHVIZ")
    print("=" * 80)
    print()
    
    # Verificações
    py_ok = verificar_python_graphviz()
    print()
    exe_ok = verificar_executavel_graphviz()
    
    # PATH
    graphviz_no_path = mostrar_path_atual()
    
    # Procurar instalações
    graphviz_instalados = procurar_graphviz_instalado()
    
    # Sugestões
    sugerir_solucao(py_ok, exe_ok, graphviz_instalados)
    
    # Script temporário
    if graphviz_instalados and not exe_ok:
        gerar_script_temporario(graphviz_instalados)
    
    print("\n" + "=" * 80)
    print("📝 APÓS FAZER AS ALTERAÇÕES")
    print("=" * 80)
    print("1. Feche completamente o VS Code")
    print("2. Abra novamente o VS Code")
    print("3. Execute este script novamente para verificar: python diagnostico_graphviz.py")
    print("4. Se tudo estiver OK, tente: python teste_grafo_visual.py")
    print("=" * 80)

if __name__ == "__main__":
    main()
