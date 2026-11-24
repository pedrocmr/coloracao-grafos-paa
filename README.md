# 3-Coloração de Grafos — Guloso e Backtracking

Implementação do trabalho **Coloração de Vértices em Grafos: 3-Coloração com Algoritmo Guloso e Backtracking**. O programa recebe um grafo simples não dirigido e compara duas abordagens para decidir se seus vértices podem receber **até três cores**, sem que vértices adjacentes tenham a mesma cor.

## Como executar

Requer Python 3, sem bibliotecas externas. Abra o terminal na pasta do projeto:

```sh
python coloracao.py --sem-tempos
```

O programa mostra as entradas, as cores de cada vértice, as verificações, os contadores da busca e uma tabela final dos cinco casos do artigo. `--sem-tempos` omite as medições de tempo e deixa a saída reproduzível. Para incluir os tempos, execute `python coloracao.py`.

No Windows, se `python` não estiver disponível, use `py`. Se houver problemas com acentos no terminal, use `python -X utf8` no início do comando.

### Executar um exemplo específico

Liste os exemplos disponíveis e escolha um deles:

```sh
python coloracao.py --listar
python coloracao.py --exemplo triangulo --sem-tempos
python coloracao.py --exemplo k4 --sem-tempos
python coloracao.py --exemplo coroa --sem-tempos
```

Para testar outra ordem de processamento no grafo coroa:

```sh
python coloracao.py --exemplo coroa --ordem 0 2 4 6 1 3 5 7 --sem-tempos
```

### Executar com um arquivo JSON

Use a entrada de exemplo em [entrada.json](entrada.json) ou crie seu próprio arquivo no formato descrito abaixo:

```sh
python coloracao.py --arquivo entrada.json --sem-tempos
```

### Entrada e saída do triângulo

Conteúdo de [entrada.json](entrada.json):

```json
{
  "vertices": 3,
  "arestas": [[0, 1], [1, 2], [0, 2]],
  "ordem": [0, 1, 2]
}
```

Saída completa do comando anterior:

```text
3-COLORAÇÃO DE GRAFOS | GULOSO E BACKTRACKING
Cada posição da lista de cores corresponde ao vértice de mesmo índice.

=== entrada.json ===
ENTRADA
Vértices: 3 | Arestas: 3
Arestas: [(0, 1), (0, 2), (1, 2)]
Ordem: [0, 1, 2]
Limite do backtracking: 3 cores (0, 1 e 2)

SAÍDA
Guloso: [0, 1, 2] | 3 cores
Conclusão do guloso: encontrou uma 3-coloração.
Backtracking: [0, 1, 2] | 3 cores nesta solução

Vértice | Guloso | Backtracking
      0 |      0 |            0
      1 |      1 |            1
      2 |      2 |            2
Verificação do guloso: válida (sem conflito nas arestas).
Verificação do backtracking: válida e usa no máximo 3 cores.
Busca: 6 tentativas | 0 desfazimentos | 4 chamadas
DECISÃO EXATA: SIM, o grafo é 3-colorível.
```

As cores são rótulos inteiros a partir de zero. `[0, 1, 2]` indica cor 0 no vértice 0, cor 1 no vértice 1 e cor 2 no vértice 2. Mesmo ao mudar a ordem de processamento, as listas e a tabela continuam organizadas pelo índice do vértice. `--` na coluna do backtracking significa que nenhuma solução foi encontrada após esgotar a busca.

### Resultados esperados

Resultados executados na ordem natural, correspondentes à tabela do artigo:

| Grafo | Vértices | Arestas | Cores do guloso | Cores do backtracking | É 3-colorível? | Tentativas / Desfazimentos / Chamadas |
| --- | ---: | ---: | ---: | --- | :---: | --- |
| Triângulo | 3 | 3 | 3 | 3 | Sim | 6 / 0 / 4 |
| Ciclo de quatro vértices | 4 | 4 | 2 | 2 | Sim | 6 / 0 / 5 |
| Completo K4 | 4 | 6 | 4 | Sem solução | Não | 48 / 15 / 16 |
| Exemplo C da referência | 7 | 6 | 3 | 3 | Sim | 13 / 0 / 8 |
| Coroa com oito vértices | 8 | 12 | 4 | 3 | Sim | 26 / 3 / 12 |

