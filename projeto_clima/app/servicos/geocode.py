from .cliente_api import ClienteAPI
from ..modelos.modelo_clima import Coordenadas
from typing import List, Dict, Optional
import time

class GeocodingClient(ClienteAPI):
    """Cliente para OpenStreetMap/Nominatim - Focado no Sul Fluminense"""
    
    def __init__(self, user_agent: str = "SulFluminenseApp/1.0"):
        super().__init__(nome ="geocode",url_base="https://nominatim.openstreetmap.org",timeout=10)
        self._sessao.headers.update({"User-Agent": user_agent})
        self.cidades_cache = {}  # Cache para não repetir consultas
    
    def buscar_coordenadas(self, cidade: str) -> Optional[Coordenadas]:
        """
        Busca coordenadas de uma cidade do Sul Fluminense
        """
        # Verifica cache primeiro
        if cidade in self.cidades_cache:
            print(f"📦 Cache: {cidade} encontrado")
            return self.cidades_cache[cidade]
        
        print(f"🔍 Buscando coordenadas de: {cidade}")
        
        params = {
            'q': f"{cidade}, Rio de Janeiro, Brasil",  # Especifica o estado
            'format': 'json',
            'limit': 1,
            'countrycodes': 'br'  # Restringe ao Brasil
        }
        
        dados = self._fazer_requisicao('search', params)
        
        if dados:
            coords = Coordenadas(
                nome=cidade,
                lat=float(dados[0]['lat']),
                lon=float(dados[0]['lon']),
                fonte="OpenStreetMap"
            )
            # Salva no cache
            self.cidades_cache[cidade] = coords
            return coords
        
        print(f"Cidade não encontrada: {cidade}")
        return None
    
    def buscar_todas_cidades_sul_fluminense(self) -> List[Coordenadas]:
        """
        Busca coordenadas de todas as cidades do Sul Fluminense
        """
        cidades = [
            "Resende", "Volta Redonda", "Barra Mansa", 
            "Barra do Piraí", "Valença", "Vassouras",
            "Angra dos Reis", "Paraty", "Itatiaia",
            "Pinheiral", "Piraí", "Rio Claro",
            "Porto Real", "Quatis", "Rio das Flores"
        ]
        
        resultados = []
        for cidade in cidades:
            coords = self.buscar_coordenadas(cidade)
            if coords:
                resultados.append(coords)
            time.sleep(1)  # Respeita rate limiting
        
        print(f"Encontradas {len(resultados)} cidades da região")
        return resultados
    
    def buscar_dados(self, cidades: List[str]) -> List[Dict]:
        """Implementação do método abstrato"""
        resultados = []
        for cidade in cidades:
            coords = self.buscar_coordenadas(cidade)
            if coords:
                resultados.append(coords.dict())
        return resultados