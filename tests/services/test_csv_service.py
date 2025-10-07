import pytest
from src.services.csv_service import generate_csv_from_data
from typing import Dict, Any
from src.core.exeptions import InvalidReportDataError

# Dados de exemplo para os testes

test_data = {
  "numero_de_inscricao": "58.351.146/0001-61",
  "data_de_abertura": "04/12/2024",
  "nome_empresarial": "58.351.146 MARTHA LACERDA EMIDIO DA SILVA",
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
  "email": "MARTHALACERDA89@GMAIL.COM",
  "telefone": "(00) 0000-0000",
  "efr": "*****",
  "situacao_cadastral": "ATIVA",
  "data_situacao_cadastral": "04/12/2024",
  "motivo_situacao_cadastral": "",
  "situacao_especial": "********",
  "data_situacao_especial": "********"
}

def test_generate_csv_all_fields():
    """Testa a geração de CSV com todos os campos."""

    # Resultado esperado
    expected_header = "numero_de_inscricao,data_de_abertura,nome_empresarial,nome_de_fantasia,porte,atividade_principal,atividades_secundarias,natureza_juridica,logradouro,numero,complemento,cep,bairro,municipio,uf,email,telefone,efr,situacao_cadastral,data_situacao_cadastral,motivo_situacao_cadastral,situacao_especial,data_situacao_especial\r"
    expected_row = "58.351.146/0001-61,04/12/2024,58.351.146 MARTHA LACERDA EMIDIO DA SILVA,********,ME,85.92-9-03 - Ensino de música,85.92-9-99 - Ensino de arte e cultura não especificado anteriormente,213-5 - Empresário (Individual),R DA MOEDA,111,********,50.030-040,RECIFE,RECIFE,PE,MARTHALACERDA89@GMAIL.COM,(00) 0000-0000,*****,ATIVA,04/12/2024,,********,********\r"

    expected_csv = f"{expected_header}\n{expected_row}\n"

    # Gera o CSV
    csv_result = generate_csv_from_data(test_data)

    assert csv_result == expected_csv

def test_generate_csv_selected_fields():
    """Testa a geração de CSV com campos selecionados."""

    selected_fields = ['numero_de_inscricao', 'nome_empresarial', 'cep', 'municipio', 'uf', 'telefone']

    # Resultado esperado
    expected_header = "numero_de_inscricao,nome_empresarial,cep,municipio,uf,telefone\r"
    expected_row = "58.351.146/0001-61,58.351.146 MARTHA LACERDA EMIDIO DA SILVA,50.030-040,RECIFE,PE,(00) 0000-0000\r"

    expected_csv = f"{expected_header}\n{expected_row}\n"

    # Gera o CSV
    csv_result = generate_csv_from_data(test_data, field_names=selected_fields)

    assert csv_result == expected_csv

def test_generate_csv_empty_data():
    """Testa a geração de CSV com dados vazios."""

    empty_data = {}

    # Resultado esperado -> Erro levantado
    with pytest.raises(InvalidReportDataError) as exc_info:
        generate_csv_from_data(empty_data)

    assert "Não há dados válidos para gerar o CSV." in str(exc_info.value)