from src.config import (
    CAMPOS_OBRIGATORIOS_ATENDIMENTO,
    DATA_CORTE_CONTA_ENERGIA,
    IDS_CULTURAS_ELEGIVEIS,
    METODOS_VALIDOS_SEFAZ,
)
from src.higienizacao import limpar_id, normalizar_texto, parse_data


def eh_metodo_sefaz(metodo: str) -> bool:
    """Verifica se o método do atendimento pertence à whitelist (SEFAZ)."""
    return normalizar_texto(metodo) in METODOS_VALIDOS_SEFAZ


def auditar_campos_obrigatorios(atendimento: dict) -> list[str]:
    """Verifica se todos os campos exigidos pelo GOPAS estão preenchidos."""
    erros = []
    for campo in CAMPOS_OBRIGATORIOS_ATENDIMENTO:
        valor = atendimento.get(campo)
        if valor is None or str(valor).strip() == "":
            erros.append(f"Campo obrigatório '{campo}' em branco")
    return erros


def auditar_atividade_produtiva(atendimento: dict, culturas_validas: set[str] = IDS_CULTURAS_ELEGIVEIS) -> list[str]:
    """
    Valida se a atividade produtiva foi informada e se o ID existe na tabela de culturas elegíveis (IDS_CULTURAS_ELEGIVEIS).
    Nota: O valor '0' é preenchido pelo extensionista quando o beneficiário não possui atividade produtiva ( ex.: aposentado rural) e é válido.
    """
    atividade = atendimento.get("atividade_produtiva")
    if atividade is None or str(atividade).strip() == "":
        return []  # Já capturado pelos campos obrigatórios

    atividade_limpa = limpar_id(atividade)
    if not atividade_limpa:
        return [f"Atividade produtiva inválida ({atividade})"]

    if atividade_limpa == "0":
        return []

    if atividade_limpa not in culturas_validas:
        return [f"ID de cultura inexistente ou não elegível ({atividade_limpa})"]

    return []


def auditar_evidencias(atendimento: dict) -> list[str]:
    """
    Valida a quantidade e tipo de anexos conforme a data do atendimento:
    - Antes de 01/02/2026: exige foto do medidor.
    - A partir de 01/02/2026: exige foto do medidor + foto da conta de energia.
    """
    erros = []
    data_atend = parse_data(atendimento.get("data_atendimento"))
    tem_foto_medidor = bool(atendimento.get("tem_foto_medidor"))
    tem_foto_conta = bool(atendimento.get("tem_foto_conta"))

    if not tem_foto_medidor:
        erros.append("Ausência da foto do medidor de energia")

    if data_atend and data_atend >= DATA_CORTE_CONTA_ENERGIA:
        if not tem_foto_conta:
            erros.append("Atendimento a partir de fev/2026 sem foto da conta de energia")

    return erros