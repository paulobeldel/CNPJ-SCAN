"""
Módulo de serviço de extração de dados do cartão CNPJ

Responsável por
- receber conteúdo de um PDF
- extrair o texto com a lib PyMuPDF
- extrair os dados do PDF buscando os campos com padrões de Regex
- lidar com erros
"""

import fitz
import re
from typing import Dict, Any
from src.core.exeptions import InvalidCNPJDocumentError


# Função auxiliar para procurar padrões de texto
def _extract_field(text: str, pattern: str, group_index: int = 1) -> str | None:
    """
    Procura por um padrão de Regex e retorna o texto capturado.
    Retorna None se o padrão não for encontrado.
    """
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(group_index).strip()
    return None


# Função para extrair as informações
async def extract_data_from_pdf(pdf_content: bytes) -> Dict[str, Any]:
    """
    Extrai informações de CNPJ de um PDF de formulário usando Regex.
    """

    # Estrutura onde ficarão os campos extraídos
    extracted_data = {}
    
    # Dicionário com as labels dos campos e os padrões que serão procurados no PDF
    field_patterns = {
        'numero_de_inscricao': r'NÚMERO DE INSCRIÇÃO.*?(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})',
        'data_de_abertura': r'DATA DE ABERTURA\s+([^\n]+)',
        'nome_empresarial': r'NOME EMPRESARIAL\s+(.*?)TÍTULO DO ESTABELECIMENTO',
        'nome_de_fantasia': r'\(NOME DE FANTASIA\)\s+(.*?)PORTE',
        'porte': r'PORTE\s+([^\n]+)',
        'atividade_principal': r'ATIVIDADE ECONÔMICA PRINCIPAL\s+(.*?)CÓDIGO',
        'atividades_secundarias': r'ATIVIDADES ECONÔMICAS SECUNDÁRIAS\s+(.*?)CÓDIGO',
        'natureza_juridica': r'NATUREZA JURÍDICA\s+(.*?)LOGRADOURO',
        'logradouro': r'LOGRADOURO\s+(.*?)NÚMERO',
        'numero': r'LOGRADOURO.*?NÚMERO\s+([^\n]+)', # número que vem depois de logradouro
        'complemento': r'COMPLEMENTO\s+([^\n]+)',
        'cep': r'CEP\s+([^\n]+)',
        'bairro': r'BAIRRO\/DISTRITO\s+([^\n]+)',
        'municipio': r'MUNICÍPIO\s+([^\n]+)',
        'uf': r'UF\s+([^\n]+)',
        'email': r'ENDEREÇO ELETRÔNICO\s+(.*?)TELEFONE',
        'telefone': r'TELEFONE\s+([^\n]+)',
        'efr': r'\(EFR\)\s+(.*?)SITUAÇÃO CADASTRAL',
        'situacao_cadastral': r'SITUAÇÃO CADASTRAL\s+(.*?)\s*DATA DA SITUAÇÃO CADASTRAL',
        'data_situacao_cadastral': r'DATA DA SITUAÇÃO CADASTRAL\s+([^\n]+)',
        'motivo_situacao_cadastral': r'MOTIVO DE SITUAÇÃO CADASTRAL\s+(.*?)SITUAÇÃO ESPECIAL',
        'situacao_especial': r'SITUAÇÃO ESPECIAL\s+(.*?)DATA DA SITUAÇÃO ESPECIAL',
        'data_situacao_especial': r'DATA DA SITUAÇÃO ESPECIAL\s+([^\n]+)'
    }

    try:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        page = doc[0]
        full_text = page.get_text("text")

        for field, pattern in field_patterns.items():
            extracted_data[field] = _extract_field(full_text, pattern)

        # Verifica se o campo número de inscrição foi encontrado
        if not extracted_data.get('numero_de_inscricao'):
            raise InvalidCNPJDocumentError("O documento PDF não é um cartão CNPJ válido.")

    except InvalidCNPJDocumentError as e:
        return {"error": str(e)}
    except fitz.FileDataError:
        return {"error": "O arquivo fornecido não é um PDF válido ou está corrompido."}
    except IndexError:
        # Captura erros ao acessar páginas inexistentes
        return {"error": "O PDF não contém páginas ou a página solicitada não existe."}
    except re.error as regex_error:
        return {"error": f"Erro na expressão regular: {regex_error}"}

    return extracted_data
