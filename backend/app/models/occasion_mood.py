"""
Occasion & Mood-Aware Retrieval System
Personalizes product ranking based on context, occasion, and user mood
"""

import numpy as np
from typing import Dict, List, Optional, Set, Tuple
import logging
from dataclasses import dataclass
from enum import Enum
import re

logger = logging.getLogger(__name__)

class Occasion(str, Enum):
    """Pre-defined occasion types"""
    WEDDING = "wedding"
    PARTY = "party"
    BUSINESS = "business"
    CASUAL = "casual"
    FORMAL = "formal"
    SPORT = "sport"
    BEACH = "beach"
    DATE = "date"
    TRAVEL = "travel"
    INTERVIEW = "interview"
    FESTIVAL = "festival"
    OUTDOOR = "outdoor"
    EVENING = "evening"
    DAYTIME = "daytime"

class Mood(str, Enum):
    """Pre-defined mood types"""
    CONFIDENT = "confident"
    RELAXED = "relaxed"
    ELEGANT = "elegant"
    PLAYFUL = "playful"
    PROFESSIONAL = "professional"
    ADVENTUROUS = "adventurous"
    ROMANTIC = "romantic"
    ENERGETIC = "energetic"
    SOPHISTICATED = "sophisticated"
    COMFORTABLE = "comfortable"

@dataclass
class ContextProfile:
    """User context profile for personalized ranking"""
    occasion: Optional[Occasion] = None
    mood: Optional[Mood] = None
    season: Optional[str] = None  # spring, summer, fall, winter
    time_of_day: Optional[str] = None  # morning, afternoon, evening, night
    weather: Optional[str] = None  # sunny, rainy, cold, hot
    location_type: Optional[str] = None  # indoor, outdoor, beach, city
    
    def to_dict(self) -> Dict:
        return {
            "occasion": self.occasion,
            "mood": self.mood,
            "season": self.season,
            "time_of_day": self.time_of_day,
            "weather": self.weather,
            "location_type": self.location_type
        }

@dataclass
class OccasionScore:
    """Score result for occasion-aware ranking"""
    base_relevance: float
    occasion_boost: float
    mood_boost: float
    context_boost: float
    final_score: float
    matched_attributes: List[str]
    explanation: str

