from datetime import date
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_CULTURAS_JSON = BASE_DIR / "data" / "referencia" / "culturas_elegiveis.json"

def _carregar_culturas_elegiveis() -> dict[str, str]:
    """Lê o JSON de referência e retorna {id_cultura: nome} apenas das culturas ativas."""
    with open(CAMINHO_CULTURAS_JSON, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return {
        str(id_cultura).strip(): info["nome"]
        for id_cultura, info in dados.get("culturas", {}).items()
        if info.get("ativo", True)
    }

# Dicionário {id: nome} e conjunto de IDs válidos para busca 0(1)
CULTURAS_ELEGIVEIS = _carregar_culturas_elegiveis()
IDS_CULTURAS_ELEGIVEIS = set(CULTURAS_ELEGIVEIS.keys())

# Métodos elegíveis na aba de Atendimento (comparação feita em minúsculo e sem acento)
METODOS_VALIDOS_SEFAZ = {
    "beneficiario nao encontrado (sefaz)",
    "acessou a propriedade (sefaz)",
    "sem acesso a propriedade (sefaz)",
}

# Data de corte para exigência de 2 evidências (foto do medidor + conta de energia)
DATA_CORTE_CONTA_ENERGIA = date(2026, 2, 1)

# Campos que não podem estar em branco dentro do atendimento
CAMPOS_OBRIGATORIOS_ATENDIMENTO = [
    "atividade_produtiva",
    "codigo_cliente",
    "tem_isencao_icms",
    "licenciamento_ambiental",
    "outorga_agua",
    "tarifa_verde",
    "quantidade_medidores",
]

# Tolerância geográfica entre coordenada da propriedade e do atendimento (em metros)
RAIO_TOLERANCIA_METROS = 1000.0  # Valor inicial provisório (1 km) para calibragem futura