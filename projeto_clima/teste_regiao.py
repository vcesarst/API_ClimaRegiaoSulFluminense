import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.coletores.coletor_dados import DataCollector

load_dotenv()

def testar_sistema_completo():
    """Testa o sistema completo"""
    print("="*60)
    print("🌍 TESTE COMPLETO - SUL FLUMINENSE")
    print("="*60)
    
    # Inicializa coletor com chave da API
    api_key = os.getenv("OPENWEATHER_API_KEY")
    coletor = DataCollector(api_key)
    
    # Executa coleta completa
    resultados = coletor.coletar_dados_completos()
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("="*60)

if __name__ == "__main__":
    testar_sistema_completo()