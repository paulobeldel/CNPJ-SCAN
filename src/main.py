from fastapi import FastAPI
from src.routers import cnpj, reports

# Instancia principal da aplicação
app = FastAPI()

# Inclui o roteador na aplicação
app.include_router(cnpj.router)
app.include_router(reports.router)

# Definição de rota para o caminho raiz
@app.get("/")
def read_root():
    return {"message": "Bem vindo ao CNPJ Scan - Backend"}