O exemplo C admite duas cores, embora ambos retornem três nessa ordem. A coroa também admite duas cores. Com a ordem `0 2 4 6 1 3 5 7`, ambos retornam `[0, 1, 0, 1, 0, 1, 0, 1]`, com 12 tentativas, zero desfazimentos e nove chamadas no backtracking.

Relatórios de exemplo para conferir os resultados:

- [Resultados dos cinco casos](resultados/artigo.txt).
- [Coroa com os pares primeiro](resultados/coroa_pares_primeiro.txt).

Para gerar novamente ou salvar outra execução:

```sh
python coloracao.py --sem-tempos --saida resultados/artigo.txt
python coloracao.py --exemplo coroa --ordem 0 2 4 6 1 3 5 7 --sem-tempos --saida resultados/coroa_pares_primeiro.txt
```

`--saida` grava exatamente o relatório mostrado no terminal, em UTF-8. A pasta de destino precisa existir. O arquivo indicado é sobrescrito.

## Formato das entradas e opções

- `vertices`: inteiro não negativo; os vértices vão de 0 a n − 1.
- `arestas`: lista de pares. As arestas são não dirigidas; repetições são armazenadas uma única vez. Laços e vértices fora do intervalo são rejeitados.
- `ordem`: opcional; deve listar cada vértice exatamente uma vez. Se omitida, usa-se a ordem natural. `--ordem` substitui a ordem do JSON.

Entradas prontas para abrir no editor e executar com `--arquivo`:

| Arquivo | Caso |
| --- | --- |
| [triangulo.json](exemplos/triangulo.json) | Triângulo |
| [ciclo4.json](exemplos/ciclo4.json) | Ciclo de quatro vértices |
| [k4.json](exemplos/k4.json) | Completo K4 |
| [referencia.json](exemplos/referencia.json) | Exemplo C |
| [coroa.json](exemplos/coroa.json) | Coroa na ordem natural |
| [coroa_pares_primeiro.json](exemplos/coroa_pares_primeiro.json) | Mesmo grafo coroa, com os pares primeiro |

```sh
python coloracao.py --listar
python coloracao.py --help
python coloracao.py --arquivo exemplos/coroa_pares_primeiro.json --sem-tempos
```

`--arquivo` e `--exemplo` são alternativas. `--ordem` exige a seleção de um único grafo. Entradas inválidas geram mensagem de erro e código de saída 2. Uma resposta negativa para a 3-coloração é um resultado normal, com código 0.

## Algoritmos e interpretação

O guloso sequencial usa a menor cor disponível, criando uma nova quando necessário. Se usar até três cores, encontrou uma solução. Se usar mais, o resultado é inconclusivo para a decisão da 3-coloração.

O backtracking tenta completar uma coloração parcial usando apenas 0, 1 e 2. Retorna a primeira solução encontrada, não necessariamente mínima. Se esgotar a busca sem solução, o grafo não é 3-colorível. A função de validação verifica independentemente se as cores respeitam todas as arestas.

Tentativas contam cada cor candidata examinada. Desfazimentos contam atribuições válidas removidas após uma busca descendente sem sucesso. Chamadas incluem a raiz e, quando há solução, a chamada de sucesso. Esses contadores descrevem o backtracking; não são uma medida comum para comparar diretamente com o guloso.

## Testes

```sh
python -m unittest -v
```

Os testes em [test_coloracao.py](test_coloracao.py) incluem comparação com força bruta para todos os grafos simples de até quatro vértices, os casos do artigo, mudança de ordem na coroa, leitura e rejeição de entradas, execução da interface e fidelidade do relatório exportado. Os algoritmos e a interface estão em [coloracao.py](coloracao.py).

## Crédito e uso de IA

Referência: Feofiloff, Paulo. [Coloração de vértices](https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/vertex-coloring.html). Algoritmos para Grafos, IME-USP. Atualização indicada no material fornecido: 20 set. 2019.

O guloso foi adaptado da função em C UGRAPHseqColoring. O backtracking foi implementado com base na descrição do exercício da mesma página. O caso coroa, a interface de entrada e os testes complementam os exemplos da fonte.

Utilizamos o Codex como apoio à implementação, documentação e testes, sob responsabilidade da equipe.

Modelo: não informado no material original disponível.

Versão: não informada no material original disponível.
