import requests
import time
import json
from typing import List, Dict

class BlogLLMEvaluator:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        
    def evaluate_generation_speed(self, test_topics: List[str]) -> Dict:
        """Evaluate generation speed across different topics"""
        results = []
        
        for topic in test_topics:
            start_time = time.time()
            
            response = requests.post(f"{self.api_url}/generate-blog", json={
                "topic": topic,
                "word_count": 500
            })
            
            if response.status_code == 200:
                data = response.json()
                results.append({
                    "topic": topic,
                    "generation_time": data["generation_time"],
                    "word_count": data["word_count"],
                    "words_per_second": data["word_count"] / data["generation_time"]
                })
        
        return {
            "average_time": sum(r["generation_time"] for r in results) / len(results),
            "average_words_per_second": sum(r["words_per_second"] for r in results) / len(results),
            "results": results
        }
    
    def evaluate_content_quality(self, topic: str) -> Dict:
        """Basic content quality metrics"""
        response = requests.post(f"{self.api_url}/generate-blog", json={
            "topic": topic,
            "word_count": 500
        })
        
        if response.status_code == 200:
            content = response.json()["content"]
            
            # Basic metrics
            words = content.split()
            sentences = content.split('.')
            paragraphs = content.split('\n\n')
            
            return {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "avg_words_per_sentence": len(words) / max(len(sentences), 1),
                "readability_score": self.calculate_readability(content),
                "has_title": content.startswith('#'),
                "has_sections": '##' in content
            }
    
    def calculate_readability(self, text: str) -> float:
        """Simple readability score (lower is better)"""
        words = text.split()
        sentences = text.split('.')
        avg_sentence_length = len(words) / max(len(sentences), 1)
        return min(avg_sentence_length / 15, 1.0)  # Normalize to 0-1

if __name__ == "__main__":
    evaluator = BlogLLMEvaluator()
    
    test_topics = [
        "artificial intelligence in healthcare",
        "sustainable energy solutions",
        "remote work productivity tips"
    ]
    
    print("🔍 Evaluating Blog LLM Performance...")
        
    # Speed evaluation
    speed_results = evaluator.evaluate_generation_speed(test_topics)
    print(f"Average generation time: {speed_results['average_time']:.2f} seconds")
    print(f"Average words per second: {speed_results['average_words_per_second']:.2f}")
    
    # Quality evaluation
    quality_results = evaluator.evaluate_content_quality(test_topics[0])
    print(f"Content quality metrics: {quality_results}")