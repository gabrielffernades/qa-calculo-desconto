import pytest

from desconto import calcular_desconto


# --- Desconto base: cliente COMUM (valores de fronteira) ---

@pytest.mark.parametrize(
    "valor_compra, esperado",
    [
        (0, 0.00),          # compra zerada
        (50, 0.00),         # abaixo de 100 -> 0%
        (99.99, 0.00),      # limite superior da faixa de 0%
        (100, 10.00),       # fronteira: exatamente 100 -> 10%
        (100.01, 10.00),    # logo acima de 100 -> 10%
        (300, 30.00),       # meio da faixa de 10%
        (499.99, 50.00),    # limite superior da faixa de 10%
        (500, 100.00),      # fronteira: exatamente 500 -> 20%
        (750, 150.00),      # meio da faixa de 20%
    ],
)
def test_desconto_base_cliente_comum(valor_compra, esperado):
    assert calcular_desconto(valor_compra, "COMUM") == esperado


# --- Cliente VIP: +5% sobre a porcentagem base ---

@pytest.mark.parametrize(
    "valor_compra, esperado",
    [
        (50, 2.50),         # 0% + 5% = 5%
        (99.99, 5.00),      # 0% + 5% = 5%
        (100, 15.00),       # fronteira: 10% + 5% = 15%
        (300, 45.00),       # 10% + 5% = 15%
        (499.99, 75.00),    # 10% + 5% = 15%
        (500, 125.00),      # fronteira: 20% + 5% = 25%
        (600, 150.00),      # 20% + 5% = 25%
    ],
)
def test_desconto_cliente_vip(valor_compra, esperado):
    assert calcular_desconto(valor_compra, "VIP") == esperado


# --- VIP independente de maiúsculas/minúsculas ---

@pytest.mark.parametrize("tipo_cliente", ["VIP", "vip", "Vip", "vIp", " vip "])
def test_vip_ignora_maiusculas_e_minusculas(tipo_cliente):
    assert calcular_desconto(300, tipo_cliente) == 45.00


@pytest.mark.parametrize("tipo_cliente", ["COMUM", "comum", "Comum"])
def test_comum_ignora_maiusculas_e_minusculas(tipo_cliente):
    assert calcular_desconto(300, tipo_cliente) == 30.00


# --- Regra de teto: desconto nunca ultrapassa R$ 200,00 ---

@pytest.mark.parametrize(
    "valor_compra, tipo_cliente, esperado",
    [
        (999.99, "COMUM", 200.00),  # 199,998 arredonda para 200,00
        (1000, "COMUM", 200.00),    # exatamente no teto
        (1000.01, "COMUM", 200.00), # logo acima do teto
        (5000, "COMUM", 200.00),    # muito acima do teto
        (799.99, "VIP", 200.00),    # 199,9975 arredonda para 200,00
        (800, "VIP", 200.00),       # exatamente no teto
        (1000, "VIP", 200.00),      # 250 -> limitado a 200
        (10000, "VIP", 200.00),     # muito acima do teto
    ],
)
def test_teto_de_duzentos_reais(valor_compra, tipo_cliente, esperado):
    assert calcular_desconto(valor_compra, tipo_cliente) == esperado


# --- Dados inesperados (não descritos explicitamente na regra) ---

@pytest.mark.parametrize("valor_compra", [-0.01, -100, -1000])
def test_valor_negativo_gera_erro(valor_compra):
    with pytest.raises(ValueError):
        calcular_desconto(valor_compra, "VIP")


@pytest.mark.parametrize("valor_compra", [None, "300", "abc", [300], True])
def test_valor_nao_numerico_gera_erro(valor_compra):
    with pytest.raises(TypeError):
        calcular_desconto(valor_compra, "COMUM")


@pytest.mark.parametrize("valor_compra", [float("nan"), float("inf")])
def test_valor_nan_ou_infinito_gera_erro(valor_compra):
    with pytest.raises(ValueError):
        calcular_desconto(valor_compra, "COMUM")


@pytest.mark.parametrize("tipo_cliente", [None, 123, ["VIP"]])
def test_tipo_cliente_nao_textual_gera_erro(tipo_cliente):
    with pytest.raises(TypeError):
        calcular_desconto(300, tipo_cliente)


@pytest.mark.parametrize("tipo_cliente", ["", "GOLD", "PREMIUM", "VIPP"])
def test_tipo_cliente_desconhecido_gera_erro(tipo_cliente):
    with pytest.raises(ValueError):
        calcular_desconto(300, tipo_cliente)
