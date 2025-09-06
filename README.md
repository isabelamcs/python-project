# Pipeline de Cotações Cambiais com Python + LLM

Um pipeline completo de ETL (Extract, Transform, Load) para processamento de dados de câmbio com integração de LLM para análise de insights de negócio.

## Características

- **ETL Completo**: Pipeline seguindo arquitetura medallion (Bronze → Silver → Gold)
- **Integração com APIs**: exchangerate-api.com para dados de câmbio
- **Análise com LLM**: ChatGPT para insights de negócio automatizados
- **Logging Estruturado**: Sistema completo de logs com structlog
- **Validação de Dados**: Verificações de qualidade em todas as etapas
- **Configuração Flexível**: YAML + variáveis de ambiente
- **Testes Automatizados**: Suite completa de testes com pytest

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
│   ├── raw/                 # Dados brutos (Bronze)
│   ├── silver/              # Dados processados (Silver)
│   ├── gold/                # Dados agregados (Gold)
│   └── logs/                # Arquivos de log
├── .env.example             # Template de variáveis de ambiente
├── requirements.txt         # Dependências Python
├── main.py                  # Ponto de entrada
└── README.md               # Este arquivo
```

## Instalação

### 1. Clonar o repositório
```bash
git clone <repository-url>
cd currency_exchange_pipeline
```

### 2. Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
```
# Editar .env com suas chaves de API
EXCHANGE_RATE_API_KEY=sua_chave_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
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
python main.py --status
```

### Pipeline Diário
```bash
# Para hoje
python main.py --daily

# Para data específica
python main.py --daily --date 2024-01-15

# Com saída detalhada
python main.py --daily --verbose
```

### Pipeline Histórico
```bash
# Período específico
python main.py --historical --start 2024-01-01 --end 2024-01-07

# Com saída detalhada
python main.py --historical --start 2024-01-01 --end 2024-01-07 --verbose
```

### Configuração Personalizada
```bash
# Usar arquivo de configuração personalizado
python main.py --daily --config /path/to/custom/config.yaml
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
- **Localização**: `data/raw/`
- **Formato**: Parquet
- **Conteúdo**: Dados brutos da API sem transformação
- **Particionamento**: Por data (`YYYY/MM/DD`)

### Camada Silver (Processed)
- **Localização**: `data/silver/`
- **Formato**: Parquet
- **Conteúdo**: Dados limpos e validados
- **Transformações**: 
  - Normalização de nomes de colunas
  - Validação de tipos de dados
  - Remoção de duplicatas
  - Cálculo de métricas derivadas

### Camada Gold (Aggregated)
- **Localização**: `data/gold/`
- **Formato**: Parquet
- **Conteúdo**: Dados agregados para análise
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
- **Localização**: `data/logs/`
- **Formato**: JSON estruturado
- **Níveis**: DEBUG, INFO, WARNING, ERROR
- **Rotação**: Diária com retenção de 30 dias

### Métricas
- Tempo de execução por etapa
- Taxa de sucesso/falha
- Volume de dados processados
- Latência das APIs

## Configuração Avançada

### Arquivo config.yaml
```yaml
# Personalizar configurações
exchange_rate_api:
  base_url: "https://v6.exchangerate-api.com/v6"
  timeout: 30
  currencies: ["USD", "EUR", "GBP", "JPY"]

llm:
  model: "gpt-3.5-turbo"
  temperature: 0.1
  max_tokens: 1000

data_paths:
  raw: "./data/raw"
  silver: "./data/silver"
  gold: "./data/gold"
  logs: "./data/logs"

logging:
  level: "INFO"
  format: "json"
```

## Solução de Problemas

### Erro: "API key não encontrada"
```bash
# Verificar se as variáveis estão definidas
echo $EXCHANGE_RATE_API_KEY
echo $OPENAI_API_KEY

# Recarregar o arquivo .env
source .env  # Linux/Mac
# ou reiniciar o terminal no Windows
```

### Erro: "Módulo não encontrado"
```bash
# Verificar se está no ambiente virtual
which python  # deve apontar para venv

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro de permissão nos diretórios
```bash
# Dar permissão de escrita
chmod -R 755 data/
```

## Desenvolvimento

### Adicionar nova moeda
1. Editar `config/config.yaml`:
```yaml
exchange_rate_api:
  currencies: ["USD", "EUR", "GBP", "JPY", "CAD"]  # Adicionar CAD
```

### Personalizar análise LLM
1. Editar prompts em `src/llm_analyzer.py`
2. Ajustar parâmetros do modelo no config






