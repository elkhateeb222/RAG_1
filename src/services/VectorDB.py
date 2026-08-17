from settings import get_settings
from logging import getLogger
import chromadb
from models import DBManager


class VectorDB:
    def __init__(self):
        self.settings = get_settings()
        self.logger = getLogger(__name__)
        self.db_manager = DBManager()
        # Lazily initialized, shared across all methods
        self.chromadb_client = None
        self.collection = None

    async def _ensure_collection(self):
        """Create the client/collection once and reuse them afterwards."""
        if self.collection is None:
            self.chromadb_client = await chromadb.AsyncHttpClient(
                host="localhost", port=8000
            )
            self.collection = await self.chromadb_client.get_or_create_collection(
                self.settings.VECTORDB_COLLECTION_NAME
            )
        return self.collection

    async def index_into_collection(self, table_name: str):
        await self._ensure_collection()

        chunk_ids_data, chunk_content_data = self.db_manager.get_ids_and_chunks_content_cols(
            table_name=table_name
        )

        await self.collection.add(
            ids=chunk_ids_data,
            documents=chunk_content_data,
        )
        self.logger.info("vectors successfully added")

        count_collection = await self.collection.count()
        return count_collection

    async def retrieve_top_chunks(self, query: str):
        await self._ensure_collection()

        top_chunks = await self.collection.query(
            query_texts=[query],
            n_results=5,
        )
        return top_chunks["documents"][0]