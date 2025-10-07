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


# Upload e extração de informações do PDF
# Recebe um arquivo e retorna um JSON com os dados
@router.post("/extract_data/")
async def upload(file: UploadFile = File(...)):

    # Lê o conteudo do arquivo em bytes
    pdf_content = await file.read()

    # Chama a função na camada de Services
    extracted_data = await extract_data_from_pdf(pdf_content)

    # Verifica se a camada de serviço retornou um erro
    if 'error' in extracted_data:
        # Levanta um erro HTTP
        raise HTTPException(
            status_code=400,
            detail=f"Erro na extração: {extracted_data['error']}"
        )

    # Em caso de sucesso retornar os dados extraídos
    return extracted_data

   
