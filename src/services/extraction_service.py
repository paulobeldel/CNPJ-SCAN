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
from src.core.exceptions import InvalidCNPJDocumentError

#----------------------------------------------------------------
# FUNÇÃO AUXILIAR PARA PROCURAR PADRÕES DE TEXTO 
#----------------------------------------------------------------

def _extract_field(text: str, pattern: str, group_index: int = 1) -> str | None:
    """
    Procura por um padrão de Regex e retorna o texto capturado.
    Retorna None se o padrão não for encontrado.
    """

    # re.search procura o padrão em qualquer lugar do texto
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    # Se encontrou, retorna o grupo capturado
    if match:
        return match.group(group_index).strip()
    
    return None


#----------------------------------------------------------------
# FUNÇÃO PRINCIPAL PARA EXTRAIR OS DADOS DO PDF
# .. Retorna um dicionário com os campos extraídos ou um erro.
#----------------------------------------------------------------

async def extract_data_from_pdf(pdf_content: bytes) -> Dict[str, Any]:
    """
    Extrai informações de CNPJ de um PDF de formulário usando Regex.
    """

    # Estrutura onde ficarão os campos extraídos
    extracted_data = {}
    
    # Dicionário com os campos e os padrões de texto que serão procurados no PDF
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

        # Abrir o PDF com PyMuPDF
        doc = fitz.open(stream=pdf_content, filetype="pdf")

        # Extrair o texto da primeira página
        page = doc[0]

        # Pegar o texto completo
        full_text = page.get_text("text")

        # Percorrer o dicionário de campos e padrões e extrair os dados
        for field, pattern in field_patterns.items():
            extracted_data[field] = _extract_field(full_text, pattern)

        # Validar se alguns campos essenciais foram encontrados
        if not extracted_data.get('numero_de_inscricao') and not extracted_data.get('nome_empresarial'):
            raise InvalidCNPJDocumentError("Não é um cartão CNPJ válido.")

    except InvalidCNPJDocumentError as e:
        return {"error": str(e)}
    
    except fitz.FileDataError:
        return {"error": "O arquivo fornecido não é um PDF válido ou está corrompido."}
    
    except IndexError:
        # Captura erros ao acessar páginas inexistentes
        return {"error": "O PDF não contém páginas ou a página solicitada não existe."}
    
    except re.error as regex_error:
        return {"error": f"Erro na expressão regular: {regex_error}"}
    
    except Exception as e:
        return {"error": f"Erro inesperado ao processar o PDF: {e}"}

    # Retornar os dados extraídos
    return {"extracted_data": extracted_data}
