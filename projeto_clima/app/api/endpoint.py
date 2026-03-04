from fastapi import FastAPI, HTTPException
from ..coletores.coletor_dados import DataCollector
from ..core.config import settings
import pandas as pd

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Inicializa o coletor
coletor = DataCollector(api_key=settings.OPENWEATHER_API_KEY)

@app.get("/")
def root():
    """Bem-vindo à API"""
    return {
        "message": "API Clima - Sul Fluminense",
        "endpoints": [
            "/cidades",
            "/temperaturas",
            "/coleta-completa",
            "/historico?anos=2023"
        ]
    }

@app.get("/cidades")
def listar_cidades():
    """Lista todas as cidades do Sul Fluminense"""
    return {"cidades": coletor.cidades_sul_fluminense}

@app.get("/temperaturas")
def temperaturas_atuais():
    """Retorna temperaturas atuais de todas as cidades"""
    dados = coletor.coletar_dados_completos()
    return dados['temperaturas']

@app.get("/coleta-completa")
def coleta_completa():
    """Retorna todos os dados coletados"""
    return coletor.coletar_dados_completos()

@app.get("/historico")
def dados_historicos(anos: str = "2023"):
    """Retorna dados históricos para os anos especificados"""
    anos_list = [int(a) for a in anos.split(",")]
    df = coletor.buscar_historico(anos_list)
    if df.empty:
        raise HTTPException(404, "Dados não encontrados")
    return df.to_dict(orient='records')