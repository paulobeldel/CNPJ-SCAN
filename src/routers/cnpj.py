from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, Query, Body, HTTPException
from fastapi.responses import Response
from src.services.extraction_service import extract_data_from_pdf
from src.services.csv_service import generate_csv_from_data

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


# Download do CSV
# Recebe os dados em JSON e retorna o arquivo CSV
@router.post("/download-csv/")
async def download_csv(
    data: Dict[str, Any] = Body(...),
    fields: list[str] = Query(None, description="Lista dos campos requisitados pelo usuario")
    ):

    try:
        csv_string = generate_csv_from_data(data, fields)

        return Response(
            content=csv_string,
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="cnpj_scan.csv"'}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")
    
        # Falta especificar as Exceptions (!)
    
    
