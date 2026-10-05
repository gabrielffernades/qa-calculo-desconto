# Resposta 3 – Bugs encontrados e como os testes os revelaram

Os 49 casos de teste foram executados contra o código original: 19 falharam e 30 passaram. As falhas apontaram três problemas.

## Bug 1 – Fronteira dos R$ 100,00

O código usava `valor_compra > 100`, mas a regra diz que compras de valor "igual ou maior que R$ 100,00" recebem 10%. Uma compra de exatamente R$ 100,00 não entrava em nenhuma faixa e ficava com 0% de desconto base.

| Entrada | Retorno do original | Esperado |
|---|---|---|
| R$ 100,00, COMUM | R$ 0,00 | R$ 10,00 |
| R$ 100,00, VIP | R$ 5,00 | R$ 15,00 |

**Correção:** `>` trocado por `>=`.

## Bug 2 – VIP sensível a maiúsculas e minúsculas

O código comparava com `tipo_cliente == "VIP"`, mas a regra diz que o VIP vale independentemente de estar em maiúsculo ou minúsculo. Qualquer variação era tratada como cliente comum e perdia os 5% extras.

| Entrada | Retorno do original | Esperado |
|---|---|---|
| R$ 300,00, `"vip"` | R$ 30,00 | R$ 45,00 |
| R$ 300,00, `"Vip"` | R$ 30,00 | R$ 45,00 |
| R$ 300,00, `"vIp"` | R$ 30,00 | R$ 45,00 |
| R$ 300,00, `" vip "` | R$ 30,00 | R$ 45,00 |

**Correção:** a entrada é normalizada com `strip()` e `upper()` antes da comparação.

## Bug 3 – Dados inválidos aceitos em silêncio

O código não validava as entradas e devolvia um resultado mesmo quando o dado não fazia sentido:

- **Valor negativo:** compra de -100 para VIP retornava desconto de R$ -5,00.
- **Booleano:** `True` era tratado como compra de R$ 1,00.
- **NaN:** retornava `NaN` como desconto.
- **Tipo de cliente desconhecido ou não textual:** `"GOLD"`, `"PREMIUM"`, texto vazio, `None` e `123` eram tratados como COMUM sem nenhum aviso.

**Correção:** validação no início da função, lançando `ValueError` ou `TypeError` para essas entradas. Como a regra de negócio não define esses casos, essa foi uma decisão de projeto: é mais seguro rejeitar o dado do que calcular desconto em cima dele.

## Como a escolha dos valores revelou os erros

O Dev Jr. testou apenas R$ 300,00 com o tipo escrito da forma esperada. Esse valor fica no meio da faixa de 10%, longe de qualquer limite, e por isso passa mesmo com os três bugs presentes.

Duas técnicas guiaram a escolha dos valores:

1. **Análise de valor limite.** Foram testados os pontos exatos de troca de faixa e seus vizinhos (99,99 / 100 / 100,01 e 499,99 / 500), além dos limites do teto (999,99 / 1000 / 1000,01 para COMUM e 799,99 / 800 para VIP). Foi o valor exato de R$ 100,00 que revelou o Bug 1: com 99,99 e 100,01 o código original acertava, e o erro só existia naquele único ponto.
2. **Partição de equivalência.** As entradas foram divididas em classes válidas (cada faixa de valor, VIP e COMUM) e inválidas (negativos, não numéricos, tipos desconhecidos), com representantes de cada uma. As variações de escrita do VIP revelaram o Bug 2 e as classes inválidas revelaram o Bug 3.

Os testes das fronteiras de R$ 500,00 e do teto de R$ 200,00 passaram no código original, o que confirma que essas partes já estavam corretas. Após as correções, os 49 testes passaram.

## Distribuição das 19 falhas

| Bug | Testes que falharam |
|---|---|
| Bug 1 – fronteira dos R$ 100,00 | 2 |
| Bug 2 – VIP em minúsculas | 4 |
| Bug 3 – dados inválidos | 13 |
