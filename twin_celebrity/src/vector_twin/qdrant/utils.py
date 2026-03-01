import logging

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.models import Distance, VectorParams

from vector_twin.settings import settings

logger = logging.getLogger(__name__)


def create_collection(
    qdrant_client: QdrantClient,
    collection_name: str = settings.QDRANT_COLLECTION_NAME,
    vector_dimensions: int = settings.QDRANT_VECTOR_DIMENSIONS
):
    if not qdrant_client.collection_exists(collection_name):
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_dimensions,
                distance=Distance.COSINE
            )
        )


def insert_image_embedding(
    qdrant_client: QdrantClient,
    img_embedding: list[float],
    img_id: str,
    img_label: str,
    collection_name: str = settings.QDRANT_COLLECTION_NAME
):
    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=img_id,
                    vector=img_embedding,
                    payload={"label": img_label}
                )
            ]
        )
    except Exception as e:
        logger.error(f"Error inserting image embedding: {e}")


def get_top_k_similar_images(
    qdrant_client: QdrantClient,
    query_embedding: list[float],
    collection_name: str = settings.QDRANT_COLLECTION_NAME,
    k: int = 5
):
    return qdrant_client.query_points(
        collection_name=collection_name,
        query=query_embedding,
        limit=k
    ).points