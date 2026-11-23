import re
import unicodedata
from datetime import datetime, date


def limpar_id(valor) -> str:
    """Remove sufixos decimais do Excel (.0), espaços e caracteres não numéricos de IDs/UCs."""
    if valor is None:
        return ""
    texto = str(valor).strip()
    if texto.endswith(".0"):
        texto = texto[:-2]
    return re.sub(r"\D", "", texto)


def limpar_cpf_cnpj(valor) -> str:
    """Mantém apenas os dígitos numéricos de CPF ou CNPJ."""
    return limpar_id(valor)


def normalizar_texto(texto: str) -> str:
    """Converte para minúsculo, remove espaços extras e retira acentos para comparação segura."""
    if not texto:
        return ""
    texto_limpo = str(texto).strip().lower()
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFD", texto_limpo)
        if unicodedata.category(c) != "Mn"
    )
    return " ".join(sem_acento.split())


def parse_data(valor) -> date | None:
    """Converte strings de data (DD/MM/AAAA ou AAAA-MM-DD) ou objetos datetime para date."""
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if not valor:
        return None

    texto = str(valor).strip()
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    return None