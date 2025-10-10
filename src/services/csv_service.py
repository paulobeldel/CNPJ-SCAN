"""
Módulo de serviço de geração de CSV

Responsável por
- receber um dicionário de dados e uma lista de strings
- gerar o cabeçalho e as linhas do arquivo CSV
"""

from typing import Dict, Any, List
import csv
import io
from src.core.exceptions import InvalidReportDataError

#----------------------------------------------------------------
# FUNÇÃO PARA GERAR O CSV
# .. Retorna o CSV como string
# .. extracted_data = { ... }
#----------------------------------------------------------------
def generate_csv_from_data(
        extracted_data_list: List[Dict[str, Any]],
        field_filter: list[str] = None
        ) -> str:
    """
    Transforma a lista de dados extraídos em uma string CSV com múltiplas linhas.
    Filtra os campos solicitados.
    """

    # Verificar se a lista de dados está vazia
    if not extracted_data_list:
        raise InvalidReportDataError("Não há dados válidos para gerar o CSV.")

    #print("\nDEBUG - Dados extraídos para CSV:", extracted_data)

    # Lista com dados válidos (sem erros)
    valid_data = [data for data in extracted_data_list if "error" not in data]
    
    #print(f"\nDEBUG - Dados válidos para CSV: {valid_data}")

    # Pegar as chaves do primeiro dicionário para o HEADER do csv
    first_data_fields = list(valid_data[0]["extracted_data"].keys())

    # Verificar se uma lista de campos foi passada
    if field_filter and len(field_filter) > 0:

        # Filtrar os campos e determinar o HEADER
        header = [field for field in first_data_fields if field in field_filter]

    else:
        # Usar todos os campos
        header = first_data_fields

    # Verificar se o header está vazio
    if not header:
        raise InvalidReportDataError("Nenhum campo válido foi fornecido para o relatório.")
    
    # Gerar o CSV
    output = io.StringIO(newline='')
    writer = csv.writer(
        output, # arquivo em memória
        quoting=csv.QUOTE_MINIMAL
    )

    # Escrever o cabeçalho
    writer.writerow(header)

    # Escrever as linhas de dados - uma linha por dicionário na lista
    for data in valid_data:

        # Criar a linha com os valores na ordem do header
        row_values = [str(data["extracted_data"].get(field)) for field in header]
        writer.writerow(row_values)

    # Retornar o conteúdo do CSV como string
    return output.getvalue()
