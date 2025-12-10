import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Tuple, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class CrossAttentionReranker(nn.Module):
    """
    Cross-attention model for reranking search results
    Implements the optional reranking component from the workflow diagram
    """
    
    def __init__(
        self,
        embedding_dim: int = 512,
        hidden_dim: int = 256,
        num_heads: int = 8,
        num_layers: int = 2,
        dropout: float = 0.1
    ):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        
        # Multi-head cross-attention layers
        self.cross_attention_layers = nn.ModuleList([
            nn.MultiheadAttention(
                embed_dim=embedding_dim,
                num_heads=num_heads,
                dropout=dropout,
                batch_first=True
            ) for _ in range(num_layers)
        ])
        
        # Layer normalization
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(embedding_dim) for _ in range(num_layers)
        ])
        
        # Feed-forward networks
        self.ffn_layers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(embedding_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim, embedding_dim),
                nn.Dropout(dropout)
            ) for _ in range(num_layers)
        ])
        
        # Final scoring layer
        self.score_head = nn.Sequential(
            nn.Linear(embedding_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(
        self,
        query_embedding: torch.Tensor,
        candidate_embeddings: torch.Tensor
    ) -> torch.Tensor:
        """
        Forward pass for cross-attention reranking
        
        Args:
            query_embedding: Query embedding [1, embedding_dim]
            candidate_embeddings: Candidate embeddings [num_candidates, embedding_dim]
            
        Returns:
            Relevance scores [num_candidates, 1]
        """
        batch_size = candidate_embeddings.shape[0]
        
        # Expand query embedding to match candidates
        query_expanded = query_embedding.expand(batch_size, -1).unsqueeze(1)  # [batch, 1, dim]
        candidates_expanded = candidate_embeddings.unsqueeze(1)  # [batch, 1, dim]
        
        # Apply cross-attention layers
        query_attended = query_expanded
        candidate_attended = candidates_expanded
        
        for i, (attn_layer, norm_layer, ffn_layer) in enumerate(
            zip(self.cross_attention_layers, self.layer_norms, self.ffn_layers)
        ):
            # Cross-attention: query attends to candidates
            q_attn_out, _ = attn_layer(
                query_attended, candidate_attended, candidate_attended
            )
            query_attended = norm_layer(query_attended + self.dropout(q_attn_out))
            
            # Feed-forward
            q_ffn_out = ffn_layer(query_attended)
            query_attended = norm_layer(query_attended + q_ffn_out)
            
            # Cross-attention: candidates attend to query
            c_attn_out, _ = attn_layer(
                candidate_attended, query_attended, query_attended
            )
            candidate_attended = norm_layer(candidate_attended + self.dropout(c_attn_out))
            
            # Feed-forward
            c_ffn_out = ffn_layer(candidate_attended)
            candidate_attended = norm_layer(candidate_attended + c_ffn_out)
        
        # Flatten for scoring
        query_final = query_attended.squeeze(1)  # [batch, dim]
        candidate_final = candidate_attended.squeeze(1)  # [batch, dim]
        
        # Concatenate and score
        combined = torch.cat([query_final, candidate_final], dim=-1)  # [batch, 2*dim]
        scores = self.score_head(combined)  # [batch, 1]
        
        return scores
    
    def rerank_candidates(
        self,
        query_embedding: np.ndarray,
        candidate_embeddings: np.ndarray,
        candidate_metadata: List[Dict],
        top_k: int = None
    ) -> Tuple[List[Dict], np.ndarray]:
        """
        Rerank candidates using cross-attention
        
        Args:
            query_embedding: Query embedding
            candidate_embeddings: Candidate embeddings
            candidate_metadata: Metadata for each candidate
            top_k: Number of top results to return
            
        Returns:
            Reranked candidates and their scores
        """
        self.eval()
        
        with torch.no_grad():
            # Convert to tensors
            query_tensor = torch.from_numpy(query_embedding).float().unsqueeze(0)
            candidate_tensor = torch.from_numpy(candidate_embeddings).float()
            
            # Get relevance scores
            scores = self.forward(query_tensor, candidate_tensor)
            scores = scores.squeeze().cpu().numpy()
            
            # Sort by scores (descending)
            sorted_indices = np.argsort(scores)[::-1]
            
            if top_k is not None:
                sorted_indices = sorted_indices[:top_k]
            
            # Reorder candidates and scores
            reranked_metadata = [candidate_metadata[i] for i in sorted_indices]
            reranked_scores = scores[sorted_indices]
            
            return reranked_metadata, reranked_scores


class ProductCatalogIndex:
    """
    Enhanced product catalog with cross-modal capabilities
    """
    
    def __init__(self):
        self.products = []
        self.image_embeddings = None
        self.text_embeddings = None
        self.combined_embeddings = None
        
    def add_product(
        self,
        product_id: str,
        title: str,
        description: str,
        category: str,
        price: float,
        image_url: str,
        image_embedding: np.ndarray,
        text_embedding: np.ndarray
    ):
        """
        Add product to catalog with embeddings
        """
        product = {
            'product_id': product_id,
            'title': title,
            'description': description,
            'category': category,
            'price': price,
            'image_url': image_url
        }
        
        self.products.append(product)
        
        # Update embeddings arrays
        if self.image_embeddings is None:
            self.image_embeddings = image_embedding.reshape(1, -1)
            self.text_embeddings = text_embedding.reshape(1, -1)
        else:
            self.image_embeddings = np.vstack([self.image_embeddings, image_embedding.reshape(1, -1)])
            self.text_embeddings = np.vstack([self.text_embeddings, text_embedding.reshape(1, -1)])
    
    def get_product_embeddings(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get all product embeddings
        """
        return self.image_embeddings, self.text_embeddings
    
    def get_products(self) -> List[Dict]:
        """
        Get all products
        """
        return self.products


def create_sample_product_catalog() -> ProductCatalogIndex:
    """
    Create sample product catalog as shown in the workflow diagram
    """
    catalog = ProductCatalogIndex()
    
    # Sample products matching the diagram examples
    sample_products = [
        {
            'product_id': 'shoes_001',
            'title': 'Comfortable Running Shoes',
            'description': 'Lightweight running shoes with excellent cushioning for daily training',
            'category': 'Footwear',
            'price': 89.99,
            'image_url': '/images/running_shoes.jpg'
        },
        {
            'product_id': 'chair_001',
            'title': 'Ergonomic Office Chair',
            'description': 'Professional office chair with lumbar support and adjustable height',
            'category': 'Furniture',
            'price': 299.99,
            'image_url': '/images/office_chair.jpg'
        },
        {
            'product_id': 'dress_001',
            'title': 'Eco-friendly Summer Dress',
            'description': 'Sustainable cotton dress perfect for summer occasions',
            'category': 'Clothing',
            'price': 49.99,
            'image_url': '/images/summer_dress.jpg'
        }
    ]
    
    # Note: In a real implementation, you would generate actual embeddings
    # For now, we'll use random embeddings as placeholders
    for product in sample_products:
        # Placeholder embeddings (would be generated by CLIP in real implementation)
        image_emb = np.random.random(512).astype(np.float32)
        text_emb = np.random.random(512).astype(np.float32)
        
        catalog.add_product(
            product_id=product['product_id'],
            title=product['title'],
            description=product['description'],
            category=product['category'],
            price=product['price'],
            image_url=product['image_url'],
            image_embedding=image_emb,
            text_embedding=text_emb
        )
    
    return catalog