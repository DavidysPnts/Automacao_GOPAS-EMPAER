from pathlib import Path
import pandas as pd


def carregar_planilha_sefaz(caminho_arquivo: str | Path) -> list[dict]:
    """Lê a planilha Excel da SEFAZ e converte as linhas para uma lista de dicionários."""
    df = pd.read_excel(caminho_arquivo, dtype={"CPF/CNPJ": str, "UC DO CLIENTE": str})
    df = df.fillna("")
    return df.to_dict(orient="records")


def exportar_resultado_auditoria(registros_auditados: list[dict], caminho_saida: str | Path) -> None:
    """
    Separa os registros auditados em duas abas ('VALIDADOS' e 'REVISÃO_MANUAL')
    e salva em arquivo Excel mantendo a coluna 'CORREÇÃO REGIONAL' intacta.
    """
    validados = []
    revisao = []

    for reg in registros_auditados:
        item = dict(reg)
        aprovado = item.pop("aprovado", False)

        if "CORREÇÃO REGIONAL" not in item:
            item["CORREÇÃO REGIONAL"] = ""

        if aprovado:
            item.pop("MOTIVO_QUARENTENA", None)
            validados.append(item)
        else:
            revisao.append(item)

    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
        pd.DataFrame(validados).to_excel(writer, sheet_name="VALIDADOS", index=False)
        pd.DataFrame(revisao).to_excel(writer, sheet_name="REVISÃO_MANUAL", index=False)