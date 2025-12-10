"""
Product Deduplication
Removes duplicate products using perceptual hashing and similarity scores.
"""

import imagehash
from PIL import Image
import numpy as np
from typing import List, Dict, Any, Set, Optional
import logging

logger = logging.getLogger(__name__)

class ProductDeduplicator:
    """
    Deduplicate products based on:
    1. Perceptual image hashing
    2. Title similarity
    3. CLIP embedding similarity
    """
    
    def __init__(
        self, 
        image_hash_threshold: int = 5,
        embedding_similarity_threshold: float = 0.98,
        title_similarity_threshold: float = 0.9
    ):
        self.image_hash_threshold = image_hash_threshold
        self.embedding_similarity_threshold = embedding_similarity_threshold
        self.title_similarity_threshold = title_similarity_threshold
    
    def compute_image_hash(self, image: Image.Image) -> str:
        """Compute perceptual hash of image"""
        try:
            # Use average hash (fast and effective)
            hash_value = imagehash.average_hash(image)
            return str(hash_value)
        except Exception as e:
            logger.error(f"Error computing image hash: {e}")
            return ""
    
    def are_images_similar(self, hash1: str, hash2: str) -> bool:
        """Check if two image hashes are similar"""
        try:
            h1 = imagehash.hex_to_hash(hash1)
            h2 = imagehash.hex_to_hash(hash2)
            distance = h1 - h2
            return distance <= self.image_hash_threshold
        except Exception as e:
            logger.error(f"Error comparing hashes: {e}")
            return False
    
    def compute_title_similarity(self, title1: str, title2: str) -> float:
        """Compute simple title similarity using Jaccard index"""
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def deduplicate_by_image_hash(
        self, 
        products: List[Dict[str, Any]], 
        image_hashes: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate products based on image perceptual hashing.
        Keeps the product with highest similarity score.
        """
        if len(products) != len(image_hashes):
            logger.warning("Mismatch between products and hashes count")
            return products
        
        seen_hashes: Set[str] = set()
        hash_to_product: Dict[str, Dict[str, Any]] = {}
        unique_products = []
        duplicates_removed = 0
        
        for product, img_hash in zip(products, image_hashes):
            if not img_hash:
                unique_products.append(product)
                continue
            
            # Check if similar hash exists
            is_duplicate = False
            for existing_hash in seen_hashes:
                if self.are_images_similar(img_hash, existing_hash):
                    # Duplicate found - keep the one with higher score
                    existing_product = hash_to_product[existing_hash]
                    existing_score = existing_product.get('score', 0)
                    current_score = product.get('score', 0)
                    
                    if current_score > existing_score:
                        # Replace with better product
                        unique_products.remove(existing_product)
                        unique_products.append(product)
                        hash_to_product[existing_hash] = product
                    
                    is_duplicate = True
                    duplicates_removed += 1
                    break
            
            if not is_duplicate:
                seen_hashes.add(img_hash)
                hash_to_product[img_hash] = product
                unique_products.append(product)
        
        logger.info(f"Removed {duplicates_removed} duplicate products by image hash")
        return unique_products
    
    def deduplicate_by_embedding_similarity(
        self, 
        products: List[Dict[str, Any]], 
        embeddings: List[np.ndarray]
    ) -> List[Dict[str, Any]]:
        """
        Remove products with very high embedding similarity (>0.98).
        Likely exact duplicates or near-duplicates.
        """
        if len(products) != len(embeddings):
            logger.warning("Mismatch between products and embeddings count")
            return products
        
        unique_products = []
        unique_embeddings = []
        duplicates_removed = 0
        
        for product, embedding in zip(products, embeddings):
            is_duplicate = False
            
            # Compare with existing unique embeddings
            for unique_emb in unique_embeddings:
                similarity = self.cosine_similarity(embedding, unique_emb)
                
                if similarity > self.embedding_similarity_threshold:
                    is_duplicate = True
                    duplicates_removed += 1
                    break
            
            if not is_duplicate:
                unique_products.append(product)
                unique_embeddings.append(embedding)
        
        logger.info(f"Removed {duplicates_removed} duplicate products by embedding similarity")
        return unique_products
    
    def deduplicate_combined(
        self,
        products: List[Dict[str, Any]],
        image_hashes: List[str],
        embeddings: Optional[List[np.ndarray]] = None
    ) -> List[Dict[str, Any]]:
        """
        Apply both deduplication methods.
        First by image hash (faster), then by embedding similarity.
        """
        logger.info(f"Starting deduplication for {len(products)} products")
        
        # Step 1: Image hash deduplication
        products = self.deduplicate_by_image_hash(products, image_hashes)
        
        # Step 2: Embedding similarity deduplication (if available)
        if embeddings and len(embeddings) == len(products):
            products = self.deduplicate_by_embedding_similarity(products, embeddings)
        
        logger.info(f"Final unique products: {len(products)}")
        return products


# Global deduplicator instance
_global_deduplicator = None

def get_deduplicator() -> ProductDeduplicator:
    """Get or create global deduplicator instance"""
    global _global_deduplicator
    if _global_deduplicator is None:
        _global_deduplicator = ProductDeduplicator()
    return _global_deduplicator
