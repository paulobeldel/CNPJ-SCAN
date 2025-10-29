"""
Módulo que define os endpoints ligados a extração de dados do cartão CNPJ

Responsável por
- receber o arquivo PDF do frontend
- chamar o serviço de extração de dados
- retornar os dados em formato JSON
- lidar com erros
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.extraction_service import extract_data_from_pdf
from typing import Dict, Any, List

router = APIRouter()

#----------------------------------------------------------------
# 1. ENDPOINT PARA RETORNAR O NOME DOS ARQUIVOS
# .. Retorna apenas os nomes dos arquivos enviados sem ler o conteúdo.
#----------------------------------------------------------------
@router.post("/upload_filename/", tags=["CNPJ"])
async def get_filename(files: List[UploadFile] = File(...)):

    # Lista para armazenar os nomes dos arquivos
    filenames = []

    # Itera sobre os arquivos enviados
    for file in files:
        filenames.append({"filename": file.filename})

    # Retorna o nome de todos os arquivos
    return filenames

#----------------------------------------------------------------
# 2. ENDPOINT PARA EXTRAIR E PROCESSAR OS DADOS
# .. Analisa o conteúdo dos PDFs e retorna os dados extraídos
#----------------------------------------------------------------
@router.post("/extract_data/", tags=["CNPJ"])
async def extract(files: List[UploadFile] = File(...)):

    # Lista para armazenar os resultados de cada arquivo
    list_of_results = []

    # Iterar sobre os arquivos enviados
    for file in files:

        # Try..except para que um erro em um arquivo não afete os outros
        try:
            # Ler o conteudo do arquivo em bytes
            pdf_content = await file.read()
        
            # Chamar a função na camada de Services
            extracted_data = await extract_data_from_pdf(pdf_content)

            # Verificar se o dicionário contém a chave 'error'
            if 'error' in extracted_data:

                # Se tiver um erro, adicionar um JSON com status de falha
                list_of_results.append({
                    "filename": file.filename,
                    "status": extracted_data["error"],
                    "error": True
                })
            
            else:
                # Se não tiver erro, adicionar um JSON com os dados extraídos
                list_of_results.append({
                    "filename": file.filename,
                    "status": "OK",
                    "extracted_data": extracted_data.get("extracted_data", {})
                })
        
        except Exception as e:
            list_of_results.append({
                "filename": file.filename,
                "status": f"Falha na extração: {e}",
                "error": True
            })
    
    # Retornar a lista de resultados
    return list_of_results
