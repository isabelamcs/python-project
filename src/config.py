"""
Módulo de configuração do pipeline de cotações cambiais.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Classe para gerenciar configurações do projeto."""
    
    def __init__(self, config_path: str = None):
        """
        Inicializa a configuração.
        
        Args:
            config_path: Caminho para o arquivo de configuração YAML
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        
        self.config_path = Path(config_path)
        self._load_config()
        self._load_env_vars()
    
    def _load_config(self):
        """Carrega configurações do arquivo YAML."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Erro ao carregar configuração YAML: {e}")
    
    def _load_env_vars(self):
        """Carrega variáveis sensíveis do ambiente."""
        self.exchange_rate_api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Configurações de banco (opcionais)
        self.db_host = os.getenv('DB_HOST', self._config.get('database', {}).get('host'))
        self.db_port = int(os.getenv('DB_PORT', self._config.get('database', {}).get('port', 5432)))
        self.db_name = os.getenv('DB_NAME', self._config.get('database', {}).get('database'))
        self.db_user = os.getenv('DB_USER', self._config.get('database', {}).get('user'))
        self.db_password = os.getenv('DB_PASSWORD', self._config.get('database', {}).get('password'))
    
    @property
    def api_base_url(self) -> str:
        """URL base da API de câmbio."""
        return self._config['api']['base_url']
    
    @property
    def api_timeout(self) -> int:
        """Timeout para requisições da API."""
        return self._config['api']['timeout']
    
    @property
    def base_currency(self) -> str:
        """Moeda base para cotações."""
        return self._config['currencies']['base']
    
    @property
    def target_currencies(self) -> List[str]:
        """Lista de moedas alvo."""
        return self._config['currencies']['targets']
    
    @property
    def data_paths(self) -> Dict[str, str]:
        """Caminhos dos diretórios de dados."""
        return self._config['data_paths']
    
    @property
    def llm_config(self) -> Dict[str, Any]:
        """Configurações do LLM."""
        return self._config['llm']
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """Configurações de logging."""
        return self._config['logging']
    
    @property
    def database_enabled(self) -> bool:
        """Se o banco de dados está habilitado."""
        return self._config.get('database', {}).get('enabled', False)
    
    def validate_api_keys(self) -> bool:
        """
        Valida se as chaves de API necessárias estão configuradas.
        
        Returns:
            bool: True se todas as chaves necessárias estão presentes
        """
        missing_keys = []
        
        if not self.exchange_rate_api_key:
            missing_keys.append('EXCHANGE_RATE_API_KEY')
        
        if not self.openai_api_key:
            missing_keys.append('OPENAI_API_KEY')
        
        if missing_keys:
            raise ValueError(f"Chaves de API não configuradas: {', '.join(missing_keys)}")
        
        return True
    
    def get_full_api_url(self, endpoint: str) -> str:
        """
        Constrói URL completa da API.
        
        Args:
            endpoint: Endpoint da API
            
        Returns:
            str: URL completa
        """
        return f"{self.api_base_url}/{self.exchange_rate_api_key}/{endpoint}"
