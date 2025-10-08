from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Indica ao Pydantic para tentar ler o .env
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )

    # Variaveis criticas (usadas internamente)
    SECRET_KEY: str
    API_VERSION: str = "v1.0" # Pode ter um valor padrao

    # Configuracoes de CORS (o FastAPI espera uma lista)
    CORS_ORIGINS: str = "*"
    
    # Propriedade para converter a string de origens em uma lista de strings
    @property
    def list_cors_origins(self) -> List[str]:
        # Divide a string por virgula e remove espacos em branco
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]


# Instancia unica de configuracao para usar em toda a aplicacao
settings = Settings()
