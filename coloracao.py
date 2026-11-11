"""Projeto de 3-coloração: guloso sequencial e backtracking.

Referência: Paulo Feofiloff, IME-USP, Coloração de vértices.
https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/vertex-coloring.html
Guloso adaptado da função em C UGRAPHseqColoring; backtracking implementado
a partir da descrição do exercício de busca em profundidade da mesma fonte.
"""

import argparse
import json
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


def demonstrar(nome, grafo, ordem=None):
    print(f'\n=== {nome} ===')
    print(f'Vértices: {len(grafo)} | Arestas: {sum(map(len, grafo)) // 2}')
    print('Ordem:', verificar_ordem(grafo, ordem))
    inicio = perf_counter()
    cores = guloso(grafo, ordem)
    tempo_guloso = perf_counter() - inicio
    assert validar_coloracao(grafo, cores)
    quantidade = len(set(cores))
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
    print('Busca:', estatisticas)
    print(f'Tempo guloso: {tempo_guloso:.8f} s | backtracking: {tempo_busca:.8f} s')
    print('Tempos de uma execução: variam e não constituem um benchmark.')


def main():
    parser = argparse.ArgumentParser(description='Comparação de algoritmos de coloração de grafos.')
    parser.add_argument('--arquivo', type=Path, help='Entrada JSON com vertices, arestas e ordem opcional.')
    args = parser.parse_args()
    if args.arquivo:
        dados = json.loads(args.arquivo.read_text(encoding='utf-8'))
        demonstrar(args.arquivo.name, criar_grafo(dados['vertices'], dados['arestas']), dados.get('ordem'))
    else:
        for nome, grafo in exemplos():
            demonstrar(nome, grafo)


if __name__ == '__main__':
    main()
