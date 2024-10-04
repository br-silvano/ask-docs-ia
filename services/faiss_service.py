import logging
import concurrent.futures
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# --- Configuração de logging ---
logger = logging.getLogger(__name__)

# --- Constantes e Configurações ---
CHUNK_SIZE = 712
CHUNK_OVERLAP = 50
TIMEOUT_SECONDS = 10  # Defina o tempo limite em segundos


class FAISSService:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.faiss_index = None

    def create_index(self, documents):
        if not documents:
            logger.warning("Nenhum documento foi carregado para o FAISS.")
            return

        text_splitter = CharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        split_docs = text_splitter.split_documents(documents)

        try:
            # Usar ThreadPoolExecutor para aplicar timeout à criação do índice
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    FAISS.from_documents, split_docs, self.embeddings)
                self.faiss_index = future.result(timeout=TIMEOUT_SECONDS)
            logger.info("Índice FAISS criado com sucesso.")
        except concurrent.futures.TimeoutError:
            logger.error("Tempo limite excedido ao criar o índice FAISS.")
        except Exception as e:
            logger.error(f"Erro ao criar o índice FAISS: {e}")

    def search(self, query, k=1):
        if not self.faiss_index:
            logger.warning("O índice FAISS não foi criado.")
            return []

        try:
            # Usar ThreadPoolExecutor para aplicar timeout à pesquisa de similaridade
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    self.faiss_index.similarity_search, query, k)
                results = future.result(timeout=TIMEOUT_SECONDS)
            return results
        except concurrent.futures.TimeoutError:
            logger.error(
                "Tempo limite excedido durante a pesquisa por similaridade no FAISS.")
            return []
        except Exception as e:
            logger.error(f"Erro durante a pesquisa no FAISS: {e}")
            return []
