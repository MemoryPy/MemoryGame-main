# Testes automaticos das funcoes de logica do jogo.
# Cada funcao test_... checa se uma regra do jogo se comporta como esperado.
# Para rodar todos de uma vez: python -m pytest

from src.funcoes import (
    montar_simbolos_do_nivel,
    criar_valores_embaralhados,
    indice_para_coordenada,
    verificar_par,
    calcular_pontos,
    todos_pares_encontrados,
    eh_novo_recorde,
    calcular_bonus_tempo,
    calcular_precisao,
    atualizar_combo,
    calcular_multiplicador_combo,
    atualizar_estatisticas,
    verificar_conquistas,
    qualifica_para_ranking,
    atualizar_ranking,
    completar_par_bonus,
    reembaralhar_ocultas,
)
from src.dados import (
    salvar_recordes,
    carregar_recordes,
    salvar_estatisticas,
    carregar_estatisticas,
    salvar_ranking,
    carregar_ranking,
    salvar_conquistas,
    carregar_conquistas,
    salvar_preferencias,
    carregar_preferencias,
)


# Lista de letras de exemplo (8 pares) usada em varios testes.
SIMBOLOS_TESTE = ["A", "B", "C", "D", "E", "F", "G", "H"]


def test_montar_simbolos_do_nivel_sem_especiais():
    """Sem cartas especiais ativas, usa só os símbolos normais do nível."""
    simbolos = montar_simbolos_do_nivel(SIMBOLOS_TESTE, 8, ["*", "+", "@"], ativar_especiais=False)
    assert simbolos == SIMBOLOS_TESTE


def test_montar_simbolos_do_nivel_com_especiais():
    """Com cartas especiais ativas, troca os últimos símbolos pelos especiais,
    mantendo o total de pares igual."""
    simbolos = montar_simbolos_do_nivel(SIMBOLOS_TESTE, 8, ["*", "+", "@"], ativar_especiais=True)
    assert len(simbolos) == 8
    assert simbolos[-3:] == ["*", "+", "@"]


def test_montar_simbolos_do_nivel_pares_insuficientes():
    """Se não houver pares suficientes, as cartas especiais não entram."""
    simbolos = montar_simbolos_do_nivel(SIMBOLOS_TESTE[:3], 3, ["*", "+", "@"], ativar_especiais=True)
    assert "*" not in simbolos


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
    
def test_calcular_bonus_tempo():
    """O bônus é o tempo restante multiplicado pelos pontos por segundo."""
    assert calcular_bonus_tempo(30, 2) == 60
    assert calcular_bonus_tempo(0, 2) == 0
    assert calcular_bonus_tempo(-5, 2) == 0  # segurança: tempo negativo não pontua

def test_todos_pares_encontrados():
    """Deve indicar fim de jogo apenas quando todos os pares forem achados."""
    assert todos_pares_encontrados({"A", "B"}, 8) is False
    assert todos_pares_encontrados(set(SIMBOLOS_TESTE), 8) is True


def test_eh_novo_recorde():
    """Só é recorde quando a pontuação supera o valor salvo."""
    assert eh_novo_recorde(80, 50) is True
    assert eh_novo_recorde(50, 50) is False


def test_salvar_e_carregar_recordes(tmp_path):
    """Os recordes por nível salvos em JSON devem ser lidos de volta iguais."""
    caminho = tmp_path / "record.json"
    salvar_recordes(str(caminho), {"facil": 80, "extremo": 260})
    recordes = carregar_recordes(str(caminho))
    assert recordes["facil"] == 80
    assert recordes["extremo"] == 260


def test_carregar_recordes_inexistente(tmp_path):
    """Quando não há arquivo de recorde, deve retornar um dicionário vazio."""
    caminho = tmp_path / "nao_existe.json"
    assert carregar_recordes(str(caminho)) == {}


def test_calcular_precisao():
    """A precisão é a porcentagem de tentativas que acertaram um par."""
    assert calcular_precisao(8, 8) == 100.0
    assert calcular_precisao(10, 5) == 50.0
    assert calcular_precisao(0, 0) == 0.0  # sem tentativas, sem divisão por zero


def test_atualizar_combo():
    """Acertar soma 1 ao combo; errar zera a sequência."""
    combo = 0
    combo = atualizar_combo(combo, acertou=True)
    combo = atualizar_combo(combo, acertou=True)
    assert combo == 2
    combo = atualizar_combo(combo, acertou=False)
    assert combo == 0


def test_calcular_multiplicador_combo():
    """O multiplicador cresce com o combo, mas não passa do máximo configurado."""
    assert calcular_multiplicador_combo(0, incremento=0.5, maximo=3.0) == 1.0
    assert calcular_multiplicador_combo(2, incremento=0.5, maximo=3.0) == 2.0
    assert calcular_multiplicador_combo(100, incremento=0.5, maximo=3.0) == 3.0


def test_atualizar_estatisticas_vitoria():
    """Vitórias atualizam menor tentativas, melhor tempo e contadores."""
    stats = {}
    stats = atualizar_estatisticas(stats, venceu=True, tentativas=10, tempo_restante=20)
    stats = atualizar_estatisticas(stats, venceu=True, tentativas=6, tempo_restante=15)
    assert stats["partidas"] == 2
    assert stats["vitorias"] == 2
    assert stats["menor_tentativas"] == 6
    assert stats["melhor_tempo"] == 20


