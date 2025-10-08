"""
Módulo de serviço de geração de CSV

Responsável por
- receber um dicionário de dados e uma lista de strings
- gerar o cabeçalho e as linhas do arquivo CSV
"""

from typing import Dict, Any
import csv
import io
from src.core.exceptions import InvalidReportDataError

def generate_csv_from_data(
        extracted_data: Dict[str, Any],
        field_names: list[str] = None
        ) -> str:
    """
    Transforma os dados extraídos em uma string CSV.
    Filtra os campos solicitados.
    """

    # Verifica se existem dados antes de tentar gerar o CSV
    if not extracted_data or 'error' in extracted_data:
        raise InvalidReportDataError("Não há dados válidos para gerar o CSV.")

    #print("\nDEBUG - Dados extraídos para CSV:", extracted_data)

    # Filtrar se uma lista de campos foi passada
    if field_names and len(field_names) > 0:
        filtered_data = {}
        for key, value in extracted_data.items():
            if key in field_names:
                filtered_data[key] = value
        data_to_write = filtered_data
    else:
        data_to_write = extracted_data
    
    output = io.StringIO(newline='')
    writer = csv.writer(
        output,
        quoting=csv.QUOTE_MINIMAL,
    )

    # Primeira linha - cabeçalhos (keys do dict)
    header = list(data_to_write.keys())
    # Verifica se o header está vazio
    if not header:
        raise InvalidReportDataError("Nenhum campo válido foi fornecido para o relatório.")
    writer.writerow(header)

    # Segunda linha - valores (values do dict)
    row = list(data_to_write.values())
    writer.writerow(row)

    return output.getvalue()
