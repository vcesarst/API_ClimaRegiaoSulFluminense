import uvicorn
from app.api.endpoint import app

if __name__ == "__main__":
    print("="*60)
    print("🚀 INICIANDO API - SUL FLUMINENSE")
    print("="*60)
    print("\n📚 Documentação: http://localhost:8000/docs")
    print("📋 Alternativa: http://localhost:8000/redoc")
    print("\n🔍 Endpoints disponíveis:")
    print("   ✅ GET  / - Raiz")
    print("   ✅ GET  /cidades - Lista cidades")
    print("   ✅ GET  /temperaturas - Temperaturas atuais")
    print("   ✅ GET  /coleta-completa - Todos os dados")
    print("   ✅ GET  /historico?anos=2023 - Dados históricos")
    print("\n" + "="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)