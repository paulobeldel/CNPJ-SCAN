import pytest
from src.services.csv_service import generate_csv_from_data
from typing import Dict, Any
from src.core.exceptions import InvalidReportDataError

# Dados de exemplo para os testes

test_data = [{
  "filename": "file_1.pdf",
  "extracted_data": {
    "numero_de_inscricao": "11.111.111/0001-11",
    "data_de_abertura": "04/12/2024",
    "nome_empresarial": "NOME EMPRESARIAL TESTE 1",
    "nome_de_fantasia": "********",
    "porte": "ME",
    "atividade_principal": "85.92-9-03 - Ensino de música",
    "atividades_secundarias": "85.92-9-99 - Ensino de arte e cultura não especificado anteriormente",
    "natureza_juridica": "213-5 - Empresário (Individual)",
    "logradouro": "R DA MOEDA",
    "numero": "111",
    "complemento": "********",
    "cep": "50.030-040",
    "bairro": "RECIFE",
    "municipio": "RECIFE",
    "uf": "PE",
    "email": "EMAILTESTE1@GMAIL.COM",
    "telefone": "(00) 0000-0000",
    "efr": "*****",
    "situacao_cadastral": "ATIVA",
    "data_situacao_cadastral": "04/12/2024",
    "motivo_situacao_cadastral": "",
    "situacao_especial": "********",
    "data_situacao_especial": "********"
  }
},
{
  "filename": "file_2.pdf",
  "extracted_data": {
    "numero_de_inscricao": "22.222.222/0001-22",
    "data_de_abertura": "04/12/2024",
    "nome_empresarial": "NOME EMPRESARIAL TESTE 2",
    "nome_de_fantasia": "********",
    "porte": "ME",
    "atividade_principal": "85.92-9-03 - Ensino de música",
    "atividades_secundarias": "85.92-9-99 - Ensino de arte e cultura não especificado anteriormente",
    "natureza_juridica": "213-5 - Empresário (Individual)",
    "logradouro": "R DA MOEDA",
    "numero": "111",
    "complemento": "********",
    "cep": "50.030-040",
    "bairro": "RECIFE",
    "municipio": "RECIFE",
    "uf": "PE",
    "email": "EMAILTESTE2@GMAIL.COM",
    "telefone": "(00) 0000-0000",
    "efr": "*****",
    "situacao_cadastral": "ATIVA",
    "data_situacao_cadastral": "04/12/2024",
    "motivo_situacao_cadastral": "",
    "situacao_especial": "********",
    "data_situacao_especial": "********"
  } 
}]

def test_generate_csv_all_fields():
    """Testa a geração de CSV com todos os campos."""

    # Resultado esperado
    expected_csv = "numero_de_inscricao;data_de_abertura;nome_empresarial;nome_de_fantasia;porte;atividade_principal;atividades_secundarias;natureza_juridica;logradouro;numero;complemento;cep;bairro;municipio;uf;email;telefone;efr;situacao_cadastral;data_situacao_cadastral;motivo_situacao_cadastral;situacao_especial;data_situacao_especial\n11.111.111/0001-11;04/12/2024;NOME EMPRESARIAL TESTE 1;********;ME;85.92-9-03 - Ensino de música;85.92-9-99 - Ensino de arte e cultura não especificado anteriormente;213-5 - Empresário (Individual);R DA MOEDA;111;********;50.030-040;RECIFE;RECIFE;PE;EMAILTESTE1@GMAIL.COM;(00) 0000-0000;*****;ATIVA;04/12/2024;;********;********\n22.222.222/0001-22;04/12/2024;NOME EMPRESARIAL TESTE 2;********;ME;85.92-9-03 - Ensino de música;85.92-9-99 - Ensino de arte e cultura não especificado anteriormente;213-5 - Empresário (Individual);R DA MOEDA;111;********;50.030-040;RECIFE;RECIFE;PE;EMAILTESTE2@GMAIL.COM;(00) 0000-0000;*****;ATIVA;04/12/2024;;********;********\n"

    # Gera o CSV
    csv_result = generate_csv_from_data(test_data)
    csv_result = csv_result.replace('\r\n', '\n')
    assert csv_result == expected_csv

def test_generate_csv_selected_fields():
    """Testa a geração de CSV com campos selecionados."""

    selected_fields = ['numero_de_inscricao', 'email']

    # Resultado esperado
    expected_csv = "numero_de_inscricao;email\n11.111.111/0001-11;EMAILTESTE1@GMAIL.COM\n22.222.222/0001-22;EMAILTESTE2@GMAIL.COM\n"

    # Gera o CSV
    csv_result = generate_csv_from_data(test_data, field_filter=selected_fields)
    csv_result = csv_result.replace('\r\n', '\n')
    assert csv_result == expected_csv

def test_generate_csv_empty_data():
    """Testa a geração de CSV com dados vazios."""

    empty_data = []

    # Resultado esperado -> Erro levantado
    with pytest.raises(InvalidReportDataError) as exc_info:
        generate_csv_from_data(empty_data)

    assert "Não há dados válidos para gerar o CSV." in str(exc_info.value)