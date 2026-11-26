# Regras de Negócio — Auditoria GOPAS / EMPAER

Este documento consolida os critérios operacionais, fiscais e de auditoria utilizados pelo pipeline de validação de atendimentos rurais (isenção de ICMS).

---

## 1. Estrutura de Dados e Identificação

* **Base de Entrada (Lista SEFAZ):** Planilha recebida com dados cadastrais pré-preenchidos (`UC DO CLIENTE`, `NOME`, `TIPO`, `CPF/CNPJ`, `REGIÃO` e `MUNICÍPIO`).
* **Chave Composta (`CPF/CNPJ` + `UC DO CLIENTE`):** Um mesmo beneficiário pode aparecer em múltiplas linhas caso possua mais de uma Unidade Consumidora. O cruzamento vincula o atendimento especificamente à UC da respectiva linha.
* **Coluna `CORREÇÃO REGIONAL`:** Campo de retorno exclusivo dos extensionistas após apontamento do GOPAS. O pipeline deve mantê-la intacta/vazia.

---

## 2. Fontes de Consulta no Sistema Web (3 Abas)

Para cada `CPF/CNPJ` auditado, o pipeline coleta informações em três módulos distintos do sistema:

### 2.1. Aba Unidade Familiar
* **Existência de Cadastro:** Preenche `1` se o CPF possuir Unidade Familiar ativa no sistema; caso contrário, `0`.
* **Extensionista Responsável:** Extração do nome do técnico responsável pelo cadastro *(pendente confirmar exibição direta na interface web vs. fallback via relatório PDF)*.

### 2.2. Aba Beneficiário
* **Propriedade Vinculada:** Caso o beneficiário possua propriedade rural cadastrada, extraem-se as **coordenadas geográficas da propriedade** para auditoria cruzada.

### 2.3. Aba Atendimento
* **Filtro de Método (Whitelist SEFAZ):** Considerar exclusivamente atendimentos cujo método possua o sufixo `(SEFAZ)`:
  * `Beneficiário não encontrado (SEFAZ)`
  * `Acessou a propriedade (SEFAZ)`
  * `Sem acesso a propriedade (SEFAZ)`
* **Cruzamento de UC (`X/XXXXXX-X`):** Extrai o miolo entre `/` e `-`. Válido se a `UC DO CLIENTE` corresponder ao miolo puro ou ao miolo + dígito verificador (ignorando espaços e sufixos `.0` do Excel).
* **Preenchimento de Saída:** Grava o **Código do Atendimento** e marca `1` na coluna correspondente ao **mês** em que o atendimento foi realizado.

---

## 3. Auditoria de Conformidade (Esteira de Validação)

Todo atendimento que passar pelo filtro de método e UC é submetido às seguintes verificações:

### 3.1. Campos Obrigatórios (Não Nulos)
O registro é sinalizado como erro caso qualquer um dos campos abaixo esteja em branco:
* Atividade produtiva
* Código do cliente
* Tem isenção do ICMS
* Licenciamento ambiental
* Outorga d'água
* Tarifa verde
* Quantidade de medidores

### 3.2. Consistência de Atividade Produtiva
* Cada cultura elegível possui um ID numérico de referência (ex: `Abacaxi -> 1`).
* **Exceção Válida (`0`):** Quando o beneficiário não possui atividade produtiva (ex.: aposentado rural), o extensionista preenche o campo com `0`, o que é aceito sem gerar pendência.
* **Critério de Erro:** Campo vazio, texto sem ID numérico ou ID diferente de `0` que não conste na tabela oficial de culturas elegíveis (`culturas_elegiveis.json`).

### 3.3. Auditoria de Geolocalização (Coordenadas)
* Quando o beneficiário possuir propriedade cadastrada na Aba Beneficiário, compara-se a coordenada da propriedade com a coordenada registrada no atendimento.
* **Critério de Erro:** Distância superior à margem de tolerância estabelecida *(raio em metros/km a ser calibrado)*.

### 3.4. Regra Temporal de Evidências (Anexos Obrigatórios)
* **Até Janeiro/2026 (`< 01/02/2026`):** Exige obrigatoriamente **1 evidência** (Foto do medidor de energia).
* **A partir de Fevereiro/2026 (`>= 01/02/2026`):** Exige obrigatoriamente **2 evidências** (Foto do medidor de energia **+** Foto da conta de energia).

---

## 4. Consolidação de Observações e Quarentena

* **Composição da Coluna `OBSERVAÇÃO`:**
  * Se o atendimento no sistema já possuir uma observação original, ela é preservada.
  * Todos os erros detectados na esteira de auditoria são concatenados ao texto da observação.
* **Roteamento de Saída:**
  * **Sem erros detectados:** Linha encaminhada para a aba `VALIDADOS`.
  * **Com qualquer inconsistência:** Linha desviada para a aba `REVISÃO_MANUAL` com diagnóstico detalhado na coluna `MOTIVO_QUARENTENA` e observação consolidada pronta.

---

## 5. Pontos Pendentes de Calibração

* **Extensionista na Interface Web:** Confirmar se o nome do técnico fica visível na Aba Unidade Familiar do sistema.
* **Raio de Tolerância Geográfica:** Definir a distância máxima aceitável (ex: 500m, 1km, 2km) entre a coordenada da propriedade e a do atendimento.
* **Multiplicidade 1:N na Mesma UC:** Definir comportamento caso um mesmo par `CPF/CNPJ + UC` possua múltiplos atendimentos `(SEFAZ)` elegíveis no mesmo período.