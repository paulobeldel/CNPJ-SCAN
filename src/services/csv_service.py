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

#----------------------------------------------------------------
# FUNÇÃO PARA GERAR O CSV
# .. Retorna o CSV como string
# .. extracted_data = { ... }
#----------------------------------------------------------------
def generate_csv_from_data(
        extracted_data: Dict[str, Any],
        field_names: list[str] = None
        ) -> str:
    """
    Transforma os dados extraídos em uma string CSV.
    Filtra os campos solicitados.
    """

    # Verificar se existem dados antes de tentar gerar o CSV
    if not extracted_data or 'error' in extracted_data:
        raise InvalidReportDataError("Não há dados válidos para gerar o CSV.")

    #print("\nDEBUG - Dados extraídos para CSV:", extracted_data)

    # Verificar se uma lista de campos foi passada
    if field_names and len(field_names) > 0:

        filtered_data = {}

        # Percorrer o dicionário e adicionar apenas os campos requisitados
        for key, value in extracted_data.items():
            if key in field_names:
                filtered_data[key] = value
        data_to_write = filtered_data

    else:

        # Se nenhum campo for especificado, usar todos os dados
        data_to_write = extracted_data

    # Usar StringIO para criar um arquivo em memória    
    output = io.StringIO(newline='')

    # Criar o escritor CSV
    writer = csv.writer(
        output, # arquivo em memória
        quoting=csv.QUOTE_MINIMAL
    )

    # Primeira linha - cabeçalho (keys do dicionario com os dados)
    header = list(data_to_write.keys())

    # Verificar se o header está vazio
    if not header:
        raise InvalidReportDataError("Nenhum campo válido foi fornecido para o relatório.")
    
    # Escrever o cabeçalho
    writer.writerow(header)

    # Segunda linha - valores (values do dicionario com os dados)
    row = list(data_to_write.values())

    # Escrever a linha de dados
    writer.writerow(row)

    # Retornar o conteúdo do CSV como string
    return output.getvalue()

