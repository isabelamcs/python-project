# Pipeline de Cotações Cambiais com Python + LLM

Um pipeline completo de ETL (Extract, Transform, Load) para processamento de dados de câmbio com integração de LLM para geração de insights de negócio.

## Características

- **ETL Completo**: Arquitetura Medallion (Bronze → Silver → Gold)
- **Integração com APIs**: exchangerate-api.com para dados de câmbio
- **Análise com LLM**: ChatGPT (OpenAI) para insights automatizados
- **Logging Estruturado**: Logs contextualizados
- **Validação de Dados**: Checks em cada camada
- **Configuração Flexível**: YAML + variáveis de ambiente (.env)
- **Testes Automatizados**: Pytest

## Estrutura do Projeto

```
currency_exchange_pipeline/
├── config/
│   └── config.yaml           # Configuração principal
├── src/
│   ├── __init__.py
│   ├── config.py            # Gerenciamento de configuração
│   ├── logger.py            # Sistema de logging
│   ├── ingest.py            # Ingestão de dados (Bronze)
│   ├── transform.py         # Transformação (Silver)
│   ├── load.py              # Carregamento (Gold)
│   ├── llm_analyzer.py      # Análise com LLM
│   └── pipeline.py          # Orquestrador principal
├── tests/
│   ├── __init__.py
│   ├── test_config.py       # Testes de configuração
│   └── test_pipeline.py     # Testes do pipeline
├── data/                    # Diretórios de dados (criados automaticamente)
│   ├── bronze/              # Dados brutos (Bronze)
│   ├── silver/              # Dados processados (Silver)
│   ├── gold/                # Dados agregados (Gold)
├── logs/                    # Arquivos de log
├── .env.example             # Template de variáveis de ambiente
├── requirements.txt         # Dependências Python
├── main.py                  # Ponto de entrada
└── README.md               # Este arquivo
```

## Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/isabelamcs/python-project.git
cd python-project
```

Crie o arquivo `.env` a partir do template:
```bash
cp .env.example .env   # Linux / Mac
# Windows (PowerShell)
Copy-Item .env.example .env
```

### 2. Criar ambiente virtual
Linux / Mac:
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```
Windows (PowerShell):
```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Edite o arquivo `.env` e inclua:
```dotenv
EXCHANGE_RATE_API_KEY=sua_chave_exchangerate
OPENAI_API_KEY=sua_chave_openai
```

### 5. Obter chaves de API

#### Exchange Rate API
1. Acesse [exchangerate-api.com](https://exchangerate-api.com/)
2. Registre-se gratuitamente
3. Copie sua chave de API

#### OpenAI API
1. Acesse [platform.openai.com](https://platform.openai.com/)
2. Crie uma conta 
3. Gere uma chave de API

## Uso

### Verificar Status
```bash
python3 main.py --status
```

### Pipeline Diário
```bash
# Para hoje
python3 main.py --daily

# Para data específica
python3 main.py --daily --date 2024-01-15

# Com saída detalhada
python3 main.py --daily --verbose
```

### Pipeline Histórico
```bash
# Período específico
python3 main.py --historical --start 2024-01-01 --end 2024-01-07

# Com saída detalhada
python3 main.py --historical --start 2024-01-01 --end 2024-01-07 --verbose
```

### Configuração Personalizada
```bash
# Usar arquivo de configuração personalizado
python3 main.py --daily --config /path/to/custom/config.yaml
```

## Testes

### Executar todos os testes
```bash
pytest tests/
```

### Executar testes específicos
```bash
# Testes de configuração
pytest tests/test_config.py

# Testes do pipeline
pytest tests/test_pipeline.py

