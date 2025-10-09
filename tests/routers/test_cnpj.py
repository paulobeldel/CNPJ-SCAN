from fastapi.testclient import TestClient
from src.main import app

# Criação do cliente de teste
client = TestClient(app)

# Caminho do PDF de teste
pdf_path = 'tests/resources/cnpj_sample.pdf'


# Teste de sucesso (200 OK)
def test_extract_data_200_success():

    # Abre o arquivo PDF em modo binário
    with open(pdf_path, 'rb') as file:

        # Simula o upload do arquivo via endpoint no formato multipart/form-data
        files = {'file': ('cnpj_sample.pdf', file, 'application/pdf')}
        response = client.post("/extract_data/", files=files)

    # Verifica se o status code é 200 (OK)
    assert response.status_code == 200

    data = response.json()

    #print("\nDEBUG DATA:", data) 

    # Verifica se o JSON retornado contém as chaves esperadas
    assert "filename" in data
    assert "extracted_data" in data

    # Verifica se um campo chave existe no dicionário extraído
    assert "numero_de_inscricao" in data["extracted_data"]


# Teste de erro (400 Bad Request)
def test_extract_data_400_invalid_file_type():
    # Simula o upload de um pdf corrompido
    files = {'file': ('corrupt_file.pdf', b'Arquivo corrompido.', 'application/pdf')}
    response = client.post("/extract_data/", files=files)

    # Verifica se o status code é 400 (Bad Request)
    assert response.status_code == 400

    data = response.json()

    #print("\nDEBUG ERROR DATA:", data) 

    # Verifica se o JSON retornado contém a chave 'detail' com a mensagem de erro esperada
    assert "detail" in data
    assert "Erro na extração" in data["detail"]


# Teste de extração de filename
def test_get_filename_200_success():
    # Abre o arquivo PDF em modo binário
    with open(pdf_path, 'rb') as file:

        # Simula o upload do arquivo via endpoint no formato multipart/form-data
        files = {'file': ('cnpj_sample.pdf', file, 'application/pdf')}
        response = client.post("/upload_filename/", files=files)

    # Verifica se o status code é 200 (OK)
    assert response.status_code == 200

    data = response.json()

    # Verifica se o JSON retornado contém a chave esperada
    assert "filename" in data

    # Verifica se o nome do arquivo está correto
    assert data["filename"] == "cnpj_sample.pdf"