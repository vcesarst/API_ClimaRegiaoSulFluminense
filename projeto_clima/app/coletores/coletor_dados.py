from typing import List, Dict, Optional
from ..servicos.geocode import GeocodingClient
from ..servicos.openw import OpenWeatherClient
from ..servicos.dados_historicos import HistoricalDataLoader
from ..modelos.modelo_clima import Coordenadas, DadosTemperatura
import os
import pandas as pd

class DataCollector:
    """Coordenador principal - coleta dados de todas as fontes"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.geo = GeocodingClient()
        self.weather = OpenWeatherClient(api_key) if api_key else None
        self.historical = HistoricalDataLoader()
        self.ultima_coleta = []
        self.cidades_sul_fluminense = [
            "Resende", "Volta Redonda", "Barra Mansa", "Barra do Piraí",
            "Valença", "Vassouras", "Angra dos Reis", "Paraty", "Itatiaia",
            "Pinheiral", "Piraí", "Rio Claro", "Porto Real", "Quatis",
            "Rio das Flores"
        ]
    
    def coletar_coordenadas_regiao(self) -> List[Coordenadas]:
        """Coleta coordenadas de todas as cidades da região"""
        print("\n Coletando coordenadas...")
        coordenadas = []
        for cidade in self.cidades_sul_fluminense:
            coord = self.geo.buscar_coordenadas(cidade)
            if coord:
                coordenadas.append(coord)
        print(f" {len(coordenadas)} cidades encontradas")
        return coordenadas
    
    def coletar_temperaturas_atuais(self, coordenadas: List[Coordenadas]) -> List[DadosTemperatura]:
        """Coleta temperaturas atuais para as coordenadas"""
        if not self.weather:
            print(" Cliente OpenWeather não configurado")
            return []
        
        print("\n Coletando temperaturas atuais...")
        temperaturas = self.weather.buscar_temperaturas_regiao(coordenadas)
        self.ultima_coleta = temperaturas
        return temperaturas
    
    def coletar_dados_completos(self) -> Dict:
        """Coleta todos os dados disponíveis"""
        print("="*60)
        print("INICIANDO COLETA COMPLETA - SUL FLUMINENSE")
        print("="*60)
        
        # 1. Coordenadas
        coords = self.coletar_coordenadas_regiao()
        
        # 2. Temperaturas atuais
        temps = self.coletar_temperaturas_atuais(coords)
        
        # 3. Resumo
        print("\n" + "="*60)
        print("RESUMO DA COLETA")
        print("="*60)
        print(f" Cidades encontradas: {len(coords)}")
        print(f"  Temperaturas coletadas: {len(temps)}")
        
        if temps:
            temp_media = sum(t.temperatura_c for t in temps) / len(temps)
            print(f"Temperatura média: {temp_media:.1f}°C")
        
        return {
            'coordenadas': [c.dict() for c in coords],
            'temperaturas': [t.dict() for t in temps],
            'total_cidades': len(coords),
            'total_temps': len(temps)
        }
    
    def buscar_historico(self, anos: List[int]) -> pd.DataFrame:
        """Busca dados históricos para treinamento"""
        print("\n Buscando dados históricos...")
        return self.historical.carregar_dados_sul_fluminense(anos)