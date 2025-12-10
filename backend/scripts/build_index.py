"""
Build and optimize FAISS index
"""
import os
import sys
import logging
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.faiss_index import FAISSIndex

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_index():
    """
    Build and optimize FAISS index
    """
    # Load existing index
    faiss_index = FAISSIndex()
    
    total_products = faiss_index.get_total_products()
    if total_products == 0:
        logger.error("No products found in index. Run generate_embeddings.py first.")
        return
    
    logger.info(f"Optimizing index with {total_products} products")
    
    # For HNSW, we can set search parameters
    if hasattr(faiss_index.index, 'hnsw'):
        faiss_index.index.hnsw.efSearch = 100
        logger.info("Set HNSW efSearch to 100")
    
    # Save optimized index
    faiss_index.save_index()
    
    # Print statistics
    stats = faiss_index.get_statistics()
    logger.info("Index statistics:")
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")
    
    logger.info("Index optimization complete")

if __name__ == "__main__":
    build_index()