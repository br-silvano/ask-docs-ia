import logging
import os
from langchain_community.document_loaders import TextLoader
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# --- Configuração de logging ---
logger = logging.getLogger(__name__)

# --- Constantes e Configurações ---
TIMEOUT_SECONDS = 10  # Defina o tempo limite em segundos


class DocumentService:
    @staticmethod
    def load_documents(file_path):
        # Verificar se o arquivo existe antes de tentar carregar
        if not os.path.exists(file_path):
            logger.error(f"O arquivo {file_path} não existe.")
            return []

        def execute_load():
            try:
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
                logger.info(
                    f"{len(documents)} documentos carregados com sucesso de {file_path}.")
                return documents
            except Exception as e:
                logger.error(f"Erro ao carregar documentos: {e}")
                return []

        # Usar ThreadPoolExecutor para aplicar um timeout no carregamento
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(execute_load)
            try:
                # Aguarda o resultado com o tempo limite definido
                documents = future.result(timeout=TIMEOUT_SECONDS)
                return documents
            except FuturesTimeoutError:
                logger.error(
                    f"Tempo limite de {TIMEOUT_SECONDS} segundos excedido ao carregar o arquivo {file_path}.")
                return []
