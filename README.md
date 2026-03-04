# 🌦️ API Climática - Sul Fluminense

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)
![Pandas](https://img.shields.io/badge/Pandas-2.1%2B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Sobre o Projeto

API completa para coleta, processamento e disponibilização de dados climáticos da **região Sul Fluminense do Rio de Janeiro**. O sistema integra três fontes de dados (OpenStreetMap, OpenWeatherMap e NASA POWER) e aplica princípios SOLID de programação orientada a objetos.

### 🎯 Motivação
Este projeto foi desenvolvido para demonstrar na prática:
- Arquitetura de software com POO e SOLID
- Integração com APIs externas reais
- Construção de APIs REST com FastAPI
- Pipeline ETL completo (Extract, Transform, Load)
- Preparação de dados para machine learning

## 🏗️ Arquitetura do Projeto
projeto_clima/
├── app/
│ ├── api/ # Endpoints da API
│ │ └── endpoint.py # Rotas da aplicação
│ ├── coletores/ # Orquestradores
│ │ └── coletor_dados.py
│ ├── core/ # Configurações
│ │ └── config.py
│ ├── modelos/ # Classes de domínio
│ │ ├── base.py # Classe abstrata DataPoint
│ │ └── modelo_clima.py # Coordenadas e DadosTemperatura
│ └── servicos/ # Clientes de API
│ ├── cliente_api.py # Classe base abstrata
│ ├── geocode.py # GeocodingClient (OSM)
│ ├── openw.py # OpenWeatherClient
│ └── dados_historicos.py # HistoricalDataLoader (NASA)
├── scripts/ # Scripts utilitários
│ └── baixar_dados_historicos.py
├── .env # Chaves de API (não versionado)
├── .env.example # Exemplo de configuração
├── .gitignore # Arquivos ignorados
├── requirements.txt # Dependências
├── main.py # Ponto de entrada da API
└── teste_regiao.py # Testes do sistema


## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.9+ | Linguagem base |
| **FastAPI** | 0.104+ | Framework web |
| **Pandas** | 2.1+ | Manipulação de dados |
| **Requests** | 2.31+ | Cliente HTTP |
| **Pydantic** | 2.4+ | Validação de dados |
| **python-dotenv** | 1.0+ | Configuração ambiental |
| **tqdm** | 4.66+ | Barras de progresso |

## 🌍 Fontes de Dados

### 1. **OpenStreetMap (Nominatim)** - Geocodificação
- Converte nomes de cidades em coordenadas
- Rate limiting: 1 requisição/segundo
- User-Agent configurável

### 2. **OpenWeatherMap** - Dados em Tempo Real
- Temperatura atual e umidade
- Requer chave de API gratuita
- Respostas em português

### 3. **NASA POWER** - Dados Históricos
- Temperaturas (média, máxima, mínima)
- Umidade relativa
- Precipitação
- Grade de 225 pontos na região
- Dados desde 1981

## 🎯 Funcionalidades Implementadas

### ✅ Clientes de API (Orientação a Objetos)
- [x] Classe abstrata `ClienteAPI` com rate limiting
- [x] `GeocodingClient` para geolocalização
- [x] `OpenWeatherClient` para clima atual
- [x] `HistoricalDataLoader` para dados históricos

### ✅ Modelos de Dados (Herança)
- [x] Classe abstrata `DataPoint`
- [x] `Coordenadas` (herda de DataPoint)
- [x] `DadosTemperatura` (herda de Coordenadas)

### ✅ Coleta e Processamento
- [x] Cache em memória para cidades
- [x] Rate limiting automático
- [x] Tratamento de erros e timeouts
- [x] Grade de 15×15 pontos (~11km de resolução)
- [x] Checkpoints por ano (CSV)
- [x] Barras de progresso com tqdm

### ✅ API REST
- [x] 5 endpoints funcionais
- [x] Documentação automática Swagger
- [x] CORS configurado
- [x] Respostas em JSON

## 📊 Dados Coletados

### Cidades do Sul Fluminense (15):

Resende, Volta Redonda, Barra Mansa, Barra do Piraí, Valença,
Vassouras, Angra dos Reis, Paraty, Itatiaia, Pinheiral,
Piraí, Rio Claro, Porto Real, Quatis, Rio das Flores


### Grade Geográfica:
- **225 pontos** (15 latitudes × 15 longitudes)
- **Resolução:** ~11km
- **Área:** 23.5°S a 22.0°S, 45.0°W a 43.5°W

### Volume de Dados (2023):
- **~82.000 registros** por ano
- **8 variáveis** por registro
- **Formato:** CSV (fácil para análise)

## 🧠 Princípios SOLID Aplicados

# S - Single Responsibility
class GeocodingClient:     # Apenas geolocalização
class OpenWeatherClient:    # Apenas clima atual
class HistoricalDataLoader: # Apenas dados históricos

# O - Open/Closed
class ClienteAPI(ABC):      # Aberta para extensão
    @abstractmethod
    def buscar_dados(self): ...

class NovaAPIClient(ClienteAPI):  # Nova API sem modificar as existentes
    pass

# L - Liskov Substitution
def processar(cliente: ClienteAPI):  # Funciona com qualquer cliente
    return cliente.buscar_dados()

# I - Interface Segregation
class DataPoint(ABC):       # Interface mínima
    @abstractmethod
    def para_dataframe(self): ...

# D - Dependency Inversion
class DataCollector:
    def __init__(self, clientes: List[ClienteAPI]):  # Depende da abstração
        self.clientes = clientes


🔧 Instalação e Uso

Checar o arquivo requirements.txt, onde se encontram todas as dependências

Passo a passo para ativação do ambiente e execução do programa:

# 1. Clone o repositório
git clone https://github.com/vcesarst/API_ClimaRegiaoSulFluminense.git
cd API_ClimaRegiaoSulFluminense

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure sua chave da API
cp .env.example .env
# Edite .env com sua chave do OpenWeatherMap
# OPENWEATHER_API_KEY=sua_chave_123

# 5. Teste o sistema
python teste_regiao.py

# 6. Inicie a API
python main.py


📡 Endpoints da API
Endpoint	Método	Descrição
/	GET	Informações da API
/cidades	GET	Lista cidades da região
/temperaturas	GET	Temperaturas atuais
/coleta-completa	GET	Todos os dados atuais
/historico?anos=2023	GET	Dados históricos
/docs	GET	Documentação Swagger

✨ Autor

Vinicius Cesar

⭐ Agradecimentos

Este projeto foi desenvolvido com auxílio de IA (DeepSeek) para orientação em arquitetura de software, boas práticas de programação e documentação.

Se este projeto te ajudou, considere dar uma estrela no GitHub! 🌟
