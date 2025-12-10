"""
Test E-Commerce API Configuration
Run this script to verify your API credentials are working
"""

import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.ecommerce_fetchers import EcommerceFetcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_api_credentials():
    """Test if API credentials are configured and working"""
    
    print("=" * 60)
    print("E-Commerce API Configuration Test")
    print("=" * 60)
    print()
    
    # Check environment variables
    print("📋 Checking environment variables...")
    env_vars = {
        "Amazon": ["AMAZON_ACCESS_KEY", "AMAZON_SECRET_KEY", "AMAZON_PARTNER_TAG"],
        "Flipkart": ["FLIPKART_AFFILIATE_ID", "FLIPKART_AFFILIATE_TOKEN"],
        "Myntra": ["MYNTRA_API_KEY"],
    }
    
    configured_apis = []
    for api_name, vars_list in env_vars.items():
        all_set = all(os.getenv(var) for var in vars_list)
        status = "✅ Configured" if all_set else "❌ Not configured (using mock)"
        print(f"  {api_name}: {status}")
        if all_set:
            configured_apis.append(api_name.lower())
    
    print(f"  IKEA: ✅ No credentials needed")
    print(f"  Meesho: ✅ No credentials needed (web scraping)")
    print()
    
    # Test search
    print("🔍 Testing product search...")
    fetcher = EcommerceFetcher()
    
    test_queries = ["laptop", "red dress", "running shoes"]
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        try:
            products = await fetcher.search_all(
                query=query,
                sources=["amazon", "flipkart", "myntra", "ikea", "meesho"],
                max_per_source=3
            )
            
            print(f"  ✅ Found {len(products)} products")
            
            # Group by source
            by_source = {}
            for p in products:
                by_source[p.source] = by_source.get(p.source, 0) + 1
            
            for source, count in by_source.items():
                print(f"     - {source}: {count} products")
            
            # Show sample products
            if products:
                print(f"\n  📦 Sample products:")
                for i, product in enumerate(products[:2], 1):
                    print(f"     {i}. {product.title}")
                    print(f"        Price: ${product.price}")
                    print(f"        Source: {product.source}")
                    print(f"        URL: {product.buy_url[:60]}...")
        
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print()
    print("=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print()
    
    if not configured_apis:
        print("⚠️  No API credentials configured - system is using MOCK data")
        print("   To use real products, add API credentials to .env file")
        print("   See API_SETUP_GUIDE.md for instructions")
    else:
        print(f"✅ {len(configured_apis)} API(s) configured: {', '.join(configured_apis)}")
    
    print()


if __name__ == "__main__":
    asyncio.run(test_api_credentials())
