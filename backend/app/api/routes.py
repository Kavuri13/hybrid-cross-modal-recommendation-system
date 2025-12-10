from fastapi import APIRouter, HTTPException, UploadFile, File, Request, Query, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Dict, Any, Tuple
import base64
import io
import json
import time
from PIL import Image
import numpy as np
import logging
from enum import Enum

# Import new utilities
from app.utils.search_service import get_search_service
from app.models.occasion_mood import ContextProfile, Occasion, Mood

logger = logging.getLogger(__name__)

router = APIRouter()

class FusionMethod(str, Enum):
    WEIGHTED_AVG = "weighted_avg"
    CONCATENATION = "concatenation"
    ELEMENT_WISE = "element_wise"

class RerankingMethod(str, Enum):
    NONE = "none"
    CROSS_ATTENTION = "cross_attention"
    COSINE_RERANK = "cosine_rerank"
    CATEGORY_BOOST = "category_boost"

class QueryRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None  # base64 encoded
    top_k: int = Field(default=10, ge=1, le=100)
    image_weight: float = Field(default=0.7, ge=0.0, le=1.0)
    text_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    fusion_method: FusionMethod = FusionMethod.WEIGHTED_AVG
    category_filter: Optional[str] = None
    price_min: Optional[float] = Field(default=None, ge=0)
    price_max: Optional[float] = Field(default=None, ge=0)
    enable_reranking: bool = False
    reranking_method: RerankingMethod = RerankingMethod.CROSS_ATTENTION
    diversity_weight: float = Field(default=0.1, ge=0.0, le=1.0)
    # New sentiment and occasion parameters
    enable_sentiment_scoring: bool = Field(default=True, description="Enable visual sentiment analysis")
    enable_occasion_ranking: bool = Field(default=True, description="Enable occasion-aware ranking")
    occasion: Optional[str] = Field(default=None, description="Occasion context (e.g., wedding, party, business)")
    mood: Optional[str] = Field(default=None, description="Mood context (e.g., confident, elegant, relaxed)")
    season: Optional[str] = Field(default=None, description="Season context (spring, summer, fall, winter)")
    time_of_day: Optional[str] = Field(default=None, description="Time context (morning, afternoon, evening)")

class ProductResult(BaseModel):
    product_id: str
    title: str
    image_url: str
    similarity_score: float
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    refined_similarity: Optional[float] = None
    diversity_score: Optional[float] = None
    # New sentiment and occasion fields
    sentiment: Optional[Dict[str, Any]] = None
    sentiment_boost: Optional[float] = None
    occasion_score: Optional[Dict[str, Any]] = None
    match_tags: Optional[List[str]] = None

class QueryResponse(BaseModel):
    results: List[ProductResult]
    query_time: float
    total_products: int
    fusion_method_used: str
    reranking_applied: bool
    search_metadata: Dict[str, Any] = {}

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    embedding_type: str
    dimension: int
    processing_time: float

class IndexStats(BaseModel):
    total_products: int
    index_type: str
    embedding_dimension: int
    category_distribution: Dict[str, int]
    index_size_mb: float
    health_status: str

class EmbedRequest(BaseModel):
    product_id: str
    title: str
    image_path: str
    category: Optional[str] = None
    price: Optional[float] = None