class OccasionMoodAnalyzer:
    """
    Analyzes and ranks products based on occasion and mood context
    Uses keyword matching, semantic understanding, and contextual rules
    """
    
    def __init__(self):
        logger.info("Initializing Occasion & Mood Analyzer")
        
        # Define occasion-specific keywords and attributes
        self.occasion_keywords = {
            Occasion.WEDDING: {
                "keywords": ["wedding", "bride", "groom", "formal", "elegant", "ceremony", "celebration"],
                "colors": ["white", "ivory", "cream", "pastel", "gold", "silver"],
                "styles": ["elegant", "formal", "sophisticated", "classic", "luxurious"],
                "categories": ["dresses", "suits", "accessories", "jewelry"]
            },
            Occasion.PARTY: {
                "keywords": ["party", "celebration", "festive", "fun", "dance", "night out"],
                "colors": ["bright", "vibrant", "metallic", "sparkle", "bold"],
                "styles": ["trendy", "flashy", "stylish", "modern", "eye-catching"],
                "categories": ["dresses", "shoes", "accessories", "bags"]
            },
            Occasion.BUSINESS: {
                "keywords": ["business", "office", "professional", "work", "corporate", "meeting"],
                "colors": ["black", "navy", "gray", "white", "dark blue", "charcoal"],
                "styles": ["professional", "formal", "classic", "conservative", "tailored"],
                "categories": ["suits", "shirts", "blazers", "pants", "shoes"]
            },
            Occasion.CASUAL: {
                "keywords": ["casual", "everyday", "comfortable", "relaxed", "weekend"],
                "colors": ["any", "neutral", "denim", "earth tones"],
                "styles": ["casual", "comfortable", "relaxed", "simple", "laid-back"],
                "categories": ["jeans", "t-shirts", "sneakers", "casual wear"]
            },
            Occasion.BEACH: {
                "keywords": ["beach", "swim", "summer", "vacation", "resort", "tropical"],
                "colors": ["bright", "tropical", "white", "blue", "coral", "turquoise"],
                "styles": ["casual", "breezy", "light", "summery", "resort"],
                "categories": ["swimwear", "sandals", "sunglasses", "beach wear", "hats"]
            },
            Occasion.SPORT: {
                "keywords": ["sport", "athletic", "gym", "workout", "running", "training", "fitness"],
                "colors": ["any", "bright", "neon", "performance"],
                "styles": ["athletic", "performance", "sporty", "active", "functional"],
                "categories": ["sportswear", "sneakers", "athletic wear", "activewear"]
            },
            Occasion.DATE: {
                "keywords": ["date", "romantic", "dinner", "evening", "special"],
                "colors": ["red", "pink", "black", "romantic", "soft"],
                "styles": ["romantic", "elegant", "stylish", "attractive", "chic"],
                "categories": ["dresses", "shoes", "accessories", "perfume"]
            },
            Occasion.INTERVIEW: {
                "keywords": ["interview", "professional", "job", "formal", "first impression"],
                "colors": ["navy", "black", "gray", "white", "conservative"],
                "styles": ["professional", "conservative", "polished", "formal", "classic"],
                "categories": ["suits", "shirts", "dress shoes", "professional wear"]
            },
            Occasion.FESTIVAL: {
                "keywords": ["festival", "concert", "music", "outdoor", "bohemian"],
                "colors": ["bright", "colorful", "bold", "eclectic", "vibrant"],
                "styles": ["bohemian", "eclectic", "trendy", "casual", "artistic"],
                "categories": ["casual wear", "accessories", "boots", "hats"]
            }
        }
        
        # Define mood-specific attributes
        self.mood_attributes = {
            Mood.CONFIDENT: {
                "keywords": ["bold", "statement", "powerful", "strong", "striking"],
                "colors": ["red", "black", "bold", "deep"],
                "styles": ["bold", "powerful", "statement", "striking"]
            },
            Mood.RELAXED: {
                "keywords": ["comfortable", "casual", "soft", "easy", "laid-back"],
                "colors": ["soft", "neutral", "pastel", "earth tones"],
                "styles": ["comfortable", "relaxed", "casual", "easy"]
            },
            Mood.ELEGANT: {
                "keywords": ["elegant", "sophisticated", "refined", "graceful", "classy"],
                "colors": ["black", "white", "navy", "neutral", "subtle"],
                "styles": ["elegant", "sophisticated", "refined", "classic"]
            },
            Mood.PLAYFUL: {
                "keywords": ["fun", "playful", "colorful", "quirky", "cheerful"],
                "colors": ["bright", "colorful", "vibrant", "fun"],
                "styles": ["playful", "fun", "trendy", "quirky"]
            },
            Mood.PROFESSIONAL: {
                "keywords": ["professional", "polished", "formal", "business", "tailored"],
                "colors": ["navy", "gray", "black", "white", "conservative"],
                "styles": ["professional", "polished", "formal", "tailored"]
            },
            Mood.ROMANTIC: {
                "keywords": ["romantic", "soft", "feminine", "delicate", "lovely"],
                "colors": ["pink", "red", "soft", "pastel", "floral"],
                "styles": ["romantic", "feminine", "soft", "delicate"]
            },
            Mood.ENERGETIC: {
                "keywords": ["energetic", "active", "dynamic", "sporty", "vibrant"],
                "colors": ["bright", "neon", "vibrant", "bold"],
                "styles": ["sporty", "active", "dynamic", "modern"]
            }
        }
        
        # Season-specific attributes
        self.season_attributes = {
            "spring": {
                "keywords": ["spring", "light", "fresh", "blossom", "renewal"],
                "colors": ["pastel", "light", "fresh", "floral", "green", "pink"]
            },
            "summer": {
                "keywords": ["summer", "hot", "sunny", "bright", "vacation"],
                "colors": ["bright", "white", "light", "tropical", "vibrant"]
            },
            "fall": {
                "keywords": ["fall", "autumn", "warm", "cozy", "harvest"],
                "colors": ["orange", "brown", "burgundy", "earth tones", "warm"]
            },
            "winter": {
                "keywords": ["winter", "cold", "warm", "cozy", "holiday"],
                "colors": ["dark", "deep", "rich", "jewel tones", "winter white"]
            }
        }
    
    def parse_context_from_query(self, query: str) -> ContextProfile:
        """
        Parse occasion and mood context from natural language query
        
        Args:
            query: Natural language search query
            
        Returns:
            ContextProfile with detected context
        """
        query_lower = query.lower()
        
        # Detect occasion
        detected_occasion = None
        for occasion, attrs in self.occasion_keywords.items():
            for keyword in attrs["keywords"]:
                if keyword in query_lower:
                    detected_occasion = occasion
                    break
            if detected_occasion:
                break
        
        # Detect mood
        detected_mood = None
        for mood, attrs in self.mood_attributes.items():
            for keyword in attrs["keywords"]:
                if keyword in query_lower:
                    detected_mood = mood
                    break
            if detected_mood:
                break
        
        # Detect season
        detected_season = None
        for season, attrs in self.season_attributes.items():
            for keyword in attrs["keywords"]:
                if keyword in query_lower:
                    detected_season = season
                    break
            if detected_season:
                break
        
        # Detect time of day
        time_of_day = None
        if any(word in query_lower for word in ["evening", "night", "dinner"]):
            time_of_day = "evening"
        elif any(word in query_lower for word in ["morning", "breakfast"]):
            time_of_day = "morning"
        elif any(word in query_lower for word in ["afternoon", "lunch"]):
            time_of_day = "afternoon"
        
        # Detect location type
        location_type = None
        if any(word in query_lower for word in ["beach", "seaside", "coastal"]):
            location_type = "beach"
        elif any(word in query_lower for word in ["outdoor", "outside"]):
            location_type = "outdoor"
        elif any(word in query_lower for word in ["indoor", "inside"]):
            location_type = "indoor"
        
        logger.info(f"Parsed context - Occasion: {detected_occasion}, Mood: {detected_mood}, Season: {detected_season}")
        
        return ContextProfile(
            occasion=detected_occasion,
            mood=detected_mood,
            season=detected_season,
            time_of_day=time_of_day,
            location_type=location_type
        )
    
    def score_product_for_context(
        self,
        product: Dict,
        context: ContextProfile,
        base_similarity: float
    ) -> OccasionScore:
        """
        Score a product based on how well it matches the context
        
        Args:
            product: Product dictionary with title, description, category
            context: User's context profile
            base_similarity: Base CLIP similarity score
            
        Returns:
            OccasionScore with detailed scoring breakdown
        """
        # Start with base relevance
        occasion_boost = 1.0
        mood_boost = 1.0
        context_boost = 1.0
        matched_attributes = []
        
        # Get product text for analysis
        product_text = f"{product.get('title', '')} {product.get('description', '')}".lower()
        product_category = product.get('category', '').lower()
        
        # Score for occasion
        if context.occasion:
            occasion_attrs = self.occasion_keywords.get(context.occasion, {})
            
            # Check keywords
            keyword_matches = sum(1 for kw in occasion_attrs.get("keywords", []) if kw in product_text)
            if keyword_matches > 0:
                occasion_boost *= (1.0 + keyword_matches * 0.1)
                matched_attributes.append(f"occasion_keywords({keyword_matches})")
            
            # Check colors
            color_matches = sum(1 for color in occasion_attrs.get("colors", []) if color in product_text)
            if color_matches > 0:
                occasion_boost *= (1.0 + color_matches * 0.08)
                matched_attributes.append(f"occasion_colors({color_matches})")
            
            # Check styles
            style_matches = sum(1 for style in occasion_attrs.get("styles", []) if style in product_text)
            if style_matches > 0:
                occasion_boost *= (1.0 + style_matches * 0.12)
                matched_attributes.append(f"occasion_styles({style_matches})")
            
            # Check category match
            relevant_categories = occasion_attrs.get("categories", [])
            if any(cat in product_category for cat in relevant_categories):
                occasion_boost *= 1.2
                matched_attributes.append("category_match")
        
        # Score for mood
        if context.mood:
            mood_attrs = self.mood_attributes.get(context.mood, {})
            
            # Check keywords
            keyword_matches = sum(1 for kw in mood_attrs.get("keywords", []) if kw in product_text)
            if keyword_matches > 0:
                mood_boost *= (1.0 + keyword_matches * 0.1)
                matched_attributes.append(f"mood_keywords({keyword_matches})")
            
            # Check colors
            color_matches = sum(1 for color in mood_attrs.get("colors", []) if color in product_text)
            if color_matches > 0:
                mood_boost *= (1.0 + color_matches * 0.08)
                matched_attributes.append(f"mood_colors({color_matches})")
            
            # Check styles
            style_matches = sum(1 for style in mood_attrs.get("styles", []) if style in product_text)
            if style_matches > 0:
                mood_boost *= (1.0 + style_matches * 0.1)
                matched_attributes.append(f"mood_styles({style_matches})")
        
        # Score for season
        if context.season:
            season_attrs = self.season_attributes.get(context.season, {})
            
            keyword_matches = sum(1 for kw in season_attrs.get("keywords", []) if kw in product_text)
            color_matches = sum(1 for color in season_attrs.get("colors", []) if color in product_text)
            
            if keyword_matches > 0 or color_matches > 0:
                context_boost *= (1.0 + (keyword_matches + color_matches) * 0.05)
                matched_attributes.append(f"season_match({keyword_matches + color_matches})")
        
        # Additional contextual boosts
        if context.time_of_day == "evening" and any(word in product_text for word in ["evening", "formal", "elegant"]):
            context_boost *= 1.1
            matched_attributes.append("time_match")
        
        if context.location_type and context.location_type in product_text:
            context_boost *= 1.1
            matched_attributes.append("location_match")
        
        # Cap boosts to prevent extreme values
        occasion_boost = min(occasion_boost, 1.8)
        mood_boost = min(mood_boost, 1.6)
        context_boost = min(context_boost, 1.3)
        
        # Compute final score
        # Combine base similarity with contextual boosts
        final_score = base_similarity * occasion_boost * mood_boost * context_boost
        
        # Generate explanation
        explanation = self._generate_explanation(
            context, matched_attributes, occasion_boost, mood_boost, context_boost
        )
        
        return OccasionScore(
            base_relevance=base_similarity,
            occasion_boost=occasion_boost,
            mood_boost=mood_boost,
            context_boost=context_boost,
            final_score=min(final_score, 1.0),  # Cap at 1.0
            matched_attributes=matched_attributes,
            explanation=explanation
        )
    
    def _generate_explanation(
        self,
        context: ContextProfile,
        matched_attributes: List[str],
        occasion_boost: float,
        mood_boost: float,
        context_boost: float
    ) -> str:
        """Generate human-readable explanation for ranking"""
        parts = []
        
        if context.occasion and occasion_boost > 1.0:
            parts.append(f"Perfect for {context.occasion}")
        
        if context.mood and mood_boost > 1.0:
            parts.append(f"Matches {context.mood} mood")
        
        if context.season and context_boost > 1.0:
            parts.append(f"Great for {context.season}")
        
        if len(matched_attributes) > 3:
            parts.append(f"Strong match ({len(matched_attributes)} attributes)")
        elif len(matched_attributes) > 0:
            parts.append(f"Good match ({len(matched_attributes)} attributes)")
        
        return " • ".join(parts) if parts else "General match"
    
    def rank_products_by_context(
        self,
        products: List[Dict],
        context: ContextProfile,
        base_scores: List[float]
    ) -> List[Tuple[Dict, OccasionScore]]:
        """
        Rank a list of products based on context
        
        Args:
            products: List of product dictionaries
            context: User context profile
            base_scores: List of base similarity scores (same length as products)
            
        Returns:
            List of (product, OccasionScore) tuples, sorted by final score
        """
        scored_products = []
        
        for product, base_score in zip(products, base_scores):
            occasion_score = self.score_product_for_context(product, context, base_score)
            scored_products.append((product, occasion_score))
        
        # Sort by final score
        scored_products.sort(key=lambda x: x[1].final_score, reverse=True)
        
        logger.info(f"Ranked {len(scored_products)} products by context")
        
        return scored_products


# Global instance
_global_occasion_analyzer = None

def get_occasion_analyzer() -> OccasionMoodAnalyzer:
    """Get or create global occasion analyzer instance"""
    global _global_occasion_analyzer
    if _global_occasion_analyzer is None:
        _global_occasion_analyzer = OccasionMoodAnalyzer()
    return _global_occasion_analyzer
