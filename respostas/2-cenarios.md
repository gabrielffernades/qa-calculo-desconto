# Resposta 2 – Cenários de teste

Cenários para `calcular_desconto(valor_compra, tipo_cliente)`, escolhidos com partição de equivalência e análise de valor limite. São 34 cenários, automatizados em 52 casos de teste em [`test_desconto.py`](../test_desconto.py).

## A) Desconto base – cliente COMUM

| Cenário | Valor da compra | Desconto esperado | O que verifica |
|---|---|---|---|
| CT01 | R$ 0,00 | R$ 0,00 | Compra zerada |
| CT02 | R$ 50,00 | R$ 0,00 | Meio da faixa de 0% |
| CT03 | R$ 99,99 | R$ 0,00 | Imediatamente antes de R$ 100,00 |
| CT04 | R$ 100,00 | R$ 10,00 | Exatamente R$ 100,00: já recebe 10% |
| CT05 | R$ 100,01 | R$ 10,00 | Imediatamente depois de R$ 100,00 |
| CT06 | R$ 300,00 | R$ 30,00 | Meio da faixa de 10% |
| CT07 | R$ 499,99 | R$ 50,00 | Imediatamente antes de R$ 500,00 |
| CT08 | R$ 500,00 | R$ 100,00 | Exatamente R$ 500,00: já recebe 20% |
| CT09 | R$ 500,01 | R$ 100,00 | Imediatamente depois de R$ 500,00 |
| CT10 | R$ 750,00 | R$ 150,00 | Meio da faixa de 20% |

## B) Cliente VIP – 5% extras sobre a porcentagem base

| Cenário | Valor da compra | Desconto esperado | O que verifica |
|---|---|---|---|
| CT11 | R$ 50,00 | R$ 2,50 | 0% vira 5% |
| CT12 | R$ 99,99 | R$ 5,00 | Imediatamente antes de R$ 100,00: 5% |
| CT13 | R$ 100,00 | R$ 15,00 | Exatamente R$ 100,00: 10% vira 15% |
| CT14 | R$ 100,01 | R$ 15,00 | Imediatamente depois de R$ 100,00: 15% |
| CT15 | R$ 300,00 | R$ 45,00 | 10% vira 15% |
| CT16 | R$ 499,99 | R$ 75,00 | Imediatamente antes de R$ 500,00: 15% |
| CT17 | R$ 500,00 | R$ 125,00 | Exatamente R$ 500,00: 20% vira 25% |
| CT18 | R$ 500,01 | R$ 125,00 | Imediatamente depois de R$ 500,00: 25% |
| CT19 | R$ 600,00 | R$ 150,00 | 20% vira 25% |

## C) Tipo de cliente em maiúsculas e minúsculas

Todos com compra de R$ 300,00.

| Cenário | Tipo informado | Desconto esperado |
|---|---|---|
| CT20 | `"VIP"`, `"vip"`, `"Vip"`, `"vIp"` e `" vip "` (com espaços) | R$ 45,00 em todos |
| CT21 | `"COMUM"`, `"comum"` e `"Comum"` | R$ 30,00 em todos |

## D) Regra de teto – desconto máximo de R$ 200,00

| Cenário | Valor da compra | Tipo | Desconto esperado | O que verifica |
|---|---|---|---|---|
| CT22 | R$ 999,99 | COMUM | R$ 200,00 | 199,998 arredonda para 200,00 |
| CT23 | R$ 1.000,00 | COMUM | R$ 200,00 | Exatamente no teto |
| CT24 | R$ 1.000,01 | COMUM | R$ 200,00 | Imediatamente acima do teto |
| CT25 | R$ 5.000,00 | COMUM | R$ 200,00 | Muito acima do teto |
| CT26 | R$ 799,99 | VIP | R$ 200,00 | 199,9975 arredonda para 200,00 |
| CT27 | R$ 800,00 | VIP | R$ 200,00 | Exatamente no teto |
| CT28 | R$ 1.000,00 | VIP | R$ 200,00 | 250,00 limitado a 200,00 |
| CT29 | R$ 10.000,00 | VIP | R$ 200,00 | Muito acima do teto |

## E) Dados inesperados

Estes casos não estão descritos na regra de negócio. A decisão adotada foi rejeitar a entrada com erro, em vez de calcular desconto sobre dado inválido.

| Cenário | Entrada | Resultado esperado |
|---|---|---|
| CT30 | Valor negativo (-0,01, -100 e -1000) | `ValueError` |
| CT31 | Valor não numérico (`None`, `"300"`, `"abc"`, `[300]` e `True`) | `TypeError` |
| CT32 | Valor `NaN` ou infinito | `ValueError` |
| CT33 | Tipo de cliente não textual (`None`, `123` e `["VIP"]`) | `TypeError` |
| CT34 | Tipo de cliente desconhecido (`""`, `"GOLD"`, `"PREMIUM"` e `"VIPP"`) | `ValueError` |
