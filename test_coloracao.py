"""Testes de correção, incluindo comparação com força bruta independente."""
import itertools
import unittest

from coloracao import backtracking, criar_grafo, exemplos, guloso, validar_coloracao


class TestColoracao(unittest.TestCase):
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
