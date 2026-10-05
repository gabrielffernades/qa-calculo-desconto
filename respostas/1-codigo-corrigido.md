# Resposta 1 – Código principal corrigido

O código corrigido está em [`desconto.py`](../desconto.py). O código original do Dev Jr. está em [`original/desconto_dev_jr.py`](../original/desconto_dev_jr.py).

```python
import math


def calcular_desconto(valor_compra, tipo_cliente):
    # Validação dos dados de entrada
    if isinstance(valor_compra, bool) or not isinstance(valor_compra, (int, float)):
        raise TypeError("valor_compra deve ser numérico")
    if not math.isfinite(valor_compra):
        raise ValueError("valor_compra deve ser um número finito")
    if valor_compra < 0:
        raise ValueError("valor_compra não pode ser negativo")
    if not isinstance(tipo_cliente, str):
        raise TypeError("tipo_cliente deve ser um texto")

    tipo_cliente = tipo_cliente.strip().upper()
    if tipo_cliente not in ("VIP", "COMUM"):
        raise ValueError("tipo_cliente deve ser 'VIP' ou 'COMUM'")

    desconto = 0

    # Validação do desconto base
    if valor_compra >= 100 and valor_compra < 500:
        desconto = 0.10
    elif valor_compra >= 500:
        desconto = 0.20

    # Validação do cliente VIP
    if tipo_cliente == "VIP":
        desconto += 0.05

    valor_desconto = valor_compra * desconto

    # Regra do Teto de R$ 200,00
    if valor_desconto > 200:
        valor_desconto = 200

    return round(valor_desconto, 2)
```

## O que mudou em relação ao original

| Trecho | Antes | Depois |
|---|---|---|
| Faixa de 10% | `valor_compra > 100` | `valor_compra >= 100` |
| Cliente VIP | comparação direta com `"VIP"` | entrada normalizada com `strip()` e `upper()` |
| Entradas inválidas | aceitas sem validação | rejeitadas com `ValueError` ou `TypeError` |

O motivo de cada mudança está em [3-bugs-encontrados.md](3-bugs-encontrados.md).
