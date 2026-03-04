from abc import ABC, abstractmethod
import requests
import time
from typing import Dict, List, Optional

class ClienteAPI(ABC):
    def __init__(self, nome:str, url_base:str, timeout:int = 10):
        self.nome = nome
        self.url_base = url_base
        self._timeout = timeout
        self._sessao = requests.Session()
        self._ultima_requisicao = 0

    def _fazer_requisicao(self, endpoint:str, params:Optional[Dict] = None) -> Dict:
        #Rate limiting simples
        agora = time.time()
        if agora - self._ultima_requisicao < 1:
            time.sleep(1 - (agora - self._ultima_requisicao))

        url = f"{self.url_base}/{endpoint.lstrip('/')}"

        try:
            resposta = self._sessao.get(url, params=params, timeout=self._timeout)
            resposta.raise_for_status()
            self._ultima_requisicao = time.time()
            return resposta.json()
        except requests.RequestException as e:
            print(f"Erro na requisição para {url}: {e}")
            return {}
        
    @abstractmethod
    def buscar_dados(self, coordenadas:Dict) -> Dict:
        pass
