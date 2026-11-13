import pandas as pd

def limpar_id(valor) -> str:
    """Garante que identificadores numéricos sejam strings limpas, sem '.0' do Excel."""
    if pd.isna(valor):
        return ""
    
    texto = str(valor).strip()
    if texto.endswith(".0"):
        texto = texto[:-2]
        
    return texto