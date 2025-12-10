"""
Visual Sentiment Analysis for Product Scoring
Analyzes visual features to determine emotional appeal and aesthetic quality
"""

import numpy as np
from PIL import Image
import cv2
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class SentimentCategory(str, Enum):
    """Sentiment categories for visual analysis"""
    VIBRANT = "vibrant"
    CALM = "calm"
    ELEGANT = "elegant"
    ENERGETIC = "energetic"
    LUXURIOUS = "luxurious"
    PLAYFUL = "playful"
    PROFESSIONAL = "professional"
    ROMANTIC = "romantic"

@dataclass
class VisualSentimentScore:
    """Container for visual sentiment analysis results"""
    overall_score: float  # 0-1 overall appeal
    sentiment_category: SentimentCategory
    color_harmony: float
    brightness_score: float
    saturation_score: float
    composition_score: float
    contrast_score: float
    warmth_score: float  # warm vs cool colors
    complexity_score: float
    emotion_scores: Dict[str, float]  # emotion -> score mapping
    
    def to_dict(self) -> Dict:
        return {
            "overall_score": self.overall_score,
            "sentiment_category": self.sentiment_category,
            "color_harmony": self.color_harmony,
            "brightness_score": self.brightness_score,
            "saturation_score": self.saturation_score,
            "composition_score": self.composition_score,
            "contrast_score": self.contrast_score,
            "warmth_score": self.warmth_score,
            "complexity_score": self.complexity_score,
            "emotion_scores": self.emotion_scores
        }

