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
from typing import Dict, Any

router = APIRouter()

#----------------------------------------------------------------
# 1. ENDPOINT PARA RETORNAR O NOME DO ARQUIVO
# .. Retorna apenas os nomes dos arquivos enviados sem ler o conteúdo.
#----------------------------------------------------------------
@router.post("/upload_filename/", tags=["CNPJ"])
async def get_filename(file: UploadFile = File(...)):

    # Retorna o nome do arquivo
    return {
        "filename": file.filename
    }

#----------------------------------------------------------------
# 2. ENDPOINT PARA EXTRAIR E PROCESSAR OS DADOS
# .. Analisa o conteúdo do PDF e retorna os dados extraídos ou erros.
#----------------------------------------------------------------
@router.post("/extract_data/", tags=["CNPJ"])
async def extract(file: UploadFile = File(...)):

    try:

        # Ler o conteudo do arquivo em bytes
        pdf_content = await file.read()
        
        # Chamar a função na camada de Services
        extracted_data = await extract_data_from_pdf(pdf_content)

        # Verifica se o dicionário contém a chave 'error'
        if 'error' in extracted_data:
            # Levanta um erro HTTP
            raise HTTPException(
                status_code=400,
                detail=f"Erro na extração: {extracted_data['error']}"
            )

        # Retorno de sucesso (200 OK)
        return {
            "filename": file.filename,
            "status": "Processado com sucesso",
            "extracted_data": extracted_data.get("extracted_data", {})
        }
    
    except HTTPException as http_e:
        # Repassa o erro HTTP levantado anteriormente
        raise http_e from http_e
    
    except Exception as e:
        # Captura qualquer outro erro inesperado
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor: {e}"
        ) from e
