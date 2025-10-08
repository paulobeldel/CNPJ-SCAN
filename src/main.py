"""
Módulo principal da aplicação FastAPI

Responsável por
- inicializar a aplicação FastAPI
- incluir os roteadores (de routers/) da API
"""

from fastapi import FastAPI
from src.routers import cnpj, reports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importe o CORSMiddlewar

# Instancia principal da aplicação
app = FastAPI()

# Defina as origens (endereços) que podem acessar sua API
origins = [
    "http://localhost:5173",  # Seu front-end (Vite/etc.)
    "http://127.0.0.1:5173",  # Alternativa de localhost
    
    # Se você tiver que acessar a API dela própria (Swagger UI)
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Lista de origens permitidas
    allow_credentials=True,            # Permite cookies de credenciais
    allow_methods=["*"],               # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],               # Permite todos os cabeçalhos
)

# Inclui o roteador na aplicação
app.include_router(cnpj.router)
app.include_router(reports.router)

# Definição de rota para o caminho raiz
@app.get("/")
def read_root():
    return {"message": "Bem vindo ao CNPJ Scan - Backend"}
