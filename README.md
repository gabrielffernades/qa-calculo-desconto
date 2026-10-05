# QA – Cálculo de Desconto Progressivo

> **Trabalho acadêmico.** Este repositório é a entrega do desafio prático "Auditoria e Caça aos Bugs (Testes Unitários Automatizados)" do Marco VA01 da disciplina de Qualidade de Software, do IESP Faculdades. Não é um projeto de produção.

## O desafio

Um Dev Jr. entregou a função `calcular_desconto(valor_compra, tipo_cliente)` sem testes unitários, tendo testado "de cabeça" apenas uma compra de R$ 300. A tarefa do QA é:

1. escrever os cenários de teste a partir dos critérios de aceite;
2. automatizar os testes unitários com Pytest;
3. rodar os testes contra o código original e registrar as falhas;
4. corrigir o código até todos os testes passarem.

## Critérios de aceite

A função retorna o valor do desconto em reais (R$):

| Valor da compra | Desconto base |
|---|---|
| Menor que R$ 100,00 | 0% |
| De R$ 100,00 até menos de R$ 500,00 | 10% |
| R$ 500,00 ou mais | 20% |

- Cliente `VIP` (maiúsculo ou minúsculo) recebe 5 pontos percentuais extras sobre a porcentagem base. Cliente `COMUM` não tem acréscimo.
- Teto: o desconto nunca ultrapassa R$ 200,00.

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| [`desconto.py`](desconto.py) | Código corrigido |
| [`test_desconto.py`](test_desconto.py) | Testes unitários (Pytest) |
| [`original/desconto_dev_jr.py`](original/desconto_dev_jr.py) | Código original entregue pelo Dev Jr., mantido para referência |

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

## Cenários de teste

### Desconto base (cliente COMUM)

| # | Valor da compra | Desconto esperado | O que verifica |
|---|---|---|---|
| 1 | 0 | 0,00 | Compra zerada |
| 2 | 50 | 0,00 | Faixa de 0% |
| 3 | 99,99 | 0,00 | Limite superior da faixa de 0% |
| 4 | 100 | 10,00 | Fronteira: exatamente 100 já recebe 10% |
| 5 | 100,01 | 10,00 | Logo acima da fronteira |
| 6 | 300 | 30,00 | Meio da faixa de 10% |
| 7 | 499,99 | 50,00 | Limite superior da faixa de 10% |
| 8 | 500 | 100,00 | Fronteira: exatamente 500 já recebe 20% |
| 9 | 750 | 150,00 | Faixa de 20% |

### Cliente VIP (+5%)

| # | Valor da compra | Desconto esperado | O que verifica |
|---|---|---|---|
| 10 | 50 | 2,50 | 0% vira 5% |
| 11 | 99,99 | 5,00 | 0% vira 5% no limite da faixa |
| 12 | 100 | 15,00 | Fronteira: 10% vira 15% |
| 13 | 300 | 45,00 | 10% vira 15% |
| 14 | 499,99 | 75,00 | 10% vira 15% no limite da faixa |
| 15 | 500 | 125,00 | Fronteira: 20% vira 25% |
| 16 | 600 | 150,00 | 20% vira 25% |

### Maiúsculas e minúsculas

| # | Entrada | Desconto esperado (compra de 300) |
|---|---|---|
| 17 | `"VIP"`, `"vip"`, `"Vip"`, `"vIp"`, `" vip "` | 45,00 |
| 18 | `"COMUM"`, `"comum"`, `"Comum"` | 30,00 |

### Regra de teto (R$ 200,00)

| # | Valor da compra | Tipo | Desconto esperado | O que verifica |
|---|---|---|---|---|
| 19 | 999,99 | COMUM | 200,00 | 199,998 arredonda para 200,00 |
| 20 | 1000 | COMUM | 200,00 | Exatamente no teto |
| 21 | 1000,01 | COMUM | 200,00 | Logo acima do teto |
| 22 | 5000 | COMUM | 200,00 | Muito acima do teto |
| 23 | 799,99 | VIP | 200,00 | 199,9975 arredonda para 200,00 |
| 24 | 800 | VIP | 200,00 | Exatamente no teto |
| 25 | 1000 | VIP | 200,00 | 250 limitado a 200 |
| 26 | 10000 | VIP | 200,00 | Muito acima do teto |

### Dados inesperados

Estes casos não estão descritos na regra de negócio. A decisão adotada foi rejeitar a entrada com erro em vez de devolver um desconto calculado sobre dados inválidos.

| # | Entrada | Resultado esperado |
|---|---|---|
| 27 | Valor negativo (-0,01, -100, -1000) | `ValueError` |
| 28 | Valor não numérico (`None`, `"300"`, `"abc"`, `[300]`, `True`) | `TypeError` |
| 29 | Valor `NaN` ou infinito | `ValueError` |
| 30 | Tipo de cliente não textual (`None`, `123`, `["VIP"]`) | `TypeError` |
| 31 | Tipo de cliente desconhecido (`""`, `"GOLD"`, `"PREMIUM"`, `"VIPP"`) | `ValueError` |

## Bugs encontrados no código original

1. **Fronteira dos R$ 100,00.** A condição era `valor_compra > 100`, mas a regra diz "igual ou maior". Uma compra de exatamente R$ 100,00 recebia 0% em vez de 10%. Revelado pelos cenários 4 e 12.
2. **VIP sensível a maiúsculas.** A comparação era `tipo_cliente == "VIP"`, então `"vip"` e `"Vip"` não recebiam os 5% extras. Revelado pelo cenário 17.
3. **Entradas inválidas aceitas em silêncio.** Uma compra de -100 para VIP devolvia desconto de -5,00, `True` era tratado como compra de R$ 1,00 e qualquer tipo de cliente desconhecido era tratado como COMUM. Revelado pelos cenários 27 a 31.

O teste "de cabeça" do Dev Jr. com R$ 300 caía no meio da faixa de 10%, longe de qualquer fronteira, e por isso não revelava nenhum desses problemas.

## Resultado dos testes

| Momento | Resultado |
|---|---|
| Antes da correção (código original) | 19 falharam, 30 passaram |
| Depois da correção | 49 passaram |

O histórico de commits registra as duas etapas: o primeiro commit contém o código original com os testes, e o segundo contém a correção.
