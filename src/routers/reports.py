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
from src.core.exceptions import InvalidReportDataError

router = APIRouter()

#----------------------------------------------------------------
# 1. ENDPOINT PARA CRIAR E BAIXAR O RELATÓRIO CSV
# .. Recebe os dados em JSON e retorna o arquivo CSV para download
# .. estrutura de data = { "extracted_data": { ... } }
#----------------------------------------------------------------
@router.post("/download_csv/", tags=["Reports"])
async def download_csv(

    data: Dict[str, Any] = Body(...),
    fields: list[str] = Query(None, description="Campos para filtrar os dados no CSV")

    ):

    try:

        # Pegar os dados da chave extracted_data do dicionário recebido
        extracted_data = data.get("extracted_data", {})

        # Chamar a função para gerar o CSV da camada de Services
        csv_string = generate_csv_from_data(extracted_data, fields)

        # Retornar o CSV como resposta para download
        return Response(
            content=csv_string, # Conteúdo do CSV
            media_type="text/csv", # Tipo de mídia do CSV
            headers={"Content-Disposition": 'attachment; filename="cnpj_scan.csv"'} # Força o download com nome do arquivo
        )
    
    except InvalidReportDataError as e:
        # O usuário enviou dados inválidos ou vazios
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e

    except Exception as e:
        # Qualquer outro erro inesperado
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao gerar o relatório: {e}"
        ) from e


#----------------------------------------------------------------
# 2. ENDPOINT PARA CRIAR E RETORNAR O RELATÓRIO CSV
# .. Recebe os dados em JSON e retorna o arquivo CSV sem download
# .. estrutura de data = { "extracted_data": { ... } }
#----------------------------------------------------------------
@router.post("/get_csv/", tags=["Reports"])
async def get_csv(

    data: Dict[str, Any] = Body(...),
    fields: list[str] = Query(None, description="Campos para filtrar os dados no CSV")

    ):

    try:

        # Pegar os dados da chave extracted_data do dicionário recebido
        extracted_data = data.get("extracted_data", {})

        # Chamar a função para gerar o CSV da camada de Services
        csv_string = generate_csv_from_data(extracted_data, fields)

        # Retornar o CSV como resposta sem forçar download
        return Response(
            content=csv_string, # Conteúdo do CSV
            media_type="text/csv" # Tipo de mídia do CSV
        )
    
    except InvalidReportDataError as e:
        # O usuário enviou dados inválidos ou vazios
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e

    except Exception as e:
        # Qualquer outro erro inesperado
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao gerar o relatório: {e}"
        ) from e