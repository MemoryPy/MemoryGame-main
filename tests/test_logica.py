from src.funcoes import (
    criar_valores_embaralhados,
    indice_para_coordenada,
    verificar_par,
    calcular_pontos,
    todos_pares_encontrados,
    eh_novo_recorde,
)
from src.dados import salvar_recorde, carregar_recorde


SIMBOLOS_TESTE = ["A", "B", "C", "D", "E", "F", "G", "H"]


def test_embaralhamento_gera_oito_pares():
    """O embaralhamento deve gerar 16 cartas, com cada símbolo aparecendo 2 vezes."""
    valores = criar_valores_embaralhados(SIMBOLOS_TESTE)
    assert len(valores) == 16
    for simbolo in SIMBOLOS_TESTE:
        assert valores.count(simbolo) == 2


def test_indice_para_coordenada():
    """Deve converter o índice da lista para a coordenada (linha, coluna)."""
    assert indice_para_coordenada(0, 4) == (0, 0)
    assert indice_para_coordenada(5, 4) == (1, 1)
    assert indice_para_coordenada(15, 4) == (3, 3)


def test_verificar_par_iguais():
    """Duas cartas com o mesmo símbolo formam um par."""
    assert verificar_par("A", "A") is True


def test_verificar_par_diferentes():
    """Duas cartas com símbolos diferentes não formam um par."""
    assert verificar_par("A", "B") is False


def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_todos_pares_encontrados():
    """Deve indicar fim de jogo apenas quando todos os pares forem achados."""
    assert todos_pares_encontrados({"A", "B"}, 8) is False
    assert todos_pares_encontrados(set(SIMBOLOS_TESTE), 8) is True


def test_eh_novo_recorde():
    """Só é recorde quando a pontuação supera o valor salvo."""
    assert eh_novo_recorde(80, 50) is True
    assert eh_novo_recorde(50, 50) is False


def test_salvar_e_carregar_recorde(tmp_path):
    """O recorde salvo em JSON deve ser lido de volta com o mesmo valor."""
    caminho = tmp_path / "record.json"
    salvar_recorde(str(caminho), 120)
    assert carregar_recorde(str(caminho)) == 120


def test_carregar_recorde_inexistente(tmp_path):
    """Quando não há arquivo de recorde, deve retornar 0."""
    caminho = tmp_path / "nao_existe.json"
    assert carregar_recorde(str(caminho)) == 0
