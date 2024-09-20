# StaticallyTypedScript

Alunos: Caio Padilha Aguiar, Kevin Zhou Zheng

## Exemplos de uso

- Tipos: `int`, `float`, `bool`

- Finalização de comandos: `;`

- Declaração de variáveis: `let <identificador>: <tipo> = <expressão>;`
> let x: int = 10;

- Comentários: `// comentário`

- Print: `print(expressão);`
> print(<expressão>);

- While loop: `while (cond) { <bloco> }`
> while (i < n) {
>    print(i);
>    i = i + 1;
>}

- If-else: `if (cond) { <bloco> } else { <bloco> }`
> if (cond) {
>    // alguma coisa
> } else if (outraCond) {
>    // outra coisa
> } else {
>    // outra outra coisa
>}

- Break: `break;`
> while (cond) {
>    // alguma coisa
>    break;
>}

- Operadores:
 * soma: `a + b`
 * subtração: `a - b`
 * multiplicação: `a * b`
 * divisão: `a / b`
 * menor que: `a < b`
 * maior que: `a > b`
 * igual: `a == b`
 * diferente: `a != b`
 * e: `a && b`
 * ou: `a || b`
 * negação: `!a`


## Gramática

A gramática do script está descrita no arquivo [grammar.md](grammar/grammar.md).
