import pytest
from fastapi.testclient import TestClient
from src.main import app 
from pathlib import Path

# 1. SETUP: Cria o cliente de teste.
client = TestClient(app)

# 2. DEFINIÇÃO DOS CAMINHOS DOS ARQUIVOS DE TESTE
# O path é relativo ao arquivo de teste atual (tests/routers/)
TEST_DIR = Path(__file__).parent
PDF_SAMPLE_1_PATH = "tests/resources/cnpj_sample1.pdf"
PDF_SAMPLE_2_PATH = "tests/resources/cnpj_sample2.pdf"


# --- FUNÇÃO AUXILIAR ---

def create_multipart_files(file_path_list):
    """
    Auxiliar para criar o formato 'files' que o TestClient espera para múltiplos uploads.
    Retorna a lista de arquivos prontos e os objetos abertos para que possam ser fechados.
    """
    files_to_send = []
    file_objects = []
    
    for p in file_path_list:
        path = Path(p)
        # Abre o arquivo em modo binário
        file_obj = open(path, "rb")
        file_objects.append(file_obj)
        
        # Cria a tupla no formato esperado pelo TestClient: (chave_do_form, (nome_do_arquivo, objeto_arquivo, media_type))
        files_to_send.append(
            ("files", (path.name, file_obj, "application/pdf"))
        )
    
    return files_to_send, file_objects


# --- TESTES ---

def test_upload_filename_200_returns_all_names():
    """
    Teste 1: Valida o endpoint /upload_filename/ para garantir que ele lista
    os nomes dos arquivos em um upload de lote.
    """
    file_paths = [PDF_SAMPLE_1_PATH, PDF_SAMPLE_2_PATH]
    files_to_send, file_objects = create_multipart_files(file_paths)
    
    try:
        response = client.post("/upload_filename/", files=files_to_send)
    finally:
        # Garantir que todos os objetos de arquivo sejam fechados
        for f_obj in file_objects:
            f_obj.close()
        
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["filename"] == "cnpj_sample1.pdf"
    assert data[1]["filename"] == "cnpj_sample2.pdf"


def test_extract_data_200_batch_two_successes():
    """
    Teste 2: Valida o cenário de SUCESSO EM LOTE.
    Garante que os dois arquivos válidos são processados corretamente e
    que a estrutura de retorno está correta.
    """
    file_paths = [PDF_SAMPLE_1_PATH, PDF_SAMPLE_2_PATH]
    files_to_send, file_objects = create_multipart_files(file_paths)

    try:
        response = client.post("/extract_data/", files=files_to_send)
    finally:
        # Garantir que todos os objetos de arquivo sejam fechados
        for f_obj in file_objects:
            f_obj.close()
        
    assert response.status_code == 200
    data = response.json()
    
    # 1. Verifica a estrutura da lista de resultados
    assert isinstance(data, list)
    assert len(data) == 2
    
    # 2. Verifica o CONTRATO para o primeiro item (Sucesso)
    assert data[0]["filename"] == "cnpj_sample1.pdf"
    assert data[0]["status"] == "OK"
    assert "extracted_data" in data[0]
    # O teste mais importante: garante que a extração funcionou
    assert "numero_de_inscricao" in data[0]["extracted_data"]
    
    # 3. Verifica o CONTRATO para o segundo item (Sucesso)
    assert data[1]["filename"] == "cnpj_sample2.pdf"
    assert data[1]["status"] == "OK"
    assert "extracted_data" in data[1]
    # O teste mais importante: garante que a extração funcionou
    assert "numero_de_inscricao" in data[1]["extracted_data"]