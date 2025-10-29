# CNPJ Scan - Processador Inteligente de Documentos

<div align="center">
  <img src="https://github.com/user-attachments/assets/7eaa9442-73cd-45f8-b601-843f0072179c">
</div>


## 🌟 Visão Geral do Projeto

Este projeto foi desenvolvido por estudantes do **NExT - Nova Experiência de Trabalho da CESAR School** como conclusão do curso.
É um processador de documentos com o objetivo principal de automatizar a extração de dados de Cartões CNPJ (Receita Federal) e convertê-los em um relatório CSV estruturado e filtrável.

O projeto é uma forma de demonstrar habilidades em arquitetura de microsserviços, programação assíncrona (`FastAPI`) e engenharia de dados (Regex e PyMyPDF), garantindo uma solução eficiente e segura.

---
> **Status:** MVP Finalizado - Extração de um Cartão CNPJ, validação e geração de relatório CSV.
---
.
## 🛠️ Tecnologias e Habilidades

A solução foi construída com foco em performance, manutenção e escalabilidade.

| Categoria | Ferramenta/Biblioteca | Habilidade Demonstrada |
| :--- | :--- | :--- |
| **Framework Principal** | **FastAPI** | Criação de APIs assíncronas e de alta performance. |
| **Configuração** | **Pydantic Settings** | Gestão e validação estruturada de variáveis de ambiente (`.env`) e configurações de CORS. |
| **Extração de Dados** | **PyMuPDF (`fitz`)** | Processamento robusto de documentos PDF e extração precisa de texto (solução para o problema de layouts de formulário). |
| **Lógica de Negócio** | **`re` (Regex)** | Engenharia de dados para identificar e extrair mais de 20 campos de formulários complexos. |
| **Relatórios** | **`csv`** | Geração eficiente de relatórios tabulares em formato CSV. |
| **Qualidade & Testes** | **`pytest` / `pytest-asyncio` / `httpx`** | Testes unitários e de integração para garantir a funcionalidade e a robustez da API. |
| **Arquitetura** | **`routers` / `services` / `core`** | Implementação do princípio da responsabilidade única e desacoplamento de código. |

---
.

## 🚀 Arquitetura e Fluxo de Trabalho

O projeto tem uma arquitetura modular de três camadas (Routers, Services e Core), projetada para processar arquivos de forma eficiente.

1. src/routers/cnpj.py: Orquestra o fluxo. Recebe os PDFs do frontend, itera sobre eles e chama o serviço para cada um.

2. src/services/extraction_service.py: A lógica de negócio. Recebe o PDF em bytes, extrai o texto com PyMuPDF e aplica os padrões Regex. Retorna um dicionário com os dados ou o motivo da falha.

3. src/routers/reports.py: Fluxo de geração e entrega de CSV. Gerencia a saída final de visualização ou download.

4. src/services/csv_service.py: Lógica de relatórios. Recebe os dados de sucesso e os formata em uma string CSV.

5. src/core/exceptions.py: Contém as exceções customizadas (InvalidCNPJDocumentError e InvalidReportDataError) para clareza no tratamento de erros de negócio.


Endpoints gerados:

1.  **POST `/upload_filename/`**: **Feedback UX**. Retorna apenas os nomes dos arquivos para exibição imediata no frontend, sem processar o conteúdo.
2.  **POST `/extract_data/`**: **Processamento de arquivo**. Recebe um PDF e retorna um resultado (status do arquivo + payload de dados).
3.  **POST `/get_csv/` ou `/download_csv/`**: **Relatórios**. Recebe os dados de sucesso e os formata em uma string CSV.

.

## ⚙️ Guia de Execução Local

Siga os passos abaixo para configurar e rodar o projeto localmente.

### **Pré-requisitos**

* Python 3.10+
* Git

### **1. Clonagem e Configuração do Ambiente**

```bash
# 1. Clone o repositório e entre na pasta raíz
git clone https://github.com/paulobeldel/CNPJ-SCAN.git

# 2. Crie e Ative o ambiente virtual
python -m venv venv

# Ativar no Windows (powershell):
.\venv\Scripts\activate

# Ativar no macOS/Linux (bash):
source venv/Scripts/activate

# 3. Instale as Dependências
pip install -r requirements.txt
```

### **2. Configuração de Variáveis de Ambiente**

Caso não exista um arquivo .env na raíz do projeto clonado (onde está o main.py), crie o .env e preencha conforme mostrado abaixo:

```bash
# Conteúdo do arquivo .env:
# --- Configurações de Segurança e API ---
SECRET_KEY="sua-chave-secreta-para-tokens-jwt-ou-sessao"
API_VERSION="v1.0"

# --- Configurações de Comunicação (CORS) ---
# URLs de onde o frontend React será acessado
CORS_ORIGINS="http://localhost:5173"
```

### **3. Inicialização do Servidor**

Execute o servidor Uvicorn a partir da raíz do projeto:

```bash
# Comando de execução do servidor
python -m uvicorn src.main:app --reload
```
Após a mensagem `Application startup complete.`, o servidor estará rodando no http mostrado no terminal - provavelmente `http://127.0.0.1:8000`

### **4. Documentação Interativa (/docs)**

Colocando um "/docs" no final do endereço (`http://127.0.0.1:8000/docs`), a documentação interativa do FastAPI (Swagger Ui) vai permitir que você teste os endpoints do projeto.

.
## ✅ Como Rodar os Testes
Para garantir a qualidade e a funcionalidade de cada módulo:

```bash
# Execute o pytest a partir da raiz do projeto
pytest
```
.
## 📜 Licença
Este projeto é de código aberto.

.
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

