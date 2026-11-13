# Automação GOPAS - EMPAER

Pipeline de engenharia e validação de dados desenvolvido para automatizar a auditoria, higienização e consolidação de atendimentos a produtores rurais no setor GOPAS, apoiando a verificação de Unidades Consumidoras (UCs) vinculadas às regras de isenção de ICMS (Decreto Estadual nº 42.307/2022).

## Arquitetura do Projeto

* **Validação e Higienização (`Pandas` + `Regex`):** Normalização de CPFs/CNPJs e fatiamento dinâmico de UCs (`X/XXXXXX-X`), com tolerância a variações de digitação e dígitos verificadores.
* **Sistema de Quarentena:** Separação automática entre registros aprovados (`VALIDADOS`) e inconsistências enviadas para auditoria humana (`REVISÃO_MANUAL`) com diagnóstico explícito do motivo.
* **Persistência Local (`MySQL` + `SQLAlchemy`):** Armazenamento seguro em ambiente isolado (`planilha_concluidos`) para consultas e histórico de processamento.
* **Extração Automatizada (`Selenium` / `pdfplumber`):** Coleta de dados cadastrais e histórico de atendimentos *(em desenvolvimento)*.

## Segurança e Privacidade (LGPD)

Por lidar com dados pessoais e fiscais de beneficiários, este repositório versiona **exclusivamente código-fonte e testes sintéticos**. Planilhas reais, relatórios em PDF e credenciais de acesso são bloqueados pelo `.gitignore` e processados apenas localmente.

## Como Executar

1. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
