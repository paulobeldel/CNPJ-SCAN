from fastapi.testclient import TestClient
from src.main import app


# Criação do cliente de teste
client = TestClient(app)

# Dados de teste: o payload completo esperado do frontend
SUCCESS_PAYLOAD_1 = {
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
}
SUCCESS_PAYLOAD_2 = {
  "filename": "file_2.pdf",
  "extracted_data": {
    "numero_de_inscricao": "22.222.222/0001-22",
    "data_de_abertura": "04/10/2024",
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
}

# Payload de teste com múltiplos arquivos
test_payload = [SUCCESS_PAYLOAD_1, SUCCESS_PAYLOAD_2]

# CSV esperado gerado a partir dos dados de teste acima
expeted_csv = "numero_de_inscricao;data_de_abertura;nome_empresarial;nome_de_fantasia;porte;atividade_principal;atividades_secundarias;natureza_juridica;logradouro;numero;complemento;cep;bairro;municipio;uf;email;telefone;efr;situacao_cadastral;data_situacao_cadastral;motivo_situacao_cadastral;situacao_especial;data_situacao_especial\n11.111.111/0001-11;04/12/2024;NOME EMPRESARIAL TESTE 1;********;ME;85.92-9-03 - Ensino de música;85.92-9-99 - Ensino de arte e cultura não especificado anteriormente;213-5 - Empresário (Individual);R DA MOEDA;111;********;50.030-040;RECIFE;RECIFE;PE;EMAILTESTE1@GMAIL.COM;(00) 0000-0000;*****;ATIVA;04/12/2024;;********;********\n22.222.222/0001-22;04/10/2024;NOME EMPRESARIAL TESTE 2;********;ME;85.92-9-03 - Ensino de música;85.92-9-99 - Ensino de arte e cultura não especificado anteriormente;213-5 - Empresário (Individual);R DA MOEDA;111;********;50.030-040;RECIFE;RECIFE;PE;EMAILTESTE2@GMAIL.COM;(00) 0000-0000;*****;ATIVA;04/12/2024;;********;********\n"


# Teste de sucesso (200 OK) para geração de relatório CSV
def test_generate_csv_200_all_fields():
    """
    Testa o endpoint de geração de relatório CSV com todos os campos.
    Verifica se o status code é 200 e se o conteúdo do CSV está correto.
    """
  
    # Simula o envio do payload via endpoint
    response = client.post("/get_csv/", json=test_payload)

    # Normaliza o texto para remover diferenças de quebras de linha entre SOs
    response_text_normalized = response.text.replace('\r\n', '\n')
    
    # Verifica se o status code é 200 (OK)
    assert response.status_code == 200

    # Verifica se o tipo de conteúdo da resposta é 'text/csv'
    assert "text/csv" in response.headers["content-type"]

    # Verifica se o conteúdo da resposta é igual ao CSV esperado
    assert response_text_normalized == expeted_csv


# Teste de erro (400 Bad Request) para geração de relatório CSV com dados vazios
def test_generate_csv_400_empty_data():
    """
    Testa o endpoint de geração de relatório CSV com dados vazios.
    Verifica se o status code é 400 e se a mensagem de erro está correta.
    """
    # Payload com dados extraídos vazios
    empty_data_payload = []

    # Simula o envio do payload via endpoint
    response = client.post("/download_csv/", json=empty_data_payload)

    # Verifica se o status code é 400 (Bad Request)
    assert response.status_code == 400

    data = response.json()

    #print("\nDEBUG ERROR DATA:", data) 

    # Verifica se o JSON retornado contém a chave 'detail' com a mensagem de erro esperada
    assert "detail" in data
    assert "Não há dados válidos para gerar o CSV." in data["detail"]


# Teste de sucesso (200 OK) para geração de relatório CSV com campos filtrados
def test_generate_csv_200_filtered_fields():
    """
      Testa o endpoint de geração de relatório CSV com campos filtrados via query params.
      Verifica se o status code é 200 e se o conteúdo do CSV está correto.
    """

    # Filtra por campos específicos
    url_with_query = "/download_csv/?fields=numero_de_inscricao&fields=nome_empresarial&fields=atividade_principal"

    expeted_csv = "numero_de_inscricao;nome_empresarial;atividade_principal\n11.111.111/0001-11;NOME EMPRESARIAL TESTE 1;85.92-9-03 - Ensino de música\n22.222.222/0001-22;NOME EMPRESARIAL TESTE 2;85.92-9-03 - Ensino de música\n"

    # Simula o envio do payload via endpoint com query params
    response = client.post(url_with_query, json=test_payload)

    # Normaliza o texto para remover diferenças de quebras de linha entre SOs
    response_text_normalized = response.text.replace('\r\n', '\n')

    # Verifica se o status code é 200 (OK)
    assert response.status_code == 200

    # Verifica se o tipo de conteúdo da resposta é 'text/csv'
    assert "text/csv" in response.headers["content-type"]

    # Verifica se o conteúdo da resposta é igual ao CSV esperado
    assert response_text_normalized == expeted_csv
  