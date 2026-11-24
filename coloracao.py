"""Projeto de 3-coloração: guloso sequencial e backtracking.

Referência: Paulo Feofiloff, IME-USP, Coloração de vértices.
https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/vertex-coloring.html
Guloso adaptado da função em C UGRAPHseqColoring; backtracking implementado
a partir da descrição do exercício de busca em profundidade da mesma fonte.
"""

import argparse
import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from time import perf_counter


def criar_grafo(n, arestas):
    """Cria um grafo simples não dirigido, com vértices de 0 até n-1."""
    if type(n) is not int or n < 0:
        raise ValueError('O número de vértices deve ser um inteiro não negativo.')
    grafo = [set() for _ in range(n)]
    for u, v in arestas:
        if type(u) is not int or type(v) is not int or not (0 <= u < n and 0 <= v < n):
            raise ValueError('Aresta com vértice fora do intervalo 0..n-1.')
        if u == v:
            raise ValueError('Este projeto trabalha com grafos simples, sem laços.')
        grafo[u].add(v)
        grafo[v].add(u)
    return grafo


def verificar_ordem(grafo, ordem):
    ordem = list(range(len(grafo))) if ordem is None else list(ordem)
    if any(type(v) is not int for v in ordem) or sorted(ordem) != list(range(len(grafo))):
        raise ValueError('A ordem deve conter cada vértice exatamente uma vez.')
    return ordem


def validar_coloracao(grafo, cores, limite=None):
    """Verificação independente da solução; não confundir com busca de solução."""
    if cores is None or len(cores) != len(grafo):
        return False
    if any(type(c) is not int or c < 0 or (limite is not None and c >= limite) for c in cores):
        return False
    return all(cores[u] != cores[v] for u in range(len(grafo)) for v in grafo[u])


def guloso(grafo, ordem=None):
    """Adaptação do guloso sequencial da referência; pode usar mais de 3 cores."""
    ordem = verificar_ordem(grafo, ordem)
    cores = [-1] * len(grafo)
    for v in ordem:
        proibidas = {cores[u] for u in grafo[v] if cores[u] != -1}
        cor = 0
        while cor in proibidas:
            cor += 1
        cores[v] = cor
    return cores


def backtracking(grafo, limite=3, ordem=None):
    """Busca exata; retorna (coloração ou None, contadores da busca).

    Cada chamada mantém uma coloração parcial válida. Quando nenhuma cor
    funciona, desfaz a atribuição anterior e explora outra possibilidade.
    """
    if type(limite) is not int or limite < 1:
        raise ValueError('O limite de cores deve ser um inteiro positivo.')
    ordem = verificar_ordem(grafo, ordem)
    cores = [-1] * len(grafo)
    estatisticas = {'tentativas': 0, 'desfazimentos': 0, 'chamadas': 0}

    def buscar(posicao):
        estatisticas['chamadas'] += 1
        if posicao == len(ordem):
            return True
        v = ordem[posicao]
        for cor in range(limite):
            estatisticas['tentativas'] += 1
            if all(cores[u] != cor for u in grafo[v]):
                cores[v] = cor
                if buscar(posicao + 1):
                    return True
                cores[v] = -1
                estatisticas['desfazimentos'] += 1
        return False

    encontrou = buscar(0)
    return (cores.copy() if encontrou else None), estatisticas


def exemplos():
    return [
        ('Triângulo', criar_grafo(3, [(0, 1), (1, 2), (0, 2)])),
        ('Ciclo de quatro vértices', criar_grafo(4, [(0, 1), (1, 2), (2, 3), (3, 0)])),
        ('Completo K4', criar_grafo(4, [(u, v) for u in range(4) for v in range(u + 1, 4)])),
        ('Exemplo C da referência', criar_grafo(7, [(0, 3), (3, 5), (5, 1), (1, 6), (6, 4), (4, 2)])),
        # Grafo coroa: ai=2*i, bi=2*i+1; ai liga a bj somente quando i != j.
        # A ordem a0,b0,a1,b1,... leva o guloso a usar quatro cores.
        ('Coroa com oito vértices', criar_grafo(8, [(2*i, 2*j+1) for i in range(4) for j in range(4) if i != j])),
    ]


IDENTIFICADORES = ('triangulo', 'ciclo4', 'k4', 'referencia', 'coroa')


