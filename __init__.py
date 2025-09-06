"""
Pipeline de Cotações Cambiais com Python + LLM

Um pipeline completo de ETL para processamento de dados de câmbio
com integração de LLM para análise de insights de negócio.
"""

__version__ = "1.0.0"
__author__ = "Currency Exchange Pipeline Team"
__email__ = "pipeline@example.com"

from .src.pipeline import CurrencyExchangePipeline
from .src.config import Config
from .src.logger import setup_logging, PipelineLogger

__all__ = [
    "CurrencyExchangePipeline",
    "Config", 
    "setup_logging",
    "PipelineLogger"
]