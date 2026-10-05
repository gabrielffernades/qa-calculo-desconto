# Resposta 2 – Cenários de teste

Cenários para `calcular_desconto(valor_compra, tipo_cliente)`, escolhidos com partição de equivalência e análise de valor limite. São 31 cenários, automatizados em 49 casos de teste em [`test_desconto.py`](../test_desconto.py).

## A) Desconto base – cliente COMUM

| Cenário | Valor da compra | Desconto esperado | O que verifica |
|---|---|---|---|
| CT01 | R$ 0,00 | R$ 0,00 | Compra zerada |
| CT02 | R$ 50,00 | R$ 0,00 | Faixa de 0% |
| CT03 | R$ 99,99 | R$ 0,00 | Limite superior da faixa de 0% |
| CT04 | R$ 100,00 | R$ 10,00 | Fronteira: exatamente 100 já recebe 10% |
| CT05 | R$ 100,01 | R$ 10,00 | Logo acima da fronteira |
| CT06 | R$ 300,00 | R$ 30,00 | Meio da faixa de 10% |
| CT07 | R$ 499,99 | R$ 50,00 | Limite superior da faixa de 10% |
| CT08 | R$ 500,00 | R$ 100,00 | Fronteira: exatamente 500 já recebe 20% |
| CT09 | R$ 750,00 | R$ 150,00 | Faixa de 20% |

## B) Cliente VIP – 5% extras sobre a porcentagem base

| Cenário | Valor da compra | Desconto esperado | O que verifica |
|---|---|---|---|
| CT10 | R$ 50,00 | R$ 2,50 | 0% vira 5% |
| CT11 | R$ 99,99 | R$ 5,00 | 0% vira 5% no limite da faixa |
| CT12 | R$ 100,00 | R$ 15,00 | Fronteira: 10% vira 15% |
| CT13 | R$ 300,00 | R$ 45,00 | 10% vira 15% |
| CT14 | R$ 499,99 | R$ 75,00 | 10% vira 15% no limite da faixa |
| CT15 | R$ 500,00 | R$ 125,00 | Fronteira: 20% vira 25% |
| CT16 | R$ 600,00 | R$ 150,00 | 20% vira 25% |

## C) Tipo de cliente em maiúsculas e minúsculas

Todos com compra de R$ 300,00.

| Cenário | Tipo informado | Desconto esperado |
|---|---|---|
| CT17 | `"VIP"`, `"vip"`, `"Vip"`, `"vIp"` e `" vip "` (com espaços) | R$ 45,00 em todos |
| CT18 | `"COMUM"`, `"comum"` e `"Comum"` | R$ 30,00 em todos |

## D) Regra de teto – desconto máximo de R$ 200,00

| Cenário | Valor da compra | Tipo | Desconto esperado | O que verifica |
|---|---|---|---|---|
| CT19 | R$ 999,99 | COMUM | R$ 200,00 | 199,998 arredonda para 200,00 |
| CT20 | R$ 1.000,00 | COMUM | R$ 200,00 | Exatamente no teto |
| CT21 | R$ 1.000,01 | COMUM | R$ 200,00 | Logo acima do teto |
| CT22 | R$ 5.000,00 | COMUM | R$ 200,00 | Muito acima do teto |
| CT23 | R$ 799,99 | VIP | R$ 200,00 | 199,9975 arredonda para 200,00 |
| CT24 | R$ 800,00 | VIP | R$ 200,00 | Exatamente no teto |
| CT25 | R$ 1.000,00 | VIP | R$ 200,00 | 250,00 limitado a 200,00 |
| CT26 | R$ 10.000,00 | VIP | R$ 200,00 | Muito acima do teto |

## E) Dados inesperados

Estes casos não estão descritos na regra de negócio. A decisão adotada foi rejeitar a entrada com erro, em vez de calcular desconto sobre dado inválido.

| Cenário | Entrada | Resultado esperado |
|---|---|---|
| CT27 | Valor negativo (-0,01, -100 e -1000) | `ValueError` |
| CT28 | Valor não numérico (`None`, `"300"`, `"abc"`, `[300]` e `True`) | `TypeError` |
| CT29 | Valor `NaN` ou infinito | `ValueError` |
| CT30 | Tipo de cliente não textual (`None`, `123` e `["VIP"]`) | `TypeError` |
| CT31 | Tipo de cliente desconhecido (`""`, `"GOLD"`, `"PREMIUM"` e `"VIPP"`) | `ValueError` |
