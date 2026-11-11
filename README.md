# Projeto: 3-Coloração de Grafos em Python

## Executar

Requer Python 3. Não utiliza bibliotecas externas.

Abra um terminal nesta pasta e execute:

```text
python coloracao.py
python coloracao.py --arquivo entrada.json
python -m unittest -v
```

Sem argumentos, o programa demonstra cinco grafos. O JSON permite definir o
número de vértices, as arestas e, opcionalmente, a ordem de processamento.
Os vértices são numerados de 0 até n-1. Arestas são não dirigidas;
laços são rejeitados e arestas repetidas são armazenadas uma única vez.
As cores são números a partir de 0.

## O que cada algoritmo responde

O guloso sequencial usa a menor cor disponível, criando uma nova quando
necessário. Se usar até três cores, encontra uma solução do projeto. Se usar
mais, não permite concluir que o grafo não é 3-colorível.

O backtracking tenta completar uma coloração parcial usando somente 0, 1 e 2.
Retorna a primeira solução encontrada, não necessariamente uma coloração mínima.
Se esgotar a busca sem solução, o grafo não é 3-colorível.

## Demonstração

1. Triângulo: três cores são necessárias.
2. Ciclo de quatro vértices: admite duas cores.
3. K4: não admite três cores, pois todos os quatro vértices são adjacentes entre si.
4. Exemplo C da fonte: o guloso usa três cores, embora o grafo admita duas.
5. Coroa com oito vértices: o guloso usa quatro cores na ordem alternada;
   o backtracking encontra uma solução com até três. O grafo admite duas,
   o que também é verificado nos testes. Processar primeiro os vértices pares
   e depois os ímpares faz o guloso usar apenas duas cores.

Tentativas contam cada cor candidata examinada. Desfazimentos contam atribuições
válidas removidas após uma busca descendente sem sucesso. Chamadas incluem a raiz
e a chamada de sucesso. Esses contadores descrevem o backtracking, não são uma
medida comum de trabalho para comparar diretamente com o guloso.

## Análise de complexidade

Sejam n o número de vértices, m o número de arestas e Δ o grau máximo.
Com conjuntos de Python e custo médio constante de consulta, esta implementação
gulosa tem tempo esperado O(n+m): construir as cores proibidas e buscar a menor
cor disponível custa O(grau(v)+1) por vértice. Essa análise corresponde à versão
em Python, que não reinicializa um vetor de todas as cores a cada vértice.

O backtracking é exponencial no pior caso. Há até 3^n atribuições completas;
incluindo as verificações de vizinhos, um limite superior é O((Δ+1) * 3^n).
Podas podem reduzir a busca, mas não eliminam o pior caso exponencial.
O armazenamento do grafo é O(n+m); a coloração e a pilha recursiva usam O(n).
Grafos grandes podem atingir o limite de recursão do Python ou demandar tempo
impraticável. A demonstração foi planejada para instâncias pequenas.

Os tempos impressos são medições isoladas e não sustentam conclusões gerais de
desempenho.

## Crédito e uso de IA

Referência: Feofiloff, Paulo. Coloração de vértices. Algoritmos para Grafos,
IME-USP. Atualização indicada no material fornecido: 20 set. 2019.
https://www.ime.usp.br/~pf/algoritmos_para_grafos/aulas/vertex-coloring.html

O guloso foi adaptado da função em C UGRAPHseqColoring. O backtracking foi
implementado com base na descrição do exercício da mesma página. O caso coroa,
a interface de entrada e os testes complementam os exemplos da fonte.

Utilizamos o Codex como apoio à implementação, documentação e testes, sob
responsabilidade da equipe.

Modelo: não informado no material disponível.

Versão: não informada no material disponível.
