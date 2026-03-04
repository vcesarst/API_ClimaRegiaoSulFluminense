from .base import DataPoint
from datetime import datetime
import pandas as pd

class Coordenadas(DataPoint):
    def __init__(self, nome: str, lat: float, lon: float,fonte: str):
        super().__init__(fonte)
        self.nome=nome
        self.lat=lat
        self.lon=lon

    def para_df(self) -> pd.DataFrame:
        return pd.DataFrame([{
            'nome': self.nome,
            'latitude': self.lat,
            'longitude': self.lon,
            'fonte': self.fonte,
            'timestamp': self.timestamp
        }])
    
    def dict(self) -> dict:
        base = super().dict()
        base.update({
            'nome': self.nome,
            'latitude': self.lat,
            'longitude': self.lon
        })
        return base
    
        def __str__(self) -> str:
            return f" {self.nome} | ({self.lat}, {self.lon}) | {self.fonte}"
    
class DadosTemperatura(Coordenadas):
    def __init__(self, nome: str, lat: float, lon: float, 
                 temperatura_c: float, umidade: float = None, 
                 fonte: str = "OpenWeather"):
        super().__init__(nome, lat, lon, fonte)
        self.temperatura_c = temperatura_c
        self.umidade = umidade
    
    def validar(self) -> bool:
        """Valida se temperatura é realista"""
        return -50 <= self.temperatura_c <= 50
    
    def para_dataframe(self) -> pd.DataFrame:
        df = super().para_dataframe()
        df['temperatura_c'] = self.temperatura_c
        df['umidade'] = self.umidade
        return df
    
    def dict(self) -> dict:
        base = super().dict()
        base.update({
            'temperatura_c': self.temperatura_c,
            'umidade': self.umidade
        })
        return base
    
    def __str__(self) -> str:
        return f" {self.nome} | ({self.lat}, {self.lon}) | Temperatura: {self.temperatura_c}°C | Umidade: {self.umidade}% | {self.fonte}"