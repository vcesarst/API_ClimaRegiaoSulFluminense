import requests
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
import time
from tqdm import tqdm

class HistoricalDataLoader:
    """Carrega dados históricos da NASA POWER para o Sul Fluminense"""
    
    def __init__(self):
        self.dados = None
        # Grade para o Sul Fluminense (resolução mais fina por ser região pequena)
        self.grade_sul_fluminense = self._criar_grade_regiao()
    
    def _criar_grade_regiao(self, resolucao=0.1):
        """
        Cria uma grade de pontos para o Sul Fluminense
        Resolução 0.1 graus ≈ 11km
        """
        # Limites da região
        lat_min, lat_max = -23.5, -22.0
        lon_min, lon_max = -45.0, -43.5
        
        latitudes = []
        lat = lat_min
        while lat <= lat_max:
            latitudes.append(round(lat, 2))
            lat += resolucao
        
        longitudes = []
        lon = lon_min
        while lon <= lon_max:
            longitudes.append(round(lon, 2))
            lon += resolucao
        
        print(f" Grade gerada: {len(latitudes)} latitudes x {len(longitudes)} longitudes")
        print(f" Total de pontos: {len(latitudes) * len(longitudes)}")
        
        return latitudes, longitudes
    
    def carregar_nasa_power(self, 
                            lat: float, lon: float,
                            ano_inicio: int, ano_fim: int) -> Optional[pd.DataFrame]:
        """
        Carrega dados da NASA POWER para um ponto específico
        """
        url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        
        parametros = [
            "T2M",        # Temperatura a 2m
            "T2M_MAX",    # Temperatura máxima
            "T2M_MIN",    # Temperatura mínima
            "RH2M",       # Umidade relativa
            "PRECTOTCORR" # Precipitação
        ]
        
        params = {
            "parameters": ",".join(parametros),
            "community": "RE",
            "longitude": lon,
            "latitude": lat,
            "start": ano_inicio,
            "end": ano_fim,
            "format": "JSON"
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            dados = response.json()
            
            # Processar dados
            registros = []
            for data, temp in dados['properties']['parameter']['T2M'].items():
                if temp != -999.0:  # Ignora valores missing
                    registros.append({
                        'data': pd.to_datetime(data, format='%Y%m%d'),
                        'lat': lat,
                        'lon': lon,
                        'temperatura': temp,
                        'temperatura_max': dados['properties']['parameter']['T2M_MAX'][data],
                        'temperatura_min': dados['properties']['parameter']['T2M_MIN'][data],
                        'umidade': dados['properties']['parameter']['RH2M'][data],
                        'precipitacao': dados['properties']['parameter']['PRECTOTCORR'][data]
                    })
            
            return pd.DataFrame(registros)
            
        except Exception as e:
            print(f" Erro no ponto ({lat}, {lon}): {e}")
            return None
    
    def carregar_dados_sul_fluminense(self, 
                                      anos: List[int],
                                      salvar_parcial: bool = True) -> pd.DataFrame:
        """
        Carrega dados históricos para TODA a região Sul Fluminense
        
        Args:
            anos: Lista de anos para baixar (ex: [2020, 2021, 2022, 2023])
            salvar_parcial: Se True, salva checkpoint a cada ano
        """
        latitudes, longitudes = self.grade_sul_fluminense
        todos_dados = []
        
        print(f" Baixando dados do Sul Fluminense para {len(anos)} anos...")
        print(f" Resolução: {len(latitudes)}x{len(longitudes)} pontos")
        
        for ano in anos:
            print(f"\nProcessando ano {ano}...")
            dados_ano = []
            
            for lat in tqdm(latitudes, desc=f"Latitudes {ano}"):
                for lon in longitudes:
                    df_ponto = self.carregar_nasa_power(lat, lon, ano, ano)
                    if df_ponto is not None and not df_ponto.empty:
                        dados_ano.append(df_ponto)
                    
                    # Pequena pausa para não sobrecarregar a API
                    time.sleep(0.1)
            
            if dados_ano:
                df_ano = pd.concat(dados_ano, ignore_index=True)
                todos_dados.append(df_ano)
                
                if salvar_parcial:
                    # Salva checkpoint do ano
                    df_ano.to_csv(f"dados_sul_fluminense_{ano}.csv",index = False)
                    print(f"Checkpoint salvo: {len(df_ano)} registros em {ano}")
        
        if todos_dados:
            self.dados = pd.concat(todos_dados, ignore_index=True)
            print(f"\n Total final: {len(self.dados)} registros")
            print(f"   Período: {self.dados['data'].min()} a {self.dados['data'].max()}")
            return self.dados
        else:
            print(" Nenhum dado carregado")
            return pd.DataFrame()
    
    def preparar_sequencias(self, 
                           dados: pd.DataFrame,
                           lookback: int = 30,
                           horizonte: int = 7) -> Tuple[np.array, np.array]:
        """
        Transforma dados em sequências para treinamento
        """
        X, y = [], []
        
        # Agrupa por ponto geográfico
        for (lat, lon), grupo in dados.groupby(['lat', 'lon']):
            valores = grupo.sort_values('data')['temperatura'].values
            
            for i in range(len(valores) - lookback - horizonte):
                X.append(valores[i:i+lookback])
                y.append(valores[i+lookback:i+lookback+horizonte])
        
        print(f"Sequências geradas: {len(X)} amostras")
        return np.array(X), np.array(y)
    
    def resumo_regiao(self):
        """
        Gera um resumo estatístico da região
        """
        if self.dados is None or self.dados.empty:
            print(" Nenhum dado carregado")
            return
        
        print("\n" + "="*50)
        print(" RESUMO DO SUL FLUMINENSE")
        print("="*50)
        
        print(f"\n Área coberta:")
        print(f"   Latitudes: {self.dados['lat'].min():.2f} a {self.dados['lat'].max():.2f}")
        print(f"   Longitudes: {self.dados['lon'].min():.2f} a {self.dados['lon'].max():.2f}")
        print(f"   Pontos únicos: {self.dados.groupby(['lat', 'lon']).ngroups}")
        
        print(f"\n  Temperaturas:")
        print(f"   Média: {self.dados['temperatura'].mean():.1f}°C")
        print(f"    Máxima: {self.dados['temperatura'].max():.1f}°C")
        print(f"   Mínima: {self.dados['temperatura'].min():.1f}°C")
        
        print(f"\nUmidade média: {self.dados['umidade'].mean():.1f}%")
        print(f"Precipitação média: {self.dados['precipitacao'].mean():.1f} mm/dia")