import logging
import concurrent.futures
from langchain_openai import ChatOpenAI

# --- Configuração de logging ---
logger = logging.getLogger(__name__)

# --- Constantes e Configurações ---
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.2
MAX_RETRIES = 2
MAX_TOKENS = 200
TIMEOUT_SECONDS = 10  # Defina o tempo limite em segundos


class LLMService:
    def __init__(self, api_key):
        self.llm = None
        try:
            # Usar ThreadPoolExecutor para aplicar timeout à inicialização do modelo
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.initialize_llm, api_key)
                # Timeout de 10 segundos
                self.llm = future.result(timeout=TIMEOUT_SECONDS)
            logger.info("Modelo LLM inicializado com sucesso.")
        except concurrent.futures.TimeoutError:
            logger.error(f"Tempo limite excedido ao inicializar o modelo LLM.")
        except Exception as e:
            logger.error(f"Erro ao inicializar o modelo LLM: {e}")

    def initialize_llm(self, api_key):
        return ChatOpenAI(api_key=api_key, model=MODEL_NAME, temperature=TEMPERATURE,
                          verbose=True, max_retries=MAX_RETRIES, max_tokens=MAX_TOKENS)
