"""
API Examples for Advanced Features
Visual Sentiment Analysis + Occasion & Mood-Aware Ranking
"""

import requests
import json
import base64
from pathlib import Path

# Base URL - adjust if needed
BASE_URL = "http://localhost:8000"

def example_1_basic_occasion_search():
    """Example 1: Basic search with occasion context"""
    print("\n" + "="*80)
    print("Example 1: Wedding Dress Search with Occasion Context")
    print("="*80)
    
    payload = {
        "text": "elegant white dress",
        "top_k": 10,
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": True,
        "occasion": "wedding",
        "mood": "elegant",
        "season": "spring"
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        print(f"⏱️  Query time: {results['meta']['query_time']:.2f}s")
        
        # Show top 3 results
        for i, product in enumerate(results['results'][:3], 1):
            print(f"\n{i}. {product['title']}")
            print(f"   Score: {product['score']:.3f}")
            if 'occasion_score' in product:
                print(f"   Occasion: {product['occasion_score']['explanation']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)


def example_2_beach_vacation():
    """Example 2: Beach vacation outfit search"""
    print("\n" + "="*80)
    print("Example 2: Beach Vacation Outfit Search")
    print("="*80)
    
    payload = {
        "text": "casual summer wear",
        "top_k": 15,
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": True,
        "occasion": "beach",
        "mood": "relaxed",
        "season": "summer",
        "location_type": "outdoor"
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        
        # Show sentiment analysis
        for i, product in enumerate(results['results'][:3], 1):
            print(f"\n{i}. {product['title']}")
            if 'sentiment' in product:
                sentiment = product['sentiment']
                print(f"   Sentiment: {sentiment['sentiment_category']}")
                print(f"   Aesthetic Score: {sentiment['overall_score']:.3f}")
    else:
        print(f"❌ Error: {response.status_code}")


def example_3_business_professional():
    """Example 3: Professional business outfit"""
    print("\n" + "="*80)
    print("Example 3: Business Professional Search")
    print("="*80)
    
    payload = {
        "text": "professional suit for interview",
        "top_k": 10,
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": True,
        "occasion": "interview",
        "mood": "confident",
        "time_of_day": "morning"
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        
        for i, product in enumerate(results['results'][:3], 1):
            print(f"\n{i}. {product['title']}")
            print(f"   Final Score: {product['score']:.3f}")
            if 'occasion_score' in product:
                occ = product['occasion_score']
                print(f"   Occasion Boost: {occ['occasion_boost']:.2f}x")
                print(f"   Mood Boost: {occ['mood_boost']:.2f}x")
    else:
        print(f"❌ Error: {response.status_code}")


def example_4_party_night():
    """Example 4: Party outfit with image search"""
    print("\n" + "="*80)
    print("Example 4: Party Night Outfit (with image)")
    print("="*80)
    
    # You would load and encode your image here
    # For demo, we'll just use text
    payload = {
        "text": "colorful party dress",
        "top_k": 12,
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": True,
        "occasion": "party",
        "mood": "energetic",
        "time_of_day": "evening"
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        
        # Show products with high sentiment scores
        print("\nProducts with highest aesthetic appeal:")
        sorted_by_sentiment = sorted(
            results['results'],
            key=lambda x: x.get('sentiment', {}).get('overall_score', 0),
            reverse=True
        )[:3]
        
        for i, product in enumerate(sorted_by_sentiment, 1):
            print(f"\n{i}. {product['title']}")
            if 'sentiment' in product:
                print(f"   Aesthetic Score: {product['sentiment']['overall_score']:.3f}")
                print(f"   Category: {product['sentiment']['sentiment_category']}")
    else:
        print(f"❌ Error: {response.status_code}")


def example_5_natural_language():
    """Example 5: Natural language query (auto-parsing)"""
    print("\n" + "="*80)
    print("Example 5: Natural Language Query (Auto Context Parsing)")
    print("="*80)
    
    # The system will automatically parse occasion/mood from the query
    payload = {
        "text": "elegant dress for romantic dinner date in summer evening",
        "top_k": 10,
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": True
        # No explicit occasion/mood - let it auto-detect!
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        
        # Show detected context
        if 'context' in results['meta']:
            context = results['meta']['context']
            print(f"\n🔍 Auto-detected context:")
            print(f"   Occasion: {context.get('occasion')}")
            print(f"   Mood: {context.get('mood')}")
            print(f"   Season: {context.get('season')}")
            print(f"   Time: {context.get('time_of_day')}")
        
        # Show top results
        for i, product in enumerate(results['results'][:3], 1):
            print(f"\n{i}. {product['title']}")
            print(f"   Score: {product['score']:.3f}")
    else:
        print(f"❌ Error: {response.status_code}")


def example_6_sentiment_only():
    """Example 6: Sentiment analysis only (no occasion)"""
    print("\n" + "="*80)
    print("Example 6: Visual Sentiment Analysis Only")
    print("="*80)
    
    payload = {
        "text": "beautiful dress",
        "top_k": 10,
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": False  # Disabled
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        
        print("\nSentiment Analysis Results:")
        for i, product in enumerate(results['results'][:5], 1):
            if 'sentiment' in product:
                s = product['sentiment']
                print(f"\n{i}. {product['title']}")
                print(f"   Overall Score: {s['overall_score']:.3f}")
                print(f"   Category: {s['sentiment_category']}")
                print(f"   Color Harmony: {s['color_harmony']:.3f}")
                print(f"   Brightness: {s['brightness_score']:.3f}")
    else:
        print(f"❌ Error: {response.status_code}")


def example_7_multimodal_context():
    """Example 7: Multimodal search with full context"""
    print("\n" + "="*80)
    print("Example 7: Full Multimodal Search with Context")
    print("="*80)
    
    payload = {
        "text": "summer dress",
        # "image": "base64_encoded_image",  # Add your image here
        "priority": {
            "image": 0.6,
            "text": 0.4
        },
        "top_k": 15,
        "sources": ["amazon", "myntra"],  # Specific sources
        "enable_sentiment_scoring": True,
        "enable_occasion_ranking": True,
        "occasion": "beach",
        "mood": "relaxed",
        "season": "summer",
        "time_of_day": "afternoon",
        "location_type": "outdoor"
    }
    
    response = requests.post(f"{BASE_URL}/search/enhanced", json=payload)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Found {len(results['results'])} products")
        print(f"⏱️  Total query time: {results['meta']['query_time']:.2f}s")
        
        # Detailed breakdown
        meta = results['meta']
        print(f"\n📊 Pipeline Breakdown:")
        print(f"   Candidates fetched: {meta['num_candidates']}")
        print(f"   Valid products: {meta['num_valid']}")
        print(f"   Sentiment enabled: {meta['sentiment_enabled']}")
        print(f"   Occasion enabled: {meta['occasion_enabled']}")
        
        # Top results with full details
        print("\n🏆 Top Results:")
        for i, product in enumerate(results['results'][:3], 1):
            print(f"\n{i}. {product['title']}")
            print(f"   Category: {product.get('category', 'N/A')}")
            print(f"   Price: ${product.get('price', 'N/A')}")
            print(f"   Final Score: {product['score']:.3f}")
            
            if 'sentiment' in product:
                print(f"   Sentiment: {product['sentiment']['sentiment_category']} "
                      f"({product['sentiment']['overall_score']:.3f})")
            
            if 'occasion_score' in product:
                print(f"   Match: {product['occasion_score']['explanation']}")
    else:
        print(f"❌ Error: {response.status_code}")


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("ADVANCED FEATURES API EXAMPLES")
    print("Visual Sentiment Analysis + Occasion & Mood-Aware Ranking")
    print("="*80)
    print("\nMake sure the backend server is running on http://localhost:8000")
    print("Start with: python backend/start_server.py")
    
    input("\nPress Enter to start examples...")
    
    try:
        # Test server
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("⚠️  Server may not be ready")
    except:
        print("❌ Cannot connect to server. Please start the backend first.")
        return
    
    # Run examples
    example_1_basic_occasion_search()
    example_2_beach_vacation()
    example_3_business_professional()
    example_4_party_night()
    example_5_natural_language()
    example_6_sentiment_only()
    example_7_multimodal_context()
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED!")
    print("="*80)


if __name__ == "__main__":
    main()