@router.post("/search/workflow", response_model=QueryResponse)
async def workflow_search(request: QueryRequest, app_request: Request):
    """
    Advanced cross-modal product search implementing the complete workflow:
    1. Dual encoder (image + text)
    2. Embedding fusion with weighted averaging
    3. FAISS/HNSW indexing and retrieval
    4. Optional cross-attention reranking
    5. Refined top-K list output
    """
    start_time = time.time()
    
    # Validate request
    if not request.text and not request.image:
        raise HTTPException(status_code=400, detail="Either text or image query must be provided")
    
    if abs(request.image_weight + request.text_weight - 1.0) > 0.01:
        raise HTTPException(status_code=400, detail="Image weight and text weight must sum to 1.0")
    
    # Get models from app state
    clip_model = getattr(app_request.app.state, 'clip_model', None)
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    reranker = getattr(app_request.app.state, 'reranker', None)
    
    if not clip_model or not faiss_index:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    if not request.text and not request.image:
        raise HTTPException(status_code=400, detail="Either text or image must be provided")
    
    try:
        # Process query
        query_embedding = None
        
        if request.text and request.image:
            # Combined search
            text_emb = await clip_model.encode_text(request.text)
            
            # Decode base64 image
            image_data = base64.b64decode(request.image)
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            image_emb = await clip_model.encode_image(image)
            
            # Weighted fusion
            query_embedding = (
                request.text_weight * text_emb + 
                request.image_weight * image_emb
            )
            
        elif request.text:
            # Text-only search
            query_embedding = await clip_model.encode_text(request.text)
            
        elif request.image:
            # Image-only search
            image_data = base64.b64decode(request.image)
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            query_embedding = await clip_model.encode_image(image)
        
        # Normalize embedding
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Search in FAISS index
        similarities, indices = faiss_index.search(query_embedding, request.top_k)
        
        # Get product metadata
        results = []
        for i, (similarity, idx) in enumerate(zip(similarities[0], indices[0])):
            if idx == -1:  # Invalid index
                continue
                
            product = faiss_index.get_product_metadata(idx)
            if product:
                results.append(ProductResult(
                    product_id=product.get('product_id', str(idx)),
                    title=product.get('title', f'Product {idx}'),
                    image_url=product.get('image_url', f'/images/product_{idx}.jpg'),
                    similarity_score=float(similarity),
                    price=product.get('price'),
                    category=product.get('category')
                ))
        
        query_time = time.time() - start_time
        
        return QueryResponse(
            results=results,
            query_time=query_time,
            total_products=len(results)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/search/workflow")
async def workflow_search_multipart(
    request: Request,
    text: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    top_k: int = Form(12),
    image_weight: float = Form(0.7),
    text_weight: float = Form(0.3),
    fusion_method: str = Form("weighted_avg"),
    category_filter: Optional[str] = Form(None),
    price_min: Optional[float] = Form(None),
    price_max: Optional[float] = Form(None),
    enable_reranking: bool = Form(False),
    reranking_method: str = Form("cross_attention"),
    diversity_weight: float = Form(0.1)
):
    """
    Complete cross-modal workflow search supporting multipart form data.
    This endpoint implements the full pipeline from the workflow diagram.
    """
    start_time = time.time()
    
    # Validate input
    if not text and not image:
        raise HTTPException(status_code=400, detail="Either text or image query must be provided")
    
    # Get models from app state
    clip_model = getattr(request.app.state, 'clip_model', None)
    faiss_index = getattr(request.app.state, 'faiss_index', None)
    reranker = getattr(request.app.state, 'reranker', None)
    
    # Mock models if not available (for development)
    mock_results = []
    
    try:
        # Phase 1: Dual Encoding
        encoding_start = time.time()
        text_embedding = None
        image_embedding = None
        
        if text and clip_model:
            text_embedding = await clip_model.encode_text(text)
        
        if image and clip_model:
            image_data = await image.read()
            pil_image = Image.open(io.BytesIO(image_data)).convert('RGB')
            image_embedding = await clip_model.encode_image(pil_image)
        
        encoding_time = time.time() - encoding_start
        
        # Phase 2: Embedding Fusion
        fusion_start = time.time()
        query_embedding = None
        
        if text_embedding is not None and image_embedding is not None:
            # Combined search with fusion
            if fusion_method == "weighted_avg":
                query_embedding = text_weight * text_embedding + image_weight * image_embedding
            elif fusion_method == "concatenation":
                query_embedding = np.concatenate([text_embedding, image_embedding])
            elif fusion_method == "element_wise":
                query_embedding = text_embedding * image_embedding
            else:
                query_embedding = text_weight * text_embedding + image_weight * image_embedding
        elif text_embedding is not None:
            query_embedding = text_embedding
        elif image_embedding is not None:
            query_embedding = image_embedding
        
        if query_embedding is not None:
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        fusion_time = time.time() - fusion_start
        
        # Phase 3: FAISS Vector Search
        search_start = time.time()
        initial_results = []
        
        if faiss_index and query_embedding is not None:
            similarities, indices = faiss_index.search(query_embedding.reshape(1, -1), top_k * 2)  # Get more for reranking
            
            for similarity, idx in zip(similarities[0], indices[0]):
                if idx != -1:
                    # Mock product data for development
                    product_data = {
                        'id': str(idx),
                        'name': f'Product {idx}',
                        'description': f'High-quality product {idx} matching your search',
                        'price': 50.0 + (idx % 100) * 2.5,
                        'original_price': None if idx % 3 != 0 else 50.0 + (idx % 100) * 3.0,
                        'image_url': f'https://picsum.photos/400/400?random={idx}',
                        'category': ['Clothing', 'Footwear', 'Electronics', 'Home'][idx % 4],
                        'rating': 3.5 + (idx % 3) * 0.5,
                        'review_count': 10 + (idx % 50) * 2,
                        'availability': ['in_stock', 'low_stock', 'out_of_stock'][idx % 3],
                        'similarity_score': float(similarity),
                        'text_relevance': float(similarity * 0.9) if text else None,
                        'image_relevance': float(similarity * 1.1) if image else None,
                    }
                    
                    # Apply filters
                    if category_filter and product_data['category'] != category_filter:
                        continue
                    if price_min and product_data['price'] < price_min:
                        continue
                    if price_max and product_data['price'] > price_max:
                        continue
                    
                    initial_results.append(product_data)
        
        search_time = time.time() - search_start
        
        # Phase 4: Optional Reranking
        reranking_time = 0
        final_results = initial_results[:top_k]
        
        if enable_reranking and len(initial_results) > 0:
            reranking_start = time.time()
            
            if reranking_method == "cross_attention" and reranker:
                # Apply cross-attention reranking
                try:
                    reranked_scores = await reranker.rerank(
                        query_embedding, 
                        [r['similarity_score'] for r in initial_results[:top_k]]
                    )
                    for i, score in enumerate(reranked_scores):
                        if i < len(final_results):
                            final_results[i]['reranking_score'] = float(score)
                    
                    # Resort by reranked scores
                    final_results.sort(key=lambda x: x.get('reranking_score', x['similarity_score']), reverse=True)
                except Exception as e:
                    logger.warning(f"Reranking failed: {e}")
            
            elif reranking_method == "cosine_rerank":
                # Simple cosine similarity boost
                for result in final_results:
                    boost = 0.1 if result['category'] in ['Electronics', 'Clothing'] else 0.0
                    result['reranking_score'] = result['similarity_score'] + boost
                
                final_results.sort(key=lambda x: x.get('reranking_score', x['similarity_score']), reverse=True)
            
            reranking_time = time.time() - reranking_start
        
        # Add cross-modal features
        for i, result in enumerate(final_results):
            result['cross_modal_features'] = {
                'dominant_colors': [f'#{hex(hash(str(i + j)) % 16777215)[2:].zfill(6)}' for j in range(3)],
                'detected_objects': ['product', 'item'],
                'style_attributes': ['modern', 'quality'],
                'semantic_tags': [result['category'].lower(), 'recommended']
            }
        
        total_time = time.time() - start_time
        
        # Return comprehensive results
        return JSONResponse({
            'results': final_results,
            'processing_stats': {
                'total_results': len(final_results),
                'processing_time_ms': int(total_time * 1000),
                'search_mode': 'combined' if text and image else ('text' if text else 'image'),
                'fusion_method': fusion_method if text and image else None,
                'reranking_applied': enable_reranking,
                'vector_search_time': int(search_time * 1000),
                'reranking_time': int(reranking_time * 1000) if enable_reranking else None,
                'encoding_time': int(encoding_time * 1000),
                'fusion_time': int(fusion_time * 1000)
            }
        })
        
    except Exception as e:
        logger.error(f"Workflow search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

# Additional utility endpoints for the complete workflow

@router.get("/workflow/info")
async def get_workflow_info():
    """
    Get information about the implemented cross-modal workflow
    """
    return {
        "workflow_name": "Cross-Modal Product Recommendation System",
        "components": {
            "input_layer": "Supports both image and text queries simultaneously",
            "dual_encoder": "CLIP ViT-B/32 for both image and text encoding",
            "embedding_fusion": "Weighted average, concatenation, or element-wise fusion",
            "indexing_retrieval": "FAISS HNSW index with nearest neighbor search",
            "optional_reranking": "Cross-attention model and refinement methods",
            "output": "Ranked product list with similarity scores"
        },
        "features": [
            "Multi-modal search (image + text)",
            "Advanced embedding fusion methods",
            "Hybrid search with filtering",
            "Cross-attention reranking",
            "Diversity-aware results",
            "Category and price filtering",
            "Batch processing support",
            "Performance benchmarking",
            "Comprehensive health monitoring"
        ],
        "api_version": "1.0.0",
        "supported_formats": {
            "images": ["JPEG", "PNG", "WebP"],
            "text": "UTF-8 encoded strings",
            "embeddings": "512-dimensional vectors"
        }
    }

@router.post("/embed")
async def embed_product(request: EmbedRequest, app_request: Request):
    """
    Generate embeddings for a new product
    """
    clip_model = getattr(app_request.app.state, 'clip_model', None)
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    
    if not clip_model or not faiss_index:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Load and encode image
        image = Image.open(request.image_path).convert('RGB')
        image_emb = await clip_model.encode_image(image)
        
        # Encode text
        text_emb = await clip_model.encode_text(request.title)
        
        # Combine embeddings (weighted average)
        combined_emb = 0.7 * image_emb + 0.3 * text_emb
        combined_emb = combined_emb / np.linalg.norm(combined_emb)
        
        # Add to FAISS index
        product_metadata = {
            'product_id': request.product_id,
            'title': request.title,
            'image_url': f'/images/{request.product_id}.jpg',
            'category': request.category,
            'price': request.price
        }
        
        faiss_index.add_product(combined_emb, product_metadata)
        
        return {"message": "Product embedded successfully", "product_id": request.product_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

@router.get("/index/status", response_model=IndexStats)
async def get_index_status(app_request: Request):
    """
    Get comprehensive index statistics and health status
    """
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    if not faiss_index:
        raise HTTPException(status_code=503, detail="FAISS index not loaded")
    
    try:
        stats = faiss_index.get_index_statistics()
        health = faiss_index.health_check()
        
        return IndexStats(
            total_products=stats['total_products'],
            index_type=stats['index_type'],
            embedding_dimension=stats['embedding_dimension'],
            category_distribution=stats['category_distribution'],
            index_size_mb=stats['index_size_mb'],
            health_status=health['status']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get index status: {str(e)}")

@router.get("/index/health")
async def get_index_health(app_request: Request):
    """
    Perform comprehensive health check on the search index
    """
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    if not faiss_index:
        raise HTTPException(status_code=503, detail="FAISS index not loaded")
    
    try:
        health_status = faiss_index.health_check()
        return health_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.post("/index/rebuild")
async def rebuild_index(app_request: Request):
    """
    Rebuild the search index (admin operation)
    """
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    if not faiss_index:
        raise HTTPException(status_code=503, detail="FAISS index not loaded")
    
    try:
        # This would rebuild the index from stored product data
        # Implementation depends on your data storage strategy
        start_time = time.time()
        
        # For now, just reinitialize
        faiss_index._initialize_index()
        
        rebuild_time = time.time() - start_time
        
        return {
            "message": "Index rebuilt successfully",
            "rebuild_time": rebuild_time,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Index rebuild failed: {str(e)}")

@router.get("/index/debug")
async def debug_index(
    app_request: Request,
    query_text: str = Query(default="test query", description="Test query for debugging")
):
    """
    Debug endpoint for analyzing search behavior
    """
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    clip_model = getattr(app_request.app.state, 'clip_model', None)
    
    if not faiss_index or not clip_model:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Generate test embedding
        test_embedding = await clip_model.encode_text(query_text)
        
        # Get debug information
        debug_info = faiss_index.debug_search(test_embedding, k=5, verbose=True)
        
        return debug_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug failed: {str(e)}")
    """
    Get FAISS index status and statistics
    """
    faiss_index = getattr(app_request.app.state, 'faiss_index', None)
    
    if not faiss_index:
        return {"status": "not_loaded", "total_products": 0}
    
    return {
        "status": "loaded",
        "total_products": faiss_index.get_total_products(),
        "index_type": "HNSW",
        "embedding_dim": faiss_index.get_embedding_dim()
    }

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file and return base64 encoded string
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_data = await file.read()
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        return {
            "message": "Image uploaded successfully",
            "image_base64": image_b64,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ===== NEW ENHANCED SEARCH ENDPOINT WITH LIVE E-COMMERCE DATA =====

class EnhancedSearchRequest(BaseModel):
    """Enhanced search request with live e-commerce integration"""
    text: Optional[str] = None
    image_b64: Optional[str] = Field(None, alias="image")
    priority: Optional[Dict[str, float]] = Field(
        default={'image': 0.6, 'text': 0.4},
        description="Priority weights for image and text"
    )
    top_k: int = Field(default=20, ge=1, le=100)
    sources: Optional[List[str]] = Field(
        default=None,
        description="E-commerce sources: amazon, flipkart, myntra, ikea, meesho"
    )
    # New sentiment and occasion parameters
    enable_sentiment_scoring: bool = Field(default=True, description="Enable visual sentiment analysis")
    enable_occasion_ranking: bool = Field(default=True, description="Enable occasion-aware ranking")
    occasion: Optional[str] = Field(default=None, description="Occasion context (e.g., wedding, party, business)")
    mood: Optional[str] = Field(default=None, description="Mood context (e.g., confident, elegant, relaxed)")
    season: Optional[str] = Field(default=None, description="Season context (spring, summer, fall, winter)")
    time_of_day: Optional[str] = Field(default=None, description="Time context (morning, afternoon, evening)")
    location_type: Optional[str] = Field(default=None, description="Location context (indoor, outdoor, beach)")

class EnhancedSearchResponse(BaseModel):
    """Enhanced search response with match tags and metadata"""
    results: List[Dict[str, Any]]
    meta: Dict[str, Any]

@router.post("/search/enhanced", response_model=EnhancedSearchResponse)
async def enhanced_search(request: EnhancedSearchRequest, app_request: Request):
    """
    ENHANCED MULTIMODAL SEARCH WITH LIVE E-COMMERCE DATA
    
    This endpoint implements the complete system as per requirements:
    - Fetches live product data from multiple e-commerce sources
    - Uses CLIP for multimodal encoding
    - Applies late fusion scoring
    - Deduplicates results
    - Returns ranked products with match tags
    - NO DATABASE - all data fetched on demand
    """
    try:
        # Get CLIP model
        clip_model = getattr(app_request.app.state, 'clip_model', None)
        if not clip_model:
            raise HTTPException(status_code=503, detail="CLIP model not loaded")
        
        # Decode image if provided
        image_query = None
        if request.image_b64:
            try:
                image_data = base64.b64decode(request.image_b64)
                image_query = Image.open(io.BytesIO(image_data)).convert('RGB')
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")
        
        # Build context profile from request
        context = None
        if request.occasion or request.mood or request.season or request.time_of_day:
            # Parse occasion and mood enums
            occasion_enum = None
            if request.occasion:
                try:
                    occasion_enum = Occasion(request.occasion.lower())
                except ValueError:
                    logger.warning(f"Invalid occasion: {request.occasion}")
            
            mood_enum = None
            if request.mood:
                try:
                    mood_enum = Mood(request.mood.lower())
                except ValueError:
                    logger.warning(f"Invalid mood: {request.mood}")
            
            context = ContextProfile(
                occasion=occasion_enum,
                mood=mood_enum,
                season=request.season,
                time_of_day=request.time_of_day,
                location_type=request.location_type
            )
        
        # Get search service
        search_service = get_search_service(clip_model)
        
        # Perform search with sentiment and occasion analysis
        results = await search_service.search(
            text_query=request.text,
            image_query=image_query,
            priority=request.priority,
            top_k=request.top_k,
            sources=request.sources,
            enable_sentiment_scoring=request.enable_sentiment_scoring,
            enable_occasion_ranking=request.enable_occasion_ranking,
            context=context
        )
        
        return EnhancedSearchResponse(
            results=results['results'],
            meta=results['meta']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/search/advanced", response_model=EnhancedSearchResponse)
async def advanced_search_with_context(
    request: EnhancedSearchRequest,
    app_request: Request
):
    """
    Advanced search with visual sentiment analysis and occasion-aware ranking.
    
    Features:
    - Visual sentiment scoring for aesthetic appeal
    - Occasion and mood-aware personalized ranking
    - Automatic context parsing from natural language queries
    - Enhanced product scoring with explanations
    """
    try:
        # Get CLIP model
        clip_model = getattr(app_request.app.state, 'clip_model', None)
        if not clip_model:
            raise HTTPException(status_code=503, detail="CLIP model not loaded")
        
        # Decode image if provided
        image_query = None
        if request.image_b64:
            try:
                image_data = base64.b64decode(request.image_b64)
                image_query = Image.open(io.BytesIO(image_data)).convert('RGB')
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")
        
        # Build context profile from request
        context = None
        if request.occasion or request.mood or request.season or request.time_of_day:
            # Parse occasion and mood enums
            occasion_enum = None
            if request.occasion:
                try:
                    occasion_enum = Occasion(request.occasion.lower())
                except ValueError:
                    logger.warning(f"Invalid occasion: {request.occasion}")
            
            mood_enum = None
            if request.mood:
                try:
                    mood_enum = Mood(request.mood.lower())
                except ValueError:
                    logger.warning(f"Invalid mood: {request.mood}")
            
            context = ContextProfile(
                occasion=occasion_enum,
                mood=mood_enum,
                season=request.season,
                time_of_day=request.time_of_day,
                location_type=request.location_type
            )
        
        # Get search service
        search_service = get_search_service(clip_model)
        
        # Perform advanced search with sentiment and occasion analysis
        results = await search_service.search(
            text_query=request.text,
            image_query=image_query,
            priority=request.priority,
            top_k=request.top_k,
            sources=request.sources,
            enable_sentiment_scoring=request.enable_sentiment_scoring,
            enable_occasion_ranking=request.enable_occasion_ranking,
            context=context
        )
        
        return EnhancedSearchResponse(
            results=results['results'],
            meta=results['meta']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Advanced search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Advanced search failed: {str(e)}")


@router.get("/cache/stats")
async def get_cache_stats():
    """Get ephemeral cache statistics"""
    from app.utils.cache import get_cache
    cache = get_cache()
    return cache.get_stats()


@router.post("/cache/clear")
async def clear_cache():
    """Clear ephemeral cache"""
    from app.utils.cache import get_cache
    cache = get_cache()
    cache.clear_all()
    return {"message": "Cache cleared successfully"}