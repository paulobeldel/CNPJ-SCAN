# CNPJ-SCAN

Projeto de sistema para automação para facilitar a busca de informações do CNPJ de empresas e converter os dados para uma planilha.

### Como executar

Na pasta raíz do projeto: `uvicorn src.main:app --reload`

<div align="center">
  <img src="https://github.com/user-attachments/assets/7eaa9442-73cd-45f8-b601-843f0072179c">
</div>


## Colaboradores ✨
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/paulobeldel"><img src="https://avatars.githubusercontent.com/u/105087411?v=4?s=100" width="100px;" alt="Paulo Beldel Filho"/><br /><sub><b>Paulo Beldel Filho</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/anacris34"><img src="https://avatars.githubusercontent.com/u/213529724?v=4" width="100px;" alt="Ana Cris"/><br /><sub><b>Ana Cris</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dualbuquerque"><img src="https://avatars.githubusercontent.com/u/96270653?v=4?s=100" width="100px;" alt="Carlos Eduardo"/><br /><sub><b>Carlos Eduardo</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/italogna"><img src="https://avatars.githubusercontent.com/u/155203334?v=4?s=100" width="100px;" alt="Italo Araujo"/><br /><sub><b>Italo Araujo</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/marthalacerda"><img src="https://avatars.githubusercontent.com/u/101488470?v=4s=100" width="100px;" alt="Martha Lacerda"/><br /><sub><b>Martha Lacerda</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MyllenaAlmeida"><img src="https://avatars.githubusercontent.com/u/38386226?v=4?s=100" width="100px;" alt="MyllenaAlmeida"/><br /><sub><b>Myllena Almeida</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/pedroabn"><img src="https://avatars.githubusercontent.com/u/62610839?v=4?s=100" width="100px;" alt="Pedro Neiva"/><br /><sub><b>Pedro Neiva</b></sub></a><br /></td>
    </tr>
  </tbody>
</table>


# CNPJ Scan - Processador de Cartões CNPJ

## 🌟 Visão Geral do Projeto

Este projeto foi desenvolvido por estudantes do **Curso NExT: Nova Experiência de Trabalho da CESAR School** como módulo de conclusão.



Este projeto, desenvolvido por estudantes do **[Nome do Seu Curso e Instituição - Ex: NExT - Formação em TI]**, é um processador de documentos em lote (Batch Document Processor). O objetivo principal é automatizar a extração de dados de Cartões CNPJ (Receita Federal) e convertê-los em um relatório CSV estruturado e filtrável.

O projeto é uma demonstração de habilidades em arquitetura de microsserviços, programação assíncrona (`FastAPI`), e engenharia de dados (Regex e PyMuPDF), garantindo uma solução eficiente e segura.

> **Status:** MVP Finalizado - Extração em Lote, Validação e Geração de Relatórios Concluídos.

---

## 🛠️ Tecnologias e Habilidades

Nossa solução foi construída com um *stack* moderno e profissional, focado em performance e manutenibilidade.

| Categoria | Ferramenta/Biblioteca | Habilidade Demonstrada |
| :--- | :--- | :--- |
| **Framework Principal** | **FastAPI** | Criação de APIs assíncronas e de alta performance. |
| **Configuração** | **Pydantic Settings** | Gestão e validação estruturada de variáveis de ambiente (`.env`) e configurações de CORS. |
| **Extração de Dados** | **PyMuPDF (`fitz`)** | Processamento robusto de documentos PDF e extração precisa de texto (solução para o problema de layouts de formulário). |
| **Lógica de Negócio** | **`re` (Regex)** | Engenharia de dados para identificar e extrair mais de 20 campos de formulários complexos. |
| **Relatórios** | **`csv`** | Geração eficiente de relatórios tabulares em formato CSV (suporte a múltiplas linhas). |
| **Qualidade & Testes** | **`pytest` / `pytest-asyncio` / `httpx`** | Testes unitários e de integração para garantir a funcionalidade e a robustez da API. |
| **Arquitetura** | **`routers` / `services` / `core`** | Implementação do Princípio da Responsabilidade Única e desacoplamento de código. |

---

## 🚀 Arquitetura e Fluxo de Trabalho

A aplicação segue uma arquitetura modular de três camadas (Routers, Services e Core), projetada para processar múltiplos arquivos de forma eficiente.

1.  **POST `/upload_filename/`**: **Feedback UX**. Retorna apenas os nomes dos arquivos para exibição imediata no frontend, sem processar o conteúdo.
2.  **POST `/extract_data/`**: **Processamento em Lote**. Recebe a lista de PDFs, itera sobre eles e retorna uma lista de resultados (status por arquivo + payload de dados).
3.  **POST `/get_csv/` ou `/download_csv/`**: **Relatórios**. Recebe os dados de sucesso e os formata em uma string CSV de múltiplas linhas.

---

## ⚙️ Guia de Execução Local

Siga os passos abaixo para configurar e rodar o projeto localmente.

### **Pré-requisitos**

* Python 3.10+
* Git

### **1. Clonagem e Configuração do Ambiente**

```bash
# 1. Clone o repositório
git clone [https://aws.amazon.com/pt/what-is/repo/](https://aws.amazon.com/pt/what-is/repo/)
cd CNPJ-SCAN-BACK/ # OU a pasta raiz do seu projeto

# 2. Crie e Ative o Ambiente Virtual
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Instale as Dependências
pip install -r requirements.txt

