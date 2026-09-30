Pretende-se criar um conversor de MarkDown para HTML para os elementos descritos na "Basic Syntax" da Cheat Sheet.

Vamos começar por escrever a expressão regular referente a cada elemento markdown:

### Cabeçalhos
A expressão regular seguinte encontra headers com apenas um "#".

``#\w``

No entanto queremos contá-los, pois é relevante para o a tag em HTML. Podemos obter este número através de um grupo de captura e do span desse grupo.

### Bold
Este é um exemplo mais simples. Sendo representado pela expressão regular:

``\*{2}\w*\*{2}``

### Itálico
Muito semelhante ao Bold.

``\*\*\w*\*\*``

### Lista numerada
Uma lista em MarkDown pode começar num número sem ser 1? Se não pode, a verificar em python, através novamente de grupos de captura.

``^\d\.[\w ,.]*``

### Link: [texto](endereço URL)
Através dos grupos de captura, conseguimos obter, no primeiro o texto, e no segundo o endereço URL.

``(\[.*\])(\([\w\/:\.]*\))``

### Imagem: ![texto alternativo](path para a imagem)
A primeira parte, apenas de texto é trivial, o segundo grupo começa com o caracter !, e dentro de parenteses retos, já o terceiro é análogo ao endereço do link.

``(.*)(!\[.*\])(\([\w\/:\.]*\))``

Nota: por enquanto, a maior parte da captura do texto está opcional, através do *, questionar ao professor sobre a necessiade do texto?

Agora que temos as expressões regulares criadas, vamos implementá-las em python através da biblioteca "re".