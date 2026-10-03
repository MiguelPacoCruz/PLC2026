## TPC2: Conversor de Markdown para HTML

Pretende-se criar um conversor de Markdown para HTML para os elementos descritos na "Basic Syntax" da Cheat Sheet.

Vamos começar por escrever a expressão regular referente a cada elemento Markdown. Depois de os testar, as expressões foram corrigidas, e indica-se em cada secção o que mudou.

### Cabeçalhos

A primeira versão, ``#\w``, encontrava apenas headers com um "#" e sem espaço depois. A versão final é:

``(#+) (.*)``

O primeiro grupo de captura apanha os `#`, e o seu comprimento (`len(m.group(1))`) dá o nível do cabeçalho, ou seja, o N da tag `<hN>`. O segundo grupo apanha o texto.

### Bold

``\*{2}(.*?)\*{2}``

A primeira versão usava `\w*`, que não aceita espaços, logo `**mais do que uma palavra**` não era convertido. Passou a `.*?`, que aceita qualquer carácter e é *lazy*: assim, `**a** e **b**` dá dois negritos e não um único a engolir tudo o que está entre o primeiro e o último `**`.

### Itálico

``\*{1}(.*?)\*{1}``

Muito semelhante ao Bold, mas com um só asterisco. Como o Bold é aplicado primeiro, os `**` já foram consumidos quando o itálico é processado. Se a ordem fosse inversa, os `**` seriam lidos como dois itálicos vazios.

### Lista numerada

``^1\. (.*)``

Uma lista em Markdown pode começar num número diferente de 1, mas para este trabalho assumimos que começa sempre em 1. A lista é detetada com `re.search` e a flag `re.MULTILINE`, que faz o `^` valer para o início de cada linha (com `re.match` só se testaria o início do texto, e a lista falharia quando viesse depois de um cabeçalho ou parágrafo).

A primeira linha abre o `<ol>`, e as seguintes (`2.`, `3.`, …) são convertidas uma a uma em `<li>`, com a última a fechar o `</ol>`.

### Link: [texto](endereço URL)

``([^!])\[(?P<texto>.*)\]\((?P<url>[\w\/:\.]*)\)``

Em vez de grupos numerados, usámos grupos nomeados (`texto` e `url`), o que torna a substituição mais legível. O `[^!]` à frente garante que uma imagem não é confundida com um link.

### Imagem: ![texto alternativo](path para a imagem)

``!\[(?P<texto>.*)\]\((?P<url>[\w\/:\.]*)\)``

Igual ao link, mas começa com `!`. Como a imagem tem de ser distinguida do link, o link só é aplicado a `[` que não venham logo depois de um `!`.

### Implementação

O conversor está implementado em [`conversor.py`](conversor.py). A função `markdown_to_html` recebe o texto completo e aplica as expressões regulares com `re.sub`, pela ordem indicada na tabela:

| Ordem | Elemento | Expressão regular | Resultado |
|---|---|---|---|
| 1 | Negrito | `\*{2}(.*?)\*{2}` | `<b>…</b>` |
| 2 | Itálico | `\*{1}(.*?)\*{1}` | `<i>…</i>` |
| 3 | Link | `([^!])\[(?P<texto>.*)\]\((?P<url>[\w\/:\.]*)\)` | `<a href="url">texto</a>` |
| 4 | Imagem | `!\[(?P<texto>.*)\]\((?P<url>[\w\/:\.]*)\)` | `<img src="url" alt="texto"/>` |
| 5 | Cabeçalho | `(#+) (.*)` | `<hN>…</hN>`, com N = nº de `#` |
| 6 | Lista numerada | `^1\. (.*)` | `<ol>` com um `<li>` por item |

A ordem é importante: o negrito tem de vir antes do itálico, para que os `**` não sejam consumidos como dois itálicos.

O programa recebe o ficheiro `.md` e o nome do `.html` de saída na linha de comandos:

`python conversor.py <input.md> <output.html>`

### Testes

Os testes estão em [`test.py`](test.py). O script corre o conversor sobre cada ficheiro de `inputs/`, compara o resultado com o respetivo ficheiro de `expected/` e indica quais os testes que passaram e quais falharam. Com a flag `-v` mostra o esperado e o obtido completos.