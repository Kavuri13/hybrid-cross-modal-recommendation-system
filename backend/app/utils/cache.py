"""
Ephemeral Caching Layer
Provides temporary caching for product images and embeddings.
Cache expires after 24 hours. No persistent database storage.
"""

import os
import hashlib
import time
import logging
from typing import Optional, Any
from diskcache import Cache
import numpy as np
from PIL import Image
import io

logger = logging.getLogger(__name__)

class EphemeralCache:
    """
    Temporary cache with 24-hour expiration.
    Used for performance optimization without persistent storage.
    """
    
    def __init__(self, cache_dir: str = "/tmp/clip_cache", size_limit_gb: int = 5):
        self.cache_dir = cache_dir
        self.size_limit = size_limit_gb * 1024 * 1024 * 1024  # Convert to bytes
        
        # Initialize diskcache
        self.cache = Cache(
            directory=cache_dir,
            size_limit=self.size_limit,
            eviction_policy='least-recently-used'
        )
        
        logger.info(f"Ephemeral cache initialized at {cache_dir} with {size_limit_gb}GB limit")
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key from identifier"""
        hash_obj = hashlib.md5(identifier.encode())
        return f"{prefix}:{hash_obj.hexdigest()}"
    
    def set_with_expiry(self, key: str, value: Any, expire_hours: int = 24) -> bool:
        """
        Store value with expiration time.
        Default: 24 hours
        """
        try:
            expire_seconds = expire_hours * 3600
            self.cache.set(key, value, expire=expire_seconds)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            return self.cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def cache_image(self, image_url: str, image: Image.Image, expire_hours: int = 24) -> bool:
        """Cache downloaded image"""
        key = self._generate_key("image", image_url)
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        
        return self.set_with_expiry(key, img_bytes, expire_hours)
    
    def get_cached_image(self, image_url: str) -> Optional[Image.Image]:
        """Retrieve cached image"""
        key = self._generate_key("image", image_url)
        img_bytes = self.get(key)
        
        if img_bytes:
            try:
                return Image.open(io.BytesIO(img_bytes))
            except Exception as e:
                logger.error(f"Error loading cached image: {e}")
                return None
        
        return None
    
    def cache_embedding(self, identifier: str, embedding: np.ndarray, expire_hours: int = 24) -> bool:
        """Cache CLIP embedding"""
        key = self._generate_key("embedding", identifier)
        
        # Store as bytes for efficiency
        embedding_bytes = embedding.tobytes()
        metadata = {
            'shape': embedding.shape,
            'dtype': str(embedding.dtype),
            'data': embedding_bytes
        }
        
        return self.set_with_expiry(key, metadata, expire_hours)
    
    def get_cached_embedding(self, identifier: str) -> Optional[np.ndarray]:
        """Retrieve cached embedding"""
        key = self._generate_key("embedding", identifier)
        metadata = self.get(key)
        
        if metadata:
            try:
                embedding = np.frombuffer(
                    metadata['data'],
                    dtype=metadata['dtype']
                ).reshape(metadata['shape'])
                return embedding
            except Exception as e:
                logger.error(f"Error loading cached embedding: {e}")
                return None
        
        return None
    
    def cache_search_results(
        self, 
        query_hash: str, 
        results: Any, 
        expire_hours: int = 1
    ) -> bool:
        """
        Cache search results for very short duration.
        Useful for pagination or repeated identical queries.
        """
        key = self._generate_key("search", query_hash)
        return self.set_with_expiry(key, results, expire_hours)
    
    def get_cached_search_results(self, query_hash: str) -> Optional[Any]:
        """Retrieve cached search results"""
        key = self._generate_key("search", query_hash)
        return self.get(key)
    
    def clear_expired(self):
        """Clear all expired entries"""
        try:
            # diskcache handles expiration automatically
            # This method can be used for manual cleanup
            self.cache.expire()
            logger.info("Cleared expired cache entries")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        try:
            return {
                'size_bytes': self.cache.volume(),
                'size_mb': round(self.cache.volume() / (1024 * 1024), 2),
                'count': len(self.cache),
                'directory': self.cache_dir
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}
    
    def clear_all(self):
        """Clear entire cache - use with caution"""
        try:
            self.cache.clear()
            logger.info("Cleared entire cache")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")


# Global cache instance
_global_cache = None

def get_cache() -> EphemeralCache:
    """Get or create global cache instance"""
    global _global_cache
    if _global_cache is None:
        cache_dir = os.environ.get("CLIP_CACHE_DIR", "/tmp/clip_cache")
        _global_cache = EphemeralCache(cache_dir=cache_dir)
    return _global_cache
