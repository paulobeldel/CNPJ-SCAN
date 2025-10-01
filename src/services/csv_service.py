from typing import Dict, Any
import csv
import io

def generate_csv_from_data(
        extracted_data: Dict[str, Any],
        field_names: list[str] = None
        ):
    """
    Transforma os dados extraídos em uma string CSV.
    Filtra os campos solicitados.
    """

    # Filtrar se uma lista de campos foi passada
    if field_names and len(field_names) > 0:
        filtered_data = {}
        for key, value in extracted_data.items():
            if key in field_names:
                filtered_data[key] = value
        data_to_write = filtered_data
    else:
        data_to_write = extracted_data
    
    output = io.StringIO()
    writer = csv.writer(output)

    # Primeira linha - cabeçalhos (keys do dict)
    header = list(data_to_write.keys())
    writer.writerow(header)

    # Segunda linha - valores (values do dict)
    row = list(data_to_write.values())
    writer.writerow(row)

    return output.getvalue()
