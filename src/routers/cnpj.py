"""
Módulo que define os endpoints ligados a extração de dados do cartão CNPJ

Responsável por
- receber o arquivo PDF do frontend
- chamar o serviço de extração de dados
- retornar os dados em formato JSON
- lidar com erros
"""

from fastapi import APIRouter, UploadFile, File
from src.services.extraction_service import extract_data_from_pdf
from typing import Dict, Any

router = APIRouter()


# Upload e extração de informações do PDF
# Recebe um arquivo e retorna um JSON com os dados
@router.post("/extract_data/")
async def upload(file: UploadFile = File(...)):

    # Falta o tratamento de erro (!)

    # Lê o conteudo do arquivo em bytes
    pdf_content = await file.read()

    # Chama a função na camada de Services
    extracted_data = await extract_data_from_pdf(pdf_content)

    # Retorna o JSON
    return extracted_data
