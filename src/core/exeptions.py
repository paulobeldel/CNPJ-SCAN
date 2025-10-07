"""
Módulo que define as exceções customizadas usadas na aplicação.
"""

class InvalidCNPJDocumentError(Exception):
    """Exceção levantada quando o documento PDF não é um cartão CNPJ válido."""
    pass

class InvalidReportDataError(Exception):
    """Exceção levantada quando os dados fornecidos para gerar o relatório são inválidos."""
    pass
