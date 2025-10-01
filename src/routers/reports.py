"""
Módulo que define os endpoints ligados a geração e download de relatórios.

Responsável por
- receber dados em JSON
- chamar serviço de geração de CSV
- retornar arquivo CSV para download
"""

from fastapi import APIRouter, Query, Body, HTTPException
from fastapi.responses import Response
from src.services.csv_service import generate_csv_from_data
from typing import Dict, Any

router = APIRouter()

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



