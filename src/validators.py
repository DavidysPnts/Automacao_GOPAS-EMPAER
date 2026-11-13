import pandas as pd
import re

def limpar_id(valor) -> str:
    """Garante que identificadores numéricos sejam strings limpas, sem '.0' do Excel."""
    if pd.isna(valor):
        return ""
    
    texto = str(valor).strip()
    if texto.endswith(".0"):
        texto = texto[:-2]
        
    return texto

def validar_uc(uc_cliente: str, uc_atendimento: str) -> tuple[bool, str, str]:
    """
    Valida se a UC do atendimento corresponde à UC oficial do cliente.
    Retorna: (eh_valido, uc_normalizada, motivo_quarentena)
    """
    cliente_limpo = limpar_id(uc_cliente)
    atendimento_limpo = limpar_id(uc_atendimento)

    if not atendimento_limpo:
        return False, "", "UC de atendimento ausente"

    # Captura o miolo (entre '/' e '-') e o dígito verificador (após '-'),
    # tolerando espaços acidentais digitados pelos extensionistas.
    padrao = re.search(r"^\d+\s*/\s*(\d+)\s*-\s*(\d+)$", atendimento_limpo)

    if not padrao:
        return False, atendimento_limpo, "Padrão de UC atípico (fora do formato X/XXXXXX-X)"

    miolo = padrao.group(1)
    digito = padrao.group(2)
    miolo_com_digito = f"{miolo}{digito}"

    # Regra flexível: aceita tanto apenas o miolo quanto o miolo + dígito após o traço
    if cliente_limpo == miolo:
        return True, miolo, ""
    elif cliente_limpo == miolo_com_digito:
        return True, miolo_com_digito, ""
    else:
        return False, atendimento_limpo, f"UC divergente (Esperado: {cliente_limpo} | Encontrado: {miolo} ou {miolo_com_digito})"