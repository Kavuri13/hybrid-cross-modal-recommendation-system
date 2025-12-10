"""
Demo script for Visual Sentiment Analysis and Occasion-Aware Ranking
Showcases the new advanced features in the recommendation system
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from PIL import Image
import numpy as np
from app.models.visual_sentiment import VisualSentimentAnalyzer
from app.models.occasion_mood import OccasionMoodAnalyzer, ContextProfile, Occasion, Mood

async def demo_visual_sentiment():
    """Demonstrate visual sentiment analysis"""
    print("=" * 80)
    print("VISUAL SENTIMENT ANALYSIS DEMO")
    print("=" * 80)
    
    analyzer = VisualSentimentAnalyzer()
    
    # Create test images with different characteristics
    test_cases = [
        ("Vibrant Red Image", create_test_image((255, 0, 0))),
        ("Calm Blue Image", create_test_image((100, 150, 200))),
        ("Elegant Black & White", create_test_image((128, 128, 128))),
        ("Energetic Yellow", create_test_image((255, 255, 0)))
    ]
    
    for name, image in test_cases:
        print(f"\n{name}:")
        print("-" * 40)
        
        sentiment = await analyzer.analyze_image(image)
        
        print(f"  Overall Score: {sentiment.overall_score:.3f}")
        print(f"  Sentiment Category: {sentiment.sentiment_category}")
        print(f"  Color Harmony: {sentiment.color_harmony:.3f}")
        print(f"  Brightness: {sentiment.brightness_score:.3f}")
        print(f"  Saturation: {sentiment.saturation_score:.3f}")
        print(f"  Warmth: {sentiment.warmth_score:.3f}")
        
        print(f"\n  Top Emotions:")
        sorted_emotions = sorted(
            sentiment.emotion_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        for emotion, score in sorted_emotions:
            print(f"    {emotion}: {score:.3f}")
        
        # Test sentiment boost
        boost = analyzer.compute_sentiment_boost(sentiment)
        print(f"\n  Ranking Boost Multiplier: {boost:.3f}")

def create_test_image(color, size=(224, 224)):
    """Create a simple test image with given color"""
    img_array = np.full((size[0], size[1], 3), color, dtype=np.uint8)
    return Image.fromarray(img_array)

async def demo_occasion_mood_ranking():
    """Demonstrate occasion and mood-aware ranking"""
    print("\n" + "=" * 80)
    print("OCCASION & MOOD-AWARE RANKING DEMO")
    print("=" * 80)
    
    analyzer = OccasionMoodAnalyzer()
    
    # Sample products
    products = [
        {
            "id": "1",
            "title": "Elegant Black Evening Dress",
            "description": "Perfect for formal occasions and weddings",
            "category": "Dresses",
            "price": 149.99
        },
        {
            "id": "2",
            "title": "Casual Beach Shorts",
            "description": "Comfortable and breezy for summer days",
            "category": "Casual",
            "price": 34.99
        },
        {
            "id": "3",
            "title": "Professional Navy Suit",
            "description": "Business formal attire for office",
            "category": "Suits",
            "price": 299.99
        },
        {
            "id": "4",
            "title": "Vibrant Party Top",
            "description": "Fun and colorful for celebrations",
            "category": "Tops",
            "price": 59.99
        }
    ]
    
    # Test different contexts
    contexts = [
        ("Wedding Context", ContextProfile(
            occasion=Occasion.WEDDING,
            mood=Mood.ELEGANT,
            season="spring",
            time_of_day="evening"
        )),
        ("Beach Vacation", ContextProfile(
            occasion=Occasion.BEACH,
            mood=Mood.RELAXED,
            season="summer",
            location_type="beach"
        )),
        ("Business Meeting", ContextProfile(
            occasion=Occasion.BUSINESS,
            mood=Mood.PROFESSIONAL,
            time_of_day="morning"
        )),
        ("Party Night", ContextProfile(
            occasion=Occasion.PARTY,
            mood=Mood.ENERGETIC,
            time_of_day="evening"
        ))
    ]
    
    # Base similarity scores (all equal for demo)
    base_scores = [0.75] * len(products)
    
    for context_name, context in contexts:
        print(f"\n{context_name}:")
        print("-" * 40)
        print(f"  Context: {context.to_dict()}")
        print(f"\n  Product Rankings:")
        
        # Rank products for this context
        ranked = analyzer.rank_products_by_context(products, context, base_scores)
        
        for i, (product, score) in enumerate(ranked, 1):
            print(f"\n  {i}. {product['title']}")
            print(f"     Base Score: {score.base_relevance:.3f}")
            print(f"     Final Score: {score.final_score:.3f}")
            print(f"     Occasion Boost: {score.occasion_boost:.2f}x")
            print(f"     Mood Boost: {score.mood_boost:.2f}x")
            print(f"     Context Boost: {score.context_boost:.2f}x")
            print(f"     Explanation: {score.explanation}")
            if score.matched_attributes:
                print(f"     Matches: {', '.join(score.matched_attributes)}")

async def demo_context_parsing():
    """Demonstrate automatic context parsing from natural language"""
    print("\n" + "=" * 80)
    print("NATURAL LANGUAGE CONTEXT PARSING DEMO")
    print("=" * 80)
    
    analyzer = OccasionMoodAnalyzer()
    
    # Test queries
    queries = [
        "elegant dress for beach wedding in summer",
        "comfortable outfit for office meeting",
        "fun and playful clothes for party tonight",
        "professional suit for job interview",
        "casual wear for outdoor festival",
        "romantic dinner date outfit"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        print("-" * 40)
        
        context = analyzer.parse_context_from_query(query)
        
        print(f"  Detected Occasion: {context.occasion}")
        print(f"  Detected Mood: {context.mood}")
        print(f"  Detected Season: {context.season}")
        print(f"  Detected Time: {context.time_of_day}")
        print(f"  Detected Location: {context.location_type}")

async def demo_full_pipeline():
    """Demonstrate the full pipeline with both features"""
    print("\n" + "=" * 80)
    print("FULL PIPELINE DEMO: SENTIMENT + OCCASION RANKING")
    print("=" * 80)
    
    sentiment_analyzer = VisualSentimentAnalyzer()
    occasion_analyzer = OccasionMoodAnalyzer()
    
    # Simulate a search scenario
    query = "elegant dress for evening wedding"
    print(f"\nSearch Query: '{query}'")
    
    # Parse context
    context = occasion_analyzer.parse_context_from_query(query)
    print(f"\nParsed Context:")
    print(f"  Occasion: {context.occasion}")
    print(f"  Mood: {context.mood}")
    
    # Sample products with images
    products = [
        {
            "id": "1",
            "title": "Red Evening Gown",
            "description": "Elegant formal dress",
            "category": "Dresses",
            "image": create_test_image((180, 50, 50))  # Deep red
        },
        {
            "id": "2",
            "title": "Casual T-Shirt",
            "description": "Comfortable everyday wear",
            "category": "Casual",
            "image": create_test_image((100, 150, 200))  # Light blue
        }
    ]
    
    print(f"\n{'Product':<30} {'Base':<8} {'Sentiment':<12} {'Occasion':<12} {'Final':<8}")
    print("-" * 80)
    
    for product in products:
        # Base CLIP score (simulated)
        base_score = 0.7
        
        # Apply sentiment analysis
        sentiment = await sentiment_analyzer.analyze_image(product['image'])
        sentiment_boost = sentiment_analyzer.compute_sentiment_boost(sentiment)
        sentiment_score = base_score * sentiment_boost
        
        # Apply occasion ranking
        occasion_score = occasion_analyzer.score_product_for_context(
            product, context, sentiment_score
        )
        
        print(f"{product['title']:<30} {base_score:<8.3f} "
              f"{sentiment_score:<12.3f} {occasion_score.final_score:<12.3f}")
        print(f"  → {occasion_score.explanation}")

async def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("ADVANCED FEATURES DEMONSTRATION")
    print("Visual Sentiment Analysis + Occasion & Mood-Aware Ranking")
    print("=" * 80)
    
    # Run demos
    await demo_visual_sentiment()
    await demo_occasion_mood_ranking()
    await demo_context_parsing()
    await demo_full_pipeline()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nThese features are now integrated into the /search/enhanced API endpoint.")
    print("\nExample API usage:")
    print("  POST /search/enhanced")
    print("  {")
    print('    "text": "elegant dress for beach wedding",')
    print('    "occasion": "wedding",')
    print('    "mood": "elegant",')
    print('    "season": "summer",')
    print('    "enable_sentiment_scoring": true,')
    print('    "enable_occasion_ranking": true,')
    print('    "top_k": 20')
    print("  }")

if __name__ == "__main__":
    asyncio.run(main())