# Com cobertura
pytest tests/ --cov=src
```

## Arquitetura dos Dados

### Camada Bronze (Raw)
- **Localização**: `data/bronze/`
- **Formato**: Parquet (ou JSON intermediário)
- **Conteúdo**: Dados brutos da API sem transformação
- **Particionamento**: Estratégia simples por data no nome do arquivo

### Camada Silver (Processed)
- **Localização**: `data/silver/`
- **Formato**: Parquet
- **Conteúdo**: Dados limpos e validados
- **Transformações**:
  - Normalização de colunas
  - Tipagem/validação
  - Remoção de duplicatas
  - Enriquecimentos

### Camada Gold (Aggregated)
- **Localização**: `data/gold/`
- **Formato**: Parquet
- **Conteúdo**: Dados agregados / métricas
- **Agregações**:
  - Estatísticas por moeda
  - Variações percentuais
  - Rankings de volatilidade

## Análise com LLM

O pipeline integra ChatGPT para gerar insights automáticos:

- **Análise de Tendências**: Identificação de padrões nos dados
- **Insights de Negócio**: Recomendações baseadas nas variações
- **Alertas**: Detecção de movimentos significativos
- **Relatórios**: Sumários executivos automáticos

### Exemplo de Saída LLM
```json
{
  "summary": "Análise das cotações de 2024-01-15",
  "key_insights": [
    "USD/BRL apresentou alta de 2.3%",
    "EUR/USD manteve estabilidade"
  ],
  "recommendations": [
    "Monitorar volatilidade do Real",
    "Oportunidade de hedge cambial"
  ],
  "risk_alerts": []
}
```

## Monitoramento

### Logs
- **Localização**: `logs/`
- **Formato**: Texto estruturado (pode ser adaptado para JSON)
- **Níveis**: DEBUG, INFO, WARNING, ERROR
- **Rotação**: (implementar se necessário via handlers)

### Métricas
- Tempo de execução por etapa
- Taxa de sucesso/falha
- Volume de dados processados
- Latência das APIs

## Configuração Avançada

### Arquivo config.yaml (trecho atual)
```yaml
api:
  base_url: "https://v6.exchangerate-api.com/v6"
  timeout: 30
  
currencies:
  base: "USD"
  targets: ["BRL", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "MXN", "ARS"]

data_paths:
  bronze: "data/bronze"
  silver: "data/silver"
  gold: "data/gold"
  logs: "logs"

llm:
  model: "gpt-3.5-turbo"
  max_tokens: 1000
  temperature: 0.3

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Solução de Problemas

### Erro: "API key não encontrada"
```bash
# Verificar se as variáveis estão definidas
echo $EXCHANGE_RATE_API_KEY  # Linux / Mac
echo $OPENAI_API_KEY
# Windows (PowerShell)
echo $Env:EXCHANGE_RATE_API_KEY
echo $Env:OPENAI_API_KEY

# Recarregar o arquivo .env
source .env  # Linux/Mac
# ou reiniciar o terminal no Windows
```

### Erro: "Módulo não encontrado"
```bash
# Verificar se está no ambiente virtual
which python  # Linux / Mac
Get-Command python  # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro de permissão nos diretórios
```bash
# Dar permissão de escrita
chmod -R 755 data/   # Linux / Mac (Windows normalmente não precisa)
```

## Desenvolvimento

### Adicionar nova moeda
1. Editar `config/config.yaml`:
```yaml
exchange_rate_api:
  currencies: ["USD", "EUR", "GBP", "JPY", "CAD"]  # Adicionar CAD
```

### Personalizar análise LLM
1. Ajustar template de prompt em `src/llm_analyzer.py`
2. Alterar parâmetros (model, temperature, max_tokens) em `config/config.yaml`
3. Reexecutar pipeline

## Arquivo .env.example (sugestão)
```dotenv
# Chaves de API
EXCHANGE_RATE_API_KEY=coloque_sua_chave
OPENAI_API_KEY=coloque_sua_chave

# (Opcional) Config DB
DB_HOST=localhost
DB_PORT=5432
DB_NAME=currency_exchange
DB_USER=postgres
DB_PASSWORD=
```

## Roadmap / Próximos Passos
- Adicionar persistência em banco (opcional)
- Implementar rotação de logs
- Adicionar camada de métricas Prometheus
- Containerização (Docker)
- GitHub Actions (CI: lint + testes)

## Licença
Definir licença (ex: MIT) e adicionar arquivo `LICENSE`.






