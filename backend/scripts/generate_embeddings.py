"""
Generate embeddings for product catalog using CLIP
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from PIL import Image
import numpy as np
from tqdm import tqdm
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.clip_model import CLIPModel
from app.utils.faiss_index import FAISSIndex

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_embeddings():
    """
    Generate embeddings for all products in the catalog
    """
    # Initialize CLIP model
    clip_model = CLIPModel()
    
    # Load product catalog
    catalog_path = "/app/data/products.json"
    if not os.path.exists(catalog_path):
        logger.error(f"Product catalog not found at {catalog_path}")
        return
    
    with open(catalog_path, 'r') as f:
        products = json.load(f)
    
    logger.info(f"Processing {len(products)} products")
    
    # Initialize FAISS index
    embedding_dim = clip_model.get_embedding_dim()
    faiss_index = FAISSIndex(embedding_dim=embedding_dim)
    
    # Process products in batches
    batch_size = 32
    embeddings_list = []
    metadata_list = []
    
    for i in tqdm(range(0, len(products), batch_size), desc="Processing batches"):
        batch = products[i:i + batch_size]
        
        # Prepare batch data
        images = []
        texts = []
        batch_metadata = []
        
        for product in batch:
            # Load image
            image_path = f"/app/data/images/{product['image']}"
            if os.path.exists(image_path):
                try:
                    image = Image.open(image_path).convert('RGB')
                    images.append(image)
                    texts.append(product['title'])
                    batch_metadata.append({
                        'product_id': product['id'],
                        'title': product['title'],
                        'image_url': f"/images/{product['image']}",
                        'category': product.get('category', ''),
                        'price': product.get('price', 0.0)
                    })
                except Exception as e:
                    logger.warning(f"Failed to load image {image_path}: {e}")
                    continue
            else:
                logger.warning(f"Image not found: {image_path}")
                continue
        
        if not images:
            continue
        
        # Generate embeddings
        try:
            image_embeddings = await clip_model.encode_batch_images(images)
            text_embeddings = await clip_model.encode_batch_texts(texts)
            
            # Combine embeddings (weighted average)
            combined_embeddings = 0.7 * image_embeddings + 0.3 * text_embeddings
            
            # Normalize
            combined_embeddings = combined_embeddings / np.linalg.norm(
                combined_embeddings, axis=1, keepdims=True
            )
            
            embeddings_list.append(combined_embeddings)
            metadata_list.extend(batch_metadata)
            
        except Exception as e:
            logger.error(f"Failed to process batch {i}: {e}")
            continue
    
    if embeddings_list:
        # Combine all embeddings
        all_embeddings = np.vstack(embeddings_list)
        
        # Add to FAISS index
        faiss_index.add_batch_products(all_embeddings, metadata_list)
        
        # Save index
        faiss_index.save_index()
        
        logger.info(f"Generated embeddings for {len(metadata_list)} products")
        logger.info(f"Saved FAISS index with {faiss_index.get_total_products()} products")
    else:
        logger.error("No embeddings generated")

if __name__ == "__main__":
    asyncio.run(generate_embeddings())