def demonstrar(nome, grafo, ordem=None, mostrar_tempos=True):
    ordem = verificar_ordem(grafo, ordem)
    print(f'\n=== {nome} ===')
    print('ENTRADA')
    print(f'Vértices: {len(grafo)} | Arestas: {sum(map(len, grafo)) // 2}')
    print('Arestas:', sorted((u, v) for u in range(len(grafo)) for v in grafo[u] if u < v))
    print('Ordem:', ordem)
    print('Limite do backtracking: 3 cores (0, 1 e 2)')
    inicio = perf_counter()
    cores = guloso(grafo, ordem)
    tempo_guloso = perf_counter() - inicio
    assert validar_coloracao(grafo, cores)
    quantidade = len(set(cores))
    print('\nSAÍDA')
    print(f'Guloso: {cores} | {quantidade} cores')
    print('Conclusão do guloso:', 'encontrou uma 3-coloração.' if quantidade <= 3 else 'inconclusivo para 3-coloração.')
    inicio = perf_counter()
    solucao, estatisticas = backtracking(grafo, ordem=ordem)
    tempo_busca = perf_counter() - inicio
    if solucao is None:
        print('Backtracking: não existe coloração com até três cores.')
    else:
        assert validar_coloracao(grafo, solucao, 3)
        print(f'Backtracking: {solucao} | {len(set(solucao))} cores nesta solução')
    print('\nVértice | Guloso | Backtracking')
    for v in range(len(grafo)):
        print(f'{v:7} | {cores[v]:6} | {str(solucao[v]) if solucao is not None else "--":>12}')
    print('Verificação do guloso: válida (sem conflito nas arestas).')
    if solucao is not None:
        print('Verificação do backtracking: válida e usa no máximo 3 cores.')
    print('Busca: {tentativas} tentativas | {desfazimentos} desfazimentos | {chamadas} chamadas'.format(**estatisticas))
    print('DECISÃO EXATA:', 'SIM, o grafo é 3-colorível.' if solucao is not None else 'NÃO, o grafo não é 3-colorível.')
    if mostrar_tempos:
        print(f'Tempo guloso: {tempo_guloso:.8f} s | backtracking: {tempo_busca:.8f} s')
        print('Tempos de uma execução: variam e não constituem um benchmark.')
    return quantidade, solucao is not None, estatisticas


def ler_entrada(caminho):
    """Valida o formato antes de construir o grafo e iniciar a busca."""
    dados = json.loads(caminho.read_text(encoding='utf-8-sig'))
    if not isinstance(dados, dict) or not {'vertices', 'arestas'} <= dados.keys():
        raise ValueError('O JSON deve ser um objeto com os campos vertices e arestas.')
    if not isinstance(dados['arestas'], list) or any(
        not isinstance(e, list) or len(e) != 2 for e in dados['arestas']
    ):
        raise ValueError('arestas deve ser uma lista de pares, como [[0, 1], [1, 2]].')
    grafo = criar_grafo(dados['vertices'], dados['arestas'])
    ordem = dados.get('ordem')
    if ordem is not None and not isinstance(ordem, list):
        raise ValueError('ordem deve ser uma lista de vértices.')
    verificar_ordem(grafo, ordem)
    return grafo, ordem


def main():
    parser = argparse.ArgumentParser(description='Comparação de algoritmos de coloração de grafos.')
    origem = parser.add_mutually_exclusive_group()
    origem.add_argument('--arquivo', type=Path, help='Entrada JSON com vertices, arestas e ordem opcional.')
    origem.add_argument('--exemplo', choices=IDENTIFICADORES, help='Executa apenas um exemplo do artigo.')
    origem.add_argument('--listar', action='store_true', help='Lista os exemplos disponíveis.')
    parser.add_argument('--ordem', nargs='+', type=int, help='Ordem dos vértices; substitui a ordem do JSON. Exige um único grafo.')
    parser.add_argument('--sem-tempos', action='store_true', help='Omite tempos para uma saída reproduzível nos slides.')
    parser.add_argument('--saida', type=Path, help='Salva também a saída em um arquivo de texto UTF-8.')
    args = parser.parse_args()
    if args.listar:
        for identificador, (nome, _) in zip(IDENTIFICADORES, exemplos()):
            print(f'{identificador:10} {nome}')
        return
    if args.ordem is not None and not (args.arquivo or args.exemplo):
        parser.error('--ordem exige --arquivo ou --exemplo.')
    try:
        if args.arquivo:
            grafo, ordem = ler_entrada(args.arquivo)
            casos = [(args.arquivo.name, grafo, ordem)]
        else:
            casos = [(nome, grafo, None) for nome, grafo in exemplos()]
            if args.exemplo:
                casos = [casos[IDENTIFICADORES.index(args.exemplo)]]
        # Valida todas as entradas antes de imprimir resultados parciais.
        casos = [(nome, grafo, verificar_ordem(grafo, args.ordem if args.ordem is not None else ordem))
                 for nome, grafo, ordem in casos]
        buffer = StringIO()
        with redirect_stdout(buffer):
            print('3-COLORAÇÃO DE GRAFOS | GULOSO E BACKTRACKING')
            print('Cada posição da lista de cores corresponde ao vértice de mesmo índice.')
            resultados = []
            for nome, grafo, ordem in casos:
                resultados.append((nome, demonstrar(nome, grafo, ordem, not args.sem_tempos)))
            if len(resultados) > 1:
                print('\nRESUMO DOS CINCO CASOS DO ARTIGO')
                print(f'{"Grafo":28} | Guloso | 3-colorível | Tent./Desf./Cham.')
                for nome, (quantidade, existe, estatisticas) in resultados:
                    contadores = '{tentativas}/{desfazimentos}/{chamadas}'.format(**estatisticas)
                    print(f'{nome:28} | {quantidade:6} | {"SIM" if existe else "NÃO":11} | {contadores}')
        relatorio = buffer.getvalue()
        if args.saida:
            args.saida.write_text(relatorio, encoding='utf-8')
        print(relatorio, end='')
    except (OSError, ValueError) as erro:
        parser.error(str(erro))
    except RecursionError:
        parser.error('Grafo grande demais para a busca recursiva. Use instâncias pequenas na demonstração.')


if __name__ == '__main__':
    main()
