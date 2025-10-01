from fastapi import APIRouter, UploadFile, File, Query, Body, HTTPException
from fastapi.responses import Response
from src.services.extraction_service import extract_data_from_pdf
from src.services.csv_service import generate_csv_from_data
from typing import Dict, Any

router = APIRouter()


# Upload e extração de informações do PDF
# Recebe um arquivo e retorna um JSON com os dados
@router.post("/upload/")
async def upload(file: UploadFile = File(...)):

    # Falta o tratamento de erro (!)

    # Lê o conteudo do arquivo em bytes
    pdf_content = await file.read()

    # Chama a função na camada de Services
    extracted_data = await extract_data_from_pdf(pdf_content)

    # Retorna o JSON
    return extracted_data


    
    
