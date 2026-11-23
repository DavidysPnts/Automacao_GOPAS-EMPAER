from src.higienizacao import parse_data
from src.validacao_atendimento import (
    auditar_atividade_produtiva,
    auditar_campos_obrigatorios,
    auditar_evidencias,
    eh_metodo_sefaz,
)
from src.validacao_geolocalizacao import auditar_geolocalizacao
from src.validacao_uc import validar_uc


def _consolidar_observacao(obs_original: str | None, erros: list[str]) -> str:
    """Preserva a observação original do atendimento e concatena os erros encontrados."""
    partes = []
    if obs_original and str(obs_original).strip():
        partes.append(str(obs_original).strip())
    if erros:
        partes.append(" | ".join(erros))
    return " - ".join(partes)


def auditar_registro(
    linha_planilha: dict,
    dados_uf: dict,
    dados_beneficiario: dict,
    atendimentos: list[dict],
    culturas_validas: set | None = None,
) -> dict:
    """
    Executa a esteira completa de auditoria para uma linha da planilha SEFAZ.
    Retorna o dicionário atualizado com os campos preenchidos e a flag 'aprovado'.
    """
    resultado = dict(linha_planilha)
    erros = []

    # 1. Aba Unidade Familiar
    tem_uf = bool(dados_uf.get("existe"))
    resultado["UNIDADE_FAMILIAR"] = 1 if tem_uf else 0
    resultado["EXTENSIONISTA"] = dados_uf.get("extensionista", "")

    # 2. Filtra atendimentos (SEFAZ) compatíveis com a UC da linha
    uc_planilha = linha_planilha.get("UC DO CLIENTE")
    atendimento_alvo = None

    for atend in atendimentos:
        if eh_metodo_sefaz(atend.get("metodo", "")) and validar_uc(uc_planilha, atend.get("codigo_cliente", "")):
            atendimento_alvo = atend
            break

    if not atendimento_alvo:
        erros.append("Nenhum atendimento (SEFAZ) encontrado para esta UC")
        resultado["OBSERVAÇÃO"] = _consolidar_observacao(None, erros)
        resultado["MOTIVO_QUARENTENA"] = " | ".join(erros)
        resultado["aprovado"] = False
        return resultado

    # 3. Preenche dados do atendimento encontrado
    resultado["COD_ATENDIMENTO"] = atendimento_alvo.get("codigo_atendimento", "")
    data_atend = parse_data(atendimento_alvo.get("data_atendimento"))
    if data_atend:
        resultado[f"MES_{data_atend.month:02d}"] = 1

    # 4. Executa validações de conformidade em cascata
    erros.extend(auditar_campos_obrigatorios(atendimento_alvo))
    erros.extend(auditar_atividade_produtiva(atendimento_alvo, culturas_validas))
    erros.extend(auditar_evidencias(atendimento_alvo))
    erros.extend(
        auditar_geolocalizacao(
            coord_propriedade=dados_beneficiario.get("coordenadas"),
            coord_atendimento=atendimento_alvo.get("coordenadas"),
        )
    )

    # 5. Consolida observação e define roteamento
    resultado["OBSERVAÇÃO"] = _consolidar_observacao(atendimento_alvo.get("observacao"), erros)
    resultado["MOTIVO_QUARENTENA"] = " | ".join(erros)
    resultado["aprovado"] = len(erros) == 0

    return resultado