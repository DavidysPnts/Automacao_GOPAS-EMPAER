import re
from src.higienizacao import limpar_id

# Padrão do sistema: X/XXXXXX-X (com tolerância a espaços)
PADRAO_UC_SISTEMA = re.compile(r"^\s*\d+\s*/\s*(\d+)\s*-\s*(\d+)\s*$")


def extrair_nucleo_uc(codigo_cliente_sistema: str) -> tuple[str, str] | None:
    """
    Extrai (miolo, miolo_com_dv) de uma string no formato 'X/XXXXXX-X'.
    Retorna None se o formato for inválido ou estiver vazio.
    """
    if not codigo_cliente_sistema:
        return None

    match = PADRAO_UC_SISTEMA.match(str(codigo_cliente_sistema))
    if not match:
        return None

    miolo, dv = match.groups()
    return miolo, f"{miolo}{dv}"


def validar_uc(uc_planilha, codigo_cliente_sistema: str) -> bool:
    """Compara a UC da planilha SEFAZ com o Código do Cliente registrado no atendimento."""
    uc_limpa = limpar_id(uc_planilha)
    if not uc_limpa:
        return False

    nucleo = extrair_nucleo_uc(codigo_cliente_sistema)
    if not nucleo:
        return False

    miolo, miolo_com_dv = nucleo
    return uc_limpa in (miolo, miolo_com_dv)