def test_atualizar_estatisticas_derrota():
    """Derrotas contam como partida jogada, mas não alteram os melhores números."""
    stats = atualizar_estatisticas({}, venceu=False, tentativas=20, tempo_restante=0)
    assert stats["partidas"] == 1
    assert stats.get("vitorias", 0) == 0
    assert stats.get("menor_tentativas") is None


def test_verificar_conquistas_perfeito_e_extremo():
    """Vencer sem errar e no nível extremo desbloqueia as conquistas certas."""
    resumo = {
        "tentativas": 8,
        "numero_pares": 8,
        "tempo_restante": 40,
        "tempo_limite": 45,
        "nivel": "extremo",
        "dicas_usadas": 0,
        "total_partidas": 1,
    }
    novas = verificar_conquistas(resumo, conquistas_atuais=set())
    assert "perfeito" in novas
    assert "sobrou_tempo" in novas
    assert "sem_dica" in novas
    assert "extremo_concluido" in novas
    assert "veterano" not in novas


def test_verificar_conquistas_ja_desbloqueadas_nao_repetem():
    """Conquistas que o jogador já tem não voltam na lista de novidades."""
    resumo = {
        "tentativas": 8,
        "numero_pares": 8,
        "tempo_restante": 40,
        "tempo_limite": 45,
        "nivel": "facil",
        "dicas_usadas": 0,
        "total_partidas": 1,
    }
    novas = verificar_conquistas(resumo, conquistas_atuais={"perfeito", "sobrou_tempo", "sem_dica"})
    assert novas == set()


def test_qualifica_para_ranking_com_vagas():
    """Com menos itens que o tamanho máximo, qualquer pontuação entra."""
    assert qualifica_para_ranking([], pontos=1, tamanho_maximo=5) is True


def test_qualifica_para_ranking_lista_cheia():
    """Com a lista cheia, só entra quem supera a pior pontuação salva."""
    ranking = [{"nome": "A", "pontos": 100}, {"nome": "B", "pontos": 50}]
    assert qualifica_para_ranking(ranking, pontos=80, tamanho_maximo=2) is True
    assert qualifica_para_ranking(ranking, pontos=30, tamanho_maximo=2) is False


def test_atualizar_ranking_ordena_e_corta():
    """O ranking fica ordenado do maior para o menor e cortado no tamanho máximo."""
    ranking = [{"nome": "A", "pontos": 100}, {"nome": "B", "pontos": 50}]
    ranking = atualizar_ranking(ranking, nome="C", pontos=80, tamanho_maximo=2)
    assert ranking == [{"nome": "A", "pontos": 100}, {"nome": "C", "pontos": 80}]


def test_completar_par_bonus_escolhe_entre_ocultas():
    """A curinga só pode completar um par que ainda está oculto."""
    assert completar_par_bonus(["B", "B"]) == "B"
    assert completar_par_bonus([]) is None


def test_reembaralhar_ocultas_preserva_valores():
    """Reembaralhar muda a ordem, mas não pode adicionar nem remover valores."""
    valores = ["A", "A", "B", "B", "C", "C"]
    embaralhados = reembaralhar_ocultas(valores)
    assert sorted(embaralhados) == sorted(valores)


def test_salvar_e_carregar_estatisticas(tmp_path):
    """As estatísticas por nível salvas em JSON devem ser lidas de volta iguais."""
    caminho = tmp_path / "record.json"
    stats = {"facil": {"partidas": 3, "vitorias": 2, "menor_tentativas": 9, "melhor_tempo": 40}}
    salvar_estatisticas(str(caminho), stats)
    assert carregar_estatisticas(str(caminho)) == stats


def test_salvar_e_carregar_ranking(tmp_path):
    """O ranking por nível salvo em JSON deve ser lido de volta igual."""
    caminho = tmp_path / "record.json"
    ranking = {"facil": [{"nome": "Mario", "pontos": 100}]}
    salvar_ranking(str(caminho), ranking)
    assert carregar_ranking(str(caminho)) == ranking


def test_salvar_e_carregar_conquistas(tmp_path):
    """As conquistas desbloqueadas salvas em JSON devem ser lidas de volta iguais."""
    caminho = tmp_path / "record.json"
    salvar_conquistas(str(caminho), {"perfeito", "veterano"})
    assert carregar_conquistas(str(caminho)) == {"perfeito", "veterano"}


def test_secoes_de_dados_nao_se_misturam(tmp_path):
    """Salvar uma seção (ex.: recordes) não deve apagar as outras seções já salvas."""
    caminho = tmp_path / "record.json"
    salvar_recordes(str(caminho), {"facil": 80})
    salvar_conquistas(str(caminho), {"perfeito"})
    assert carregar_recordes(str(caminho)) == {"facil": 80}
    assert carregar_conquistas(str(caminho)) == {"perfeito"}


def test_carregar_preferencias_usa_padrao_quando_nao_existe(tmp_path):
    """Sem preferências salvas, o jogo assume tema escuro e som ligado."""
    caminho = tmp_path / "nao_existe.json"
    prefs = carregar_preferencias(str(caminho))
    assert prefs == {"tema": "escuro", "som_ativado": True}


def test_salvar_e_carregar_preferencias(tmp_path):
    """As preferências salvas em JSON devem ser lidas de volta iguais."""
    caminho = tmp_path / "record.json"
    salvar_preferencias(str(caminho), {"tema": "claro", "som_ativado": False})
    assert carregar_preferencias(str(caminho)) == {"tema": "claro", "som_ativado": False}