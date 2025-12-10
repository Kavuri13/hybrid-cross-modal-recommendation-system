"""
Async Image Downloader
Downloads product images in parallel for CLIP encoding.
Uses caching to avoid redundant downloads.
"""

import asyncio
import aiohttp
import httpx
from typing import List, Dict, Optional, Tuple
from PIL import Image
import io
import logging
from app.utils.cache import get_cache

logger = logging.getLogger(__name__)

class ImageDownloader:
    """Async image downloader with caching"""
    
    def __init__(self, timeout: int = 10, max_concurrent: int = 20):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.cache = get_cache()
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def download_image(self, url: str) -> Optional[Image.Image]:
        """
        Download a single image with caching.
        Returns PIL Image or None if failed.
        """
        # Check cache first
        cached_image = self.cache.get_cached_image(url)
        if cached_image:
            logger.debug(f"Cache hit for image: {url}")
            return cached_image
        
        # Download image
        async with self.semaphore:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, follow_redirects=True)
                    response.raise_for_status()
                    
                    # Convert to PIL Image
                    image_data = response.content
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Convert to RGB if needed
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    # Cache the image
                    self.cache.cache_image(url, image)
                    
                    logger.debug(f"Downloaded image: {url}")
                    return image
                    
            except Exception as e:
                logger.error(f"Error downloading image {url}: {e}")
                return None
    
    async def download_images_batch(
        self, 
        urls: List[str]
    ) -> Dict[str, Optional[Image.Image]]:
        """
        Download multiple images in parallel.
        Returns dict mapping URL to Image (or None if failed).
        """
        logger.info(f"Downloading {len(urls)} images in parallel")
        
        tasks = [self.download_image(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Map results back to URLs
        image_map = {}
        for url, result in zip(urls, results):
            if isinstance(result, Image.Image):
                image_map[url] = result
            elif isinstance(result, Exception):
                logger.error(f"Exception downloading {url}: {result}")
                image_map[url] = None
            else:
                image_map[url] = None
        
        success_count = sum(1 for img in image_map.values() if img is not None)
        logger.info(f"Successfully downloaded {success_count}/{len(urls)} images")
        
        return image_map
    
    async def download_with_metadata(
        self, 
        product_data: List[Dict]
    ) -> List[Tuple[Dict, Optional[Image.Image]]]:
        """
        Download images and keep associated product metadata.
        Returns list of (product_dict, image) tuples.
        """
        urls = [p.get('image_url') for p in product_data if p.get('image_url')]
        
        # Download all images
        image_map = await self.download_images_batch(urls)
        
        # Combine with metadata
        results = []
        for product in product_data:
            url = product.get('image_url')
            image = image_map.get(url) if url else None
            results.append((product, image))
        
        return results


# Global downloader instance
_global_downloader = None

def get_image_downloader() -> ImageDownloader:
    """Get or create global image downloader instance"""
    global _global_downloader
    if _global_downloader is None:
        _global_downloader = ImageDownloader()
    return _global_downloader
