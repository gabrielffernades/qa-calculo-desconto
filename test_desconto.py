import pytest

from desconto import calcular_desconto


# --- Desconto base: cliente COMUM (valores de fronteira) ---

@pytest.mark.parametrize(
    "valor_compra, desconto_esperado",
    [
        (0, 0.00),          # compra zerada
        (50, 0.00),         # meio da faixa de 0%
        (99.99, 0.00),      # imediatamente antes de 100 -> 0%
        (100, 10.00),       # exatamente 100 -> 10%
        (100.01, 10.00),    # imediatamente depois de 100 -> 10%
        (300, 30.00),       # meio da faixa de 10%
        (499.99, 50.00),    # imediatamente antes de 500 -> 10%
        (500, 100.00),      # exatamente 500 -> 20%
        (500.01, 100.00),   # imediatamente depois de 500 -> 20%
        (750, 150.00),      # meio da faixa de 20%
    ],
)
def test_cliente_comum_recebe_desconto_base_da_faixa(valor_compra, desconto_esperado):
    # Arrange
    tipo_cliente = "COMUM"

    # Act
    resultado = calcular_desconto(valor_compra, tipo_cliente)

    # Assert
    assert resultado == desconto_esperado


# --- Cliente VIP: +5% sobre a porcentagem base ---

@pytest.mark.parametrize(
    "valor_compra, desconto_esperado",
    [
        (50, 2.50),         # 0% + 5% = 5%
        (99.99, 5.00),      # imediatamente antes de 100 -> 5%
        (100, 15.00),       # exatamente 100 -> 15%
        (100.01, 15.00),    # imediatamente depois de 100 -> 15%
        (300, 45.00),       # 10% + 5% = 15%
        (499.99, 75.00),    # imediatamente antes de 500 -> 15%
        (500, 125.00),      # exatamente 500 -> 25%
        (500.01, 125.00),   # imediatamente depois de 500 -> 25%
        (600, 150.00),      # 20% + 5% = 25%
    ],
)
def test_cliente_vip_recebe_cinco_por_cento_extras(valor_compra, desconto_esperado):
    # Arrange
    tipo_cliente = "VIP"

    # Act
    resultado = calcular_desconto(valor_compra, tipo_cliente)

    # Assert
    assert resultado == desconto_esperado


# --- Tipo de cliente independente de maiúsculas/minúsculas ---

@pytest.mark.parametrize("tipo_cliente", ["VIP", "vip", "Vip", "vIp", " vip "])
def test_vip_ignora_maiusculas_e_minusculas(tipo_cliente):
    # Arrange
    valor_compra = 300
    desconto_esperado = 45.00

    # Act
    resultado = calcular_desconto(valor_compra, tipo_cliente)

    # Assert
    assert resultado == desconto_esperado


@pytest.mark.parametrize("tipo_cliente", ["COMUM", "comum", "Comum"])
def test_comum_ignora_maiusculas_e_minusculas(tipo_cliente):
    # Arrange
    valor_compra = 300
    desconto_esperado = 30.00

    # Act
    resultado = calcular_desconto(valor_compra, tipo_cliente)

    # Assert
    assert resultado == desconto_esperado


# --- Regra de teto: desconto nunca ultrapassa R$ 200,00 ---

@pytest.mark.parametrize(
    "valor_compra, tipo_cliente",
    [
        (999.99, "COMUM"),   # 199,998 arredonda para 200,00
        (1000, "COMUM"),     # exatamente no teto
        (1000.01, "COMUM"),  # imediatamente acima do teto
        (5000, "COMUM"),     # muito acima do teto
        (799.99, "VIP"),     # 199,9975 arredonda para 200,00
        (800, "VIP"),        # exatamente no teto
        (1000, "VIP"),       # 250,00 limitado a 200,00
        (10000, "VIP"),      # muito acima do teto
    ],
)
def test_desconto_nunca_ultrapassa_teto_de_duzentos_reais(valor_compra, tipo_cliente):
    # Arrange
    teto = 200.00

    # Act
    resultado = calcular_desconto(valor_compra, tipo_cliente)

    # Assert
    assert resultado == teto


# --- Dados inesperados (não descritos explicitamente na regra) ---

@pytest.mark.parametrize("valor_compra", [-0.01, -100, -1000])
def test_valor_negativo_gera_erro(valor_compra):
    # Arrange
    tipo_cliente = "VIP"

    # Act / Assert
    with pytest.raises(ValueError):
        calcular_desconto(valor_compra, tipo_cliente)


@pytest.mark.parametrize("valor_compra", [None, "300", "abc", [300], True])
def test_valor_nao_numerico_gera_erro(valor_compra):
    # Arrange
    tipo_cliente = "COMUM"

    # Act / Assert
    with pytest.raises(TypeError):
        calcular_desconto(valor_compra, tipo_cliente)


@pytest.mark.parametrize("valor_compra", [float("nan"), float("inf")])
def test_valor_nan_ou_infinito_gera_erro(valor_compra):
    # Arrange
    tipo_cliente = "COMUM"

    # Act / Assert
    with pytest.raises(ValueError):
        calcular_desconto(valor_compra, tipo_cliente)


@pytest.mark.parametrize("tipo_cliente", [None, 123, ["VIP"]])
def test_tipo_cliente_nao_textual_gera_erro(tipo_cliente):
    # Arrange
    valor_compra = 300

    # Act / Assert
    with pytest.raises(TypeError):
        calcular_desconto(valor_compra, tipo_cliente)


@pytest.mark.parametrize("tipo_cliente", ["", "GOLD", "PREMIUM", "VIPP"])
def test_tipo_cliente_desconhecido_gera_erro(tipo_cliente):
    # Arrange
    valor_compra = 300

    # Act / Assert
    with pytest.raises(ValueError):
        calcular_desconto(valor_compra, tipo_cliente)
