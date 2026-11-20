# Gerenciamento de Biblioteca (Tema 5)

**Aluno:** Natanael Antônio Dos Reis Santana | **RA:** 251-002126

Sistema de terminal em Python que gerencia uma biblioteca usando as quatro estruturas da disciplina: Lista, Fila, Pilha e Árvore. Os dados podem ser salvos e carregados de um arquivo texto.

## Como executar

Com o Python 3 instalado, abra o terminal na pasta do projeto e rode:

```bash
python main.py
```

O sistema começa vazio. No menu principal, use **5. Salvar dados** para gravar em `dados_sistema.txt` e **6. Carregar dados** para recuperar o que foi salvo. Não é preciso instalar nenhuma biblioteca.

## Por que escolhi cada estrutura

**Lista (leitores).** Preciso consultar, editar e remover qualquer leitor, não só o primeiro ou o último. Por isso usei uma `list` de dicionários (`id` e `nome`) e busco cada leitor pelo ID.

**Fila (reservas).** Quem reserva um livro primeiro deve ser atendido primeiro, então a regra é FIFO. Usei `collections.deque`: `append` coloca a reserva no fim e `popleft` atende a do início. Escolhi `deque` porque `popleft` é mais eficiente que `pop(0)` de uma lista.

**Pilha (livros devolvidos).** Os livros devolvidos ficam empilhados no balcão e o último a chegar é o primeiro a ser triado, ou seja, LIFO. Usei uma `list`, com `append` para empilhar e `pop` para triar, sempre no topo.

**Árvore (acervo).** O acervo se organiza em áreas, subáreas e assuntos, que é uma hierarquia. Como o Python não tem árvore pronta, usei dicionários aninhados: cada chave é um nó e o valor guarda seus filhos.

## Menu

| Opção | Estrutura | O que faz |
|---|---|---|
| 1. Leitores | Lista | cadastrar, listar, atualizar, remover |
| 2. Reservas | Fila | reservar, listar, atualizar, atender |
| 3. Devolvidos | Pilha | devolver, listar, atualizar topo, triar |
| 4. Acervo | Árvore | adicionar, listar, renomear, remover |
| 5 e 6 | Arquivo | salvar e carregar dados |

Na árvore, o caminho é digitado com `>`, por exemplo: `Ciências > Computação > Python`.

## Formato do arquivo `dados_sistema.txt`

Cada linha começa com o nome da estrutura, seguido dos campos separados por `|`:

```
LISTA|1|Maria Souza
FILA|O Pequeno Príncipe|Maria Souza
PILHA|Dom Casmurro
ARVORE|Ciências|Computação|Python
```

Na fila, a primeira linha é o início; na pilha, a última é o topo. A árvore é gravada como caminhos completos até as folhas e remontada ao carregar. Se o usuário digitar `|` em algum campo, o programa troca por `/` para não quebrar o arquivo.
