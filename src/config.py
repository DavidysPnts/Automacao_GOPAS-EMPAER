from datetime import date

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