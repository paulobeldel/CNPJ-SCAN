"""
Módulo principal da aplicação FastAPI

Responsável por
- inicializar a aplicação FastAPI
- incluir os roteadores (de routers/) da API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import cnpj, reports
from config import settings # Importa as configuracoes

# Define o titulo da API usando a variavel
app = FastAPI(title=f"Minha API - {settings.API_VERSION}")

# 1. Configurando o CORS (MUITO importante para o React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.list_cors_origins, # Permite que o frontend se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia principal da aplicação
# app = FastAPI()

# Inclui o roteador na aplicação
app.include_router(cnpj.router)
app.include_router(reports.router)

# Definição de rota para o caminho raiz
@app.get("/")
def read_root():
    return {"message": "Bem vindo ao CNPJ Scan - Backend"}
