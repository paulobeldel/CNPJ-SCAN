import pytest
from src.services.extraction_service import _extract_field, extract_data_from_pdf

# Dados de exemplo para os testes
# Esse é o formato que a lib PyMuPDF extrai do PDF
sample_text = """
REPÚBLICA FEDERATIVA DO BRASIL   
CADASTRO NACIONAL DA PESSOA JURÍDICA
NÚMERO DE INSCRIÇÃO
58.351.146/0001-61
MATRIZ
COMPROVANTE DE INSCRIÇÃO E DE SITUAÇÃO
CADASTRAL
DATA DE ABERTURA
04/12/2024
NOME EMPRESARIAL
58.351.146 MARTHA LACERDA EMIDIO DA SILVA
TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)
********
PORTE
ME
CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL
85.92-9-03 - Ensino de música
CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS
85.92-9-99 - Ensino de arte e cultura não especificado anteriormente 
CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA
213-5 - Empresário (Individual)
LOGRADOURO
R DA MOEDA
NÚMERO
111
COMPLEMENTO
********
CEP
50.030-040
BAIRRO/DISTRITO
RECIFE
MUNICÍPIO
RECIFE
UF
PE
ENDEREÇO ELETRÔNICO
MARTHALACERDA89@GMAIL.COM
TELEFONE
(00) 0000-0000
ENTE FEDERATIVO RESPONSÁVEL (EFR)
*****
SITUAÇÃO CADASTRAL
ATIVA
DATA DA SITUAÇÃO CADASTRAL
04/12/2024
MOTIVO DE SITUAÇÃO CADASTRAL
SITUAÇÃO ESPECIAL
********
DATA DA SITUAÇÃO ESPECIAL
********
Aprovado pela Instrução Normativa RFB nº 2.119, de 06 de dezembro de 2022.
Emitido no dia 24/09/2025 às 18:36:46 (data e hora de Brasília).    
Página: 1/1
"""

# Padrões para os testes: lista de tuplas (campo, padrão regex, resultado esperado)
test_data = [
    ('numero_de_inscricao', r'NÚMERO DE INSCRIÇÃO.*?(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})', '58.351.146/0001-61'),
    ('data_de_abertura', r'DATA DE ABERTURA\s+([^\n]+)', '04/12/2024'),
    ('nome_empresarial', r'NOME EMPRESARIAL\s+(.*?)TÍTULO DO ESTABELECIMENTO', '58.351.146 MARTHA LACERDA EMIDIO DA SILVA'),
    ('nome_de_fantasia', r'\(NOME DE FANTASIA\)\s+(.*?)PORTE', '********'),
    ('porte', r'PORTE\s+([^\n]+)', 'ME'),
    ('atividade_principal', r'ATIVIDADE ECONÔMICA PRINCIPAL\s+(.*?)CÓDIGO', '85.92-9-03 - Ensino de música'),
    ('atividades_secundarias', r'ATIVIDADES ECONÔMICAS SECUNDÁRIAS\s+(.*?)CÓDIGO', '85.92-9-99 - Ensino de arte e cultura não especificado anteriormente'),
    ('natureza_juridica', r'NATUREZA JURÍDICA\s+(.*?)LOGRADOURO', '213-5 - Empresário (Individual)'),
    ('logradouro', r'LOGRADOURO\s+(.*?)NÚMERO', 'R DA MOEDA'),
    ('numero', r'LOGRADOURO.*?NÚMERO\s+([^\n]+)', '111'), # número que vem depois de logradouro
    ('complemento', r'COMPLEMENTO\s+([^\n]+)', '********'),
    ('cep', r'CEP\s+([^\n]+)', '50.030-040'),
    ('bairro', r'BAIRRO\/DISTRITO\s+([^\n]+)', 'RECIFE'),
    ('municipio', r'MUNICÍPIO\s+([^\n]+)', 'RECIFE'),
    ('uf', r'UF\s+([^\n]+)', 'PE'),
    ('email', r'ENDEREÇO ELETRÔNICO\s+(.*?)TELEFONE', 'MARTHALACERDA89@GMAIL.COM'),
    ('telefone', r'TELEFONE\s+([^\n]+)', '(00) 0000-0000'),
    ('efr', r'\(EFR\)\s+(.*?)SITUAÇÃO CADASTRAL', '*****'),
    ('situacao_cadastral', r'SITUAÇÃO CADASTRAL\s+(.*?)\s*DATA DA SITUAÇÃO CADASTRAL', 'ATIVA'),
    ('data_situacao_cadastral', r'DATA DA SITUAÇÃO CADASTRAL\s+([^\n]+)', '04/12/2024'),
    ('motivo_situacao_cadastral', r'MOTIVO DE SITUAÇÃO CADASTRAL\s+(.*?)SITUAÇÃO ESPECIAL', ''),
    ('situacao_especial', r'SITUAÇÃO ESPECIAL\s+(.*?)DATA DA SITUAÇÃO ESPECIAL', '********'),
    ('data_situacao_especial', r'DATA DA SITUAÇÃO ESPECIAL\s+([^\n]+)', '********')
]

# ----Testes do _extract_field----

# Parametrização dos testes (rodar o teste para cada padrão)
@pytest.mark.parametrize("field, pattern, expected", test_data)
def test_extract_field(field, pattern, expected):
    """
    Testa a extração de um campo (field)
    com um padrão específico (pattern)
    e verfica se o resultado é o esperado (expected).
    """
    extracted_result = _extract_field(sample_text, pattern)
    assert extracted_result == expected, f"Falha no campo {field}: Esperado '{expected}', Obtido '{extracted_result}'"

def test_extract_field_not_found():
    """Testa a extração de um campo com um padrão que não existe no texto, deve retornar None."""
    
    # Padrão que não existe no texto
    pattern = r'CAMPO QUALQUER INEXISTENTE\s+([^\n]+)'
    
    # Resultado esperado
    expected_result = _extract_field(sample_text, pattern)
    
    assert expected_result is None, f"Esperado None para campo inexistente, mas obteve '{expected_result}'"

# ----Testes do extract_data_from_pdf----

# É uma função async, então o teste também deve ser async
@pytest.mark.asyncio
async def test_extract_data_from_pdf():
    """Testa a extração de dados de um PDF"""
    
    # Caminho do PDF usado no teste
    pdf_path = 'tests/resources/cnpj_sample.pdf'

    # Dicionário com os dados esperados (transformar a lista do ppadrões de teste em dicionário)
    expected_data_payload = {key: value for key, _, value in test_data}
    
    # O resultado esperado é o payload dentro de outro dicionário
    expected_result = {"extracted_data": expected_data_payload}

    with open(pdf_path, 'rb') as file:
        pdf_content = file.read()
    
    result = await extract_data_from_pdf(pdf_content)

    assert result == expected_result, f"Falha na extração do PDF: Esperado {expected_result}, Obtido {result}"
