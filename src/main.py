from fastapi import FastAPI
from src.routers import cnpj

# Instancia principal da aplicação
app = FastAPI()

# Inclui o roteador na aplicação
app.include_router(cnpj.router)

# Definição de rota para o caminho raiz
@app.get("/")
def read_root():
    return {"message": "Bem vindo ao CNPJ Scan - Backend"}
