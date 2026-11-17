# Regras de Negócio — Auditoria GOPAS / EMPAER

Este documento consolida os critérios operacionais e fiscais utilizados pelo pipeline de validação de atendimentos rurais (isenção de ICMS).

---

## 1. Estrutura de Dados e Identificação

* **Base de Entrada (Lista SEFAZ):** A planilha recebida já contém os dados cadastrais pré-preenchidos (`UC DO CLIENTE`, `NOME`, `TIPO`, `CPF/CNPJ`, `REGIÃO` e `MUNICÍPIO`).
* **Chave Composta (`CPF/CNPJ` + `UC DO CLIENTE`):** Um mesmo beneficiário pode aparecer em múltiplas linhas caso possua mais de uma Unidade Consumidora. A validação cruza o histórico do CPF/CNPJ especificamente contra a UC da linha correspondente.
* **Coluna `CORREÇÃO REGIONAL`:** Campo exclusivo para retorno operacional dos extensionistas após apontamento do GOPAS. O pipeline deve mantê-la intacta/vazia.

---

## 2. Higienização e Cruzamento de UCs

* **Formato no Sistema de Atendimento:** `X/XXXXXX-X` (ex: `3/458912-8`).
* **Regra de Match:** Extrai-se o miolo numérico entre a barra (`/`) e o hífen (`-`). O registro é considerado válido se a `UC DO CLIENTE` na planilha corresponder:
  1. Apenas ao miolo (`458912`), **OU**
  2. Ao miolo concatenado com o dígito verificador após o hífen (`4589128`).
* **Tolerância de Formatação:** Espaços em branco acidentais ao redor dos separadores e sufixos decimais gerados pelo Excel (`.0`) são removidos antes da comparação.

---

## 3. Critérios de Elegibilidade do Atendimento

### 3.1. Filtro de Método
Atendimentos de rotina são ignorados. O pipeline deve considerar **exclusivamente** atendimentos cujo método possua o sufixo `(SEFAZ)`:
* `Beneficiário não encontrado (SEFAZ)`
* `Acessou a propriedade (SEFAZ)`
* `Sem acesso a propriedade (SEFAZ)`

### 3.2. Regra Temporal de Evidências (Anexos Obrigatórios)
A exigência documental varia conforme a data de realização do atendimento:
* **Até Janeiro/2026 (`< 01/02/2026`):** Exige obrigatoriamente **1 evidência** (Foto do medidor de energia).
* **A partir de Fevereiro/2026 (`>= 01/02/2026`):** Exige obrigatoriamente **2 evidências** (Foto do medidor de energia **+** Foto da conta de energia).

---

## 4. Tratamento de Exceções (Quarentena)

Registros que falharem na validação da UC, ausência de atendimento elegível ou falta de evidências obrigatórias não são descartados; são desviados para a aba `REVISÃO_MANUAL` acompanhados de um diagnóstico explícito na coluna `MOTIVO_QUARENTENA`.

---

## 5. Pontos em Levantamento (Em Aberto)

* **Origem do Extensionista:** Confirmar se o nome do técnico responsável está acessível diretamente na interface web do sistema (eliminando a necessidade de parser no relatório PDF `rpt-00537.pdf`).
* **Multiplicidade 1:N na Mesma UC:** Definir o comportamento padrão caso um mesmo par `CPF/CNPJ + UC` possua dois ou mais atendimentos `(SEFAZ)` válidos dentro do período auditado.