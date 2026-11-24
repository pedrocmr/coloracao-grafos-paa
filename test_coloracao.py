"""Testes de correção, incluindo comparação com força bruta independente."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from coloracao import backtracking, criar_grafo, exemplos, guloso, ler_entrada, validar_coloracao


class TestColoracao(unittest.TestCase):
    def executar_cli(self, *argumentos):
        return subprocess.run(
            [sys.executable, '-X', 'utf8', str(Path(__file__).with_name('coloracao.py')), *argumentos],
            capture_output=True, text=True, encoding='utf-8', check=False,
        )

    def test_relatorio_exportado_e_resultados_do_artigo(self):
        with tempfile.TemporaryDirectory() as pasta:
            saida = Path(pasta) / 'resultados.txt'
            processo = self.executar_cli('--sem-tempos', '--saida', str(saida))
            self.assertEqual(processo.returncode, 0, processo.stderr)
            self.assertEqual(saida.read_text(encoding='utf-8'), processo.stdout)
            self.assertNotIn('Tempo guloso:', processo.stdout)
            for contadores in ('6/0/4', '6/0/5', '48/15/16', '13/0/8', '26/3/12'):
                self.assertIn(contadores, processo.stdout)
            self.assertIn('DECISÃO EXATA: NÃO', processo.stdout)

    def test_coroa_com_ordem_alternativa_pela_cli(self):
        processo = self.executar_cli('--exemplo', 'coroa', '--sem-tempos', '--ordem',
                                    '0', '2', '4', '6', '1', '3', '5', '7')
        self.assertEqual(processo.returncode, 0, processo.stderr)
        self.assertIn('Guloso: [0, 1, 0, 1, 0, 1, 0, 1] | 2 cores', processo.stdout)
        self.assertNotIn('=== Triângulo ===', processo.stdout)

    def test_json_e_erros_de_entrada(self):
        with tempfile.TemporaryDirectory() as pasta:
            entrada = Path(pasta) / 'entrada.json'
            entrada.write_text(json.dumps({'vertices': 3, 'arestas': [[0, 1], [1, 2], [0, 2]]}), encoding='utf-8')
            processo = self.executar_cli('--arquivo', str(entrada), '--sem-tempos')
            self.assertEqual(processo.returncode, 0, processo.stderr)
            self.assertIn('Guloso: [0, 1, 2] | 3 cores', processo.stdout)
            for dados in ({}, [], {'vertices': 3, 'arestas': [[0]]},
                          {'vertices': 3, 'arestas': [], 'ordem': 42},
                          {'vertices': 3, 'arestas': [[0, 3]]}):
                entrada.write_text(json.dumps(dados), encoding='utf-8')
                with self.assertRaises(ValueError):
                    ler_entrada(entrada)
            processo = self.executar_cli('--arquivo', str(entrada))
            self.assertEqual(processo.returncode, 2)
            self.assertNotIn('Traceback', processo.stderr)
            self.assertIn('error:', processo.stderr)
        processo = self.executar_cli('--ordem', '0', '1')
        self.assertEqual(processo.returncode, 2)

    def test_todos_grafos_ate_quatro_vertices(self):
        for n in range(5):
            possiveis = list(itertools.combinations(range(n), 2))
            for mascara in range(1 << len(possiveis)):
                arestas = [e for i, e in enumerate(possiveis) if mascara & (1 << i)]
                grafo = criar_grafo(n, arestas)
                for k in (1, 2, 3):
                    existe = any(all(c[u] != c[v] for u, v in arestas)
                                 for c in itertools.product(range(k), repeat=n))
                    solucao, _ = backtracking(grafo, k)
                    self.assertEqual(solucao is not None, existe)
                    if existe:
                        self.assertTrue(validar_coloracao(grafo, solucao, k))
                self.assertTrue(validar_coloracao(grafo, guloso(grafo)))

    def test_exemplos(self):
        casos = exemplos()
        self.assertIsNone(backtracking(casos[2][1])[0])
        self.assertEqual(guloso(casos[3][1]), [0, 0, 0, 1, 1, 2, 2])
        coroa = casos[4][1]
        self.assertEqual(len(set(guloso(coroa))), 4)
        self.assertTrue(validar_coloracao(coroa, backtracking(coroa)[0], 3))
        self.assertTrue(validar_coloracao(coroa, backtracking(coroa, 2)[0], 2))
        self.assertEqual(len(set(guloso(coroa, [0, 2, 4, 6, 1, 3, 5, 7]))), 2)

    def test_entradas_e_validacao(self):
        for n, arestas in [(-1, []), (2, [(0, 2)]), (1, [(0, 0)])]:
            with self.assertRaises(ValueError):
                criar_grafo(n, arestas)
        grafo = criar_grafo(2, [(0, 1)])
        self.assertFalse(validar_coloracao(grafo, [0, 0]))
        self.assertFalse(validar_coloracao(grafo, [-1, 0]))
        self.assertFalse(validar_coloracao(grafo, [0, 3], 3))
        with self.assertRaises(ValueError):
            guloso(grafo, [0, 0])


if __name__ == '__main__':
    unittest.main()
