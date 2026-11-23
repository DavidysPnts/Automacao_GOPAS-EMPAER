from src.config import (
    CAMPOS_OBRIGATORIOS_ATENDIMENTO,
    DATA_CORTE_CONTA_ENERGIA,
    METODOS_VALIDOS_SEFAZ,
)
from src.higienizacao import normalizar_texto, parse_data


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


def auditar_atividade_produtiva(atendimento: dict, culturas_validas: set | None = None) -> list[str]:
    """
    Valida se a atividade produtiva foi informada e se o ID existe na tabela de culturas.
    Se 'culturas_validas' não for passado ainda, valida apenas presença de ID/texto válido.
    """
    erros = []
    atividade = atendimento.get("atividade_produtiva")
    id_cultura = atendimento.get("id_cultura")

    if not atividade or str(atividade).strip() == "":
        return []  # Já capturado pelos campos obrigatórios

    if id_cultura is None or str(id_cultura).strip() == "":
        erros.append("Atividade produtiva sem ID de cultura associado")
    elif culturas_validas is not None and str(id_cultura).strip() not in culturas_validas:
        erros.append(f"ID de cultura inexistente ({id_cultura})")

    return erros


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