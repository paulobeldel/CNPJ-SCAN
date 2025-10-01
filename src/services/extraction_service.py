import fitz
import io
import re


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

# --------------------
# (!) Quando tem "none" é porque os labels não foram encontrados
# Então o documento não é cartão cnpj
# --------------------


# Função para extrair as informações
async def extract_data_from_pdf(pdf_content: bytes):
    """
    Extrai informações de CNPJ de um PDF de formulário usando Regex.
    """
    # Dicionário onde ficarão os campos extraídos
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

    except Exception as e:
        return {"error": f"Erro ao processar o arquivo: {e}"}
    
        # (!) O tratamento de erros é basicamente inexistente..

    return extracted_data