class VisualSentimentAnalyzer:
    """
    Analyzes visual features to compute sentiment and aesthetic scores
    Based on color theory, composition analysis, and psychological associations
    """
    
    def __init__(self):
        logger.info("Initializing Visual Sentiment Analyzer")
        
        # Define emotion-color associations (based on color psychology)
        self.emotion_color_map = {
            "happy": [(255, 255, 0), (255, 200, 0), (255, 150, 0)],  # Yellow, Gold
            "calm": [(100, 150, 200), (150, 200, 220), (180, 220, 240)],  # Blues
            "energetic": [(255, 0, 0), (255, 100, 0), (255, 50, 100)],  # Reds, Orange
            "luxurious": [(50, 0, 50), (100, 0, 100), (139, 0, 139)],  # Purple, Gold
            "romantic": [(255, 192, 203), (255, 105, 180), (255, 20, 147)],  # Pinks
            "professional": [(0, 0, 100), (50, 50, 100), (70, 70, 90)],  # Dark blues, grays
            "playful": [(255, 100, 200), (100, 255, 200), (200, 100, 255)],  # Bright mixed
            "elegant": [(0, 0, 0), (255, 255, 255), (200, 200, 200)]  # Black, white, gray
        }
    
    async def analyze_image(self, image: Image.Image) -> VisualSentimentScore:
        """
        Perform comprehensive visual sentiment analysis on an image
        
        Args:
            image: PIL Image to analyze
            
        Returns:
            VisualSentimentScore with detailed analysis
        """
        # Convert to numpy array and different color spaces
        img_array = np.array(image)
        
        # Ensure RGB format
        if len(img_array.shape) == 2:  # Grayscale
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:  # RGBA
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # Analyze different aspects
        color_harmony = self._analyze_color_harmony(img_array)
        brightness = self._analyze_brightness(img_array)
        saturation = self._analyze_saturation(img_array)
        composition = self._analyze_composition(img_array)
        contrast = self._analyze_contrast(img_array)
        warmth = self._analyze_warmth(img_array)
        complexity = self._analyze_complexity(img_array)
        
        # Compute emotion scores
        emotion_scores = self._compute_emotion_scores(img_array)
        
        # Determine primary sentiment category
        sentiment_category = self._determine_sentiment_category(emotion_scores)
        
        # Compute overall aesthetic score
        overall_score = self._compute_overall_score(
            color_harmony, brightness, saturation, composition,
            contrast, warmth, complexity
        )
        
        return VisualSentimentScore(
            overall_score=overall_score,
            sentiment_category=sentiment_category,
            color_harmony=color_harmony,
            brightness_score=brightness,
            saturation_score=saturation,
            composition_score=composition,
            contrast_score=contrast,
            warmth_score=warmth,
            complexity_score=complexity,
            emotion_scores=emotion_scores
        )
    
    def _analyze_color_harmony(self, img: np.ndarray) -> float:
        """Analyze color harmony using HSV color space"""
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        
        # Get dominant colors
        pixels = hsv.reshape(-1, 3)
        hues = pixels[:, 0]
        
        # Calculate hue distribution
        hist, _ = np.histogram(hues, bins=36, range=(0, 180))
        hist = hist / hist.sum()
        
        # Harmony based on complementary and analogous colors
        # Lower entropy in hue distribution = better harmony
        entropy = -np.sum(hist * np.log(hist + 1e-10))
        max_entropy = np.log(36)
        
        # Normalize: lower entropy = higher harmony
        harmony_score = 1 - (entropy / max_entropy)
        
        return float(harmony_score)
    
    def _analyze_brightness(self, img: np.ndarray) -> float:
        """Analyze overall brightness/luminance"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Calculate mean brightness (0-255)
        mean_brightness = np.mean(gray)
        
        # Optimal brightness around 127, normalize to 0-1
        # Penalize very dark or very bright images
        optimal = 127
        deviation = abs(mean_brightness - optimal)
        brightness_score = 1 - (deviation / optimal)
        
        return float(max(0, brightness_score))
    
    def _analyze_saturation(self, img: np.ndarray) -> float:
        """Analyze color saturation"""
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        saturation = hsv[:, :, 1]
        
        mean_saturation = np.mean(saturation)
        
        # Normalize to 0-1 (saturation is 0-255 in OpenCV)
        saturation_score = mean_saturation / 255.0
        
        return float(saturation_score)
    
    def _analyze_composition(self, img: np.ndarray) -> float:
        """Analyze composition using rule of thirds and balance"""
        height, width = img.shape[:2]
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        
        # Divide into rule of thirds grid
        h_third = height // 3
        w_third = width // 3
        
        # Calculate edge density in each grid cell
        grid_scores = []
        for i in range(3):
            for j in range(3):
                cell = edges[i*h_third:(i+1)*h_third, j*w_third:(j+1)*w_third]
                density = np.sum(cell) / (h_third * w_third * 255)
                grid_scores.append(density)
        
        # Good composition has balanced edge distribution
        grid_scores = np.array(grid_scores)
        std_dev = np.std(grid_scores)
        
        # Lower std dev = better balance
        composition_score = 1 / (1 + std_dev * 10)
        
        return float(composition_score)
    
    def _analyze_contrast(self, img: np.ndarray) -> float:
        """Analyze image contrast"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Calculate standard deviation as contrast measure
        contrast = np.std(gray)
        
        # Normalize (typical range 0-100)
        contrast_score = min(contrast / 50.0, 1.0)
        
        return float(contrast_score)
    
    def _analyze_warmth(self, img: np.ndarray) -> float:
        """Analyze color temperature (warm vs cool)"""
        # Calculate average red vs blue ratio
        red = img[:, :, 0].astype(float)
        blue = img[:, :, 2].astype(float)
        
        avg_red = np.mean(red)
        avg_blue = np.mean(blue)
        
        # Warmth: 0 = cool (blue), 1 = warm (red)
        if avg_red + avg_blue == 0:
            warmth = 0.5
        else:
            warmth = avg_red / (avg_red + avg_blue)
        
        return float(warmth)
    
    def _analyze_complexity(self, img: np.ndarray) -> float:
        """Analyze visual complexity"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Use edge density and texture as complexity measures
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1] * 255)
        
        # Calculate texture using Laplacian variance
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_variance = laplacian.var()
        
        # Combine measures
        complexity = (edge_density + min(texture_variance / 1000, 1.0)) / 2
        
        return float(complexity)
    
    def _compute_emotion_scores(self, img: np.ndarray) -> Dict[str, float]:
        """Compute scores for different emotions based on color analysis"""
        emotion_scores = {}
        
        # Get dominant colors
        pixels = img.reshape(-1, 3)
        
        for emotion, color_palette in self.emotion_color_map.items():
            scores = []
            
            for target_color in color_palette:
                target = np.array(target_color)
                
                # Calculate color distances
                distances = np.linalg.norm(pixels - target, axis=1)
                
                # Count pixels close to target color (within threshold)
                threshold = 100
                close_pixels = np.sum(distances < threshold)
                
                # Normalize by total pixels
                score = close_pixels / len(pixels)
                scores.append(score)
            
            # Emotion score is max of palette colors
            emotion_scores[emotion] = float(max(scores))
        
        # Normalize scores
        max_score = max(emotion_scores.values()) if emotion_scores else 1.0
        if max_score > 0:
            emotion_scores = {k: v/max_score for k, v in emotion_scores.items()}
        
        return emotion_scores
    
    def _determine_sentiment_category(self, emotion_scores: Dict[str, float]) -> SentimentCategory:
        """Determine primary sentiment category from emotion scores"""
        if not emotion_scores:
            return SentimentCategory.CALM
        
        # Map emotions to sentiment categories
        emotion_to_category = {
            "happy": SentimentCategory.VIBRANT,
            "calm": SentimentCategory.CALM,
            "energetic": SentimentCategory.ENERGETIC,
            "luxurious": SentimentCategory.LUXURIOUS,
            "romantic": SentimentCategory.ROMANTIC,
            "professional": SentimentCategory.PROFESSIONAL,
            "playful": SentimentCategory.PLAYFUL,
            "elegant": SentimentCategory.ELEGANT
        }
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        return emotion_to_category.get(dominant_emotion, SentimentCategory.CALM)
    
    def _compute_overall_score(
        self,
        color_harmony: float,
        brightness: float,
        saturation: float,
        composition: float,
        contrast: float,
        warmth: float,
        complexity: float
    ) -> float:
        """
        Compute overall aesthetic appeal score
        Weights are based on visual design principles
        """
        weights = {
            "color_harmony": 0.25,
            "composition": 0.20,
            "contrast": 0.15,
            "brightness": 0.15,
            "saturation": 0.10,
            "complexity": 0.10,
            "warmth": 0.05
        }
        
        overall = (
            weights["color_harmony"] * color_harmony +
            weights["composition"] * composition +
            weights["contrast"] * contrast +
            weights["brightness"] * brightness +
            weights["saturation"] * saturation +
            weights["complexity"] * complexity +
            weights["warmth"] * warmth
        )
        
        return float(overall)
    
    def compute_sentiment_boost(
        self,
        sentiment_score: VisualSentimentScore,
        user_preference: Optional[str] = None
    ) -> float:
        """
        Compute a ranking boost based on sentiment analysis
        
        Args:
            sentiment_score: Visual sentiment analysis result
            user_preference: Optional user preference for sentiment ("vibrant", "calm", etc.)
            
        Returns:
            Boost multiplier (0.8 to 1.2)
        """
        # Base boost from overall aesthetic score
        base_boost = 0.8 + (sentiment_score.overall_score * 0.4)
        
        # Additional boost if matches user preference
        if user_preference and sentiment_score.sentiment_category == user_preference:
            base_boost *= 1.15
        
        return min(1.2, max(0.8, base_boost))
