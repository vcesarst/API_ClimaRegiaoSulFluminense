from .cliente_api import ClienteAPI
from ..modelos.modelo_clima import DadosTemperatura, Coordenadas
from typing import List, Dict, Optional
import time

class OpenWeatherClient(ClienteAPI):
    """Cliente para OpenWeatherMap - Focado no Sul Fluminense"""
    
    def __init__(self, api_key: str):
        super().__init__(
            nome="openweather",
            url_base="https://api.openweathermap.org/data/2.5",
            timeout=10
        )
        self.api_key = api_key
    
    def buscar_temperatura(self, coords: Coordenadas) -> Optional[DadosTemperatura]:
        """
        Busca temperatura atual para uma cidade do Sul Fluminense
        """
        params = {
            'lat': coords.lat,
            'lon': coords.lon,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'pt_br'
        }
        
        # Usa o método da classe base
        dados = self._fazer_requisicao('weather', params)
        
        if dados:
            temperatura = DadosTemperatura(
                nome=coords.nome,
                lat=coords.lat,
                lon=coords.lon,
                temperatura_c=dados['main']['temp'],
                umidade=dados['main']['humidity'],
                fonte="OpenWeatherMap"
            )
            return temperatura
        return None
    
    def buscar_temperaturas_regiao(self, cidades: List[Coordenadas]) -> List[DadosTemperatura]:
        """
        Busca temperaturas para múltiplas cidades da região
        """
        resultados = []
        for cidade in cidades:
            temp = self.buscar_temperatura(cidade)
            if temp:
                resultados.append(temp)
                # Mostra resultado
                print(f"    {cidade.nome}: {temp.temperatura_c}°C, {temp.umidade}%")
            time.sleep(1)  # Rate limiting
        return resultados
    
    def buscar_dados(self, coordenadas: List[Coordenadas]) -> List[Dict]:
        """Implementação do método abstrato"""
        temps = self.buscar_temperaturas_regiao(coordenadas)
        return [t.dict() for t in temps]