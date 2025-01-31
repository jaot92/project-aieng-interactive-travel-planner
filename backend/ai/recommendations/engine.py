from collections import defaultdict
from typing import List, Dict, Optional
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class UserProfile:
    def __init__(self):
        """Initialize user profile with empty interests and history"""
        self.interests = defaultdict(int)
        self.visit_history = []
        self.queries = []
        try:
            self.nlp = spacy.load("es_core_news_sm")
        except:
            self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer()
        
    def update_interests(self, query: str) -> None:
        """Update user interests based on their query
        
        Args:
            query: The user's search query or chat message
        """
        self.queries.append(query)
        doc = self.nlp(query.lower())
        
        # Extract relevant keywords (nouns, proper nouns, adjectives)
        keywords = [token.text for token in doc 
                   if token.pos_ in ['NOUN', 'PROPN', 'ADJ']]
        
        # Update interest counts
        for word in keywords:
            self.interests[word] += 1
            
    def add_visited_location(self, location_id: str, rating: Optional[float] = None) -> None:
        """Add a visited location to user history
        
        Args:
            location_id: Unique identifier for the location
            rating: Optional rating given by user (1-5)
        """
        self.visit_history.append({
            'location': location_id,
            'rating': rating
        })
        
    def get_top_interests(self, n: int = 5) -> List[str]:
        """Get user's top n interests based on frequency
        
        Args:
            n: Number of top interests to return
            
        Returns:
            List of top n interests
        """
        sorted_interests = sorted(
            self.interests.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return [interest[0] for interest in sorted_interests[:n]]
        
    def get_recommendations(self, 
                          available_locations: List[Dict],
                          n_recommendations: int = 5) -> List[Dict]:
        """Get personalized location recommendations
        
        Args:
            available_locations: List of location dictionaries with descriptions
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended locations
        """
        if not self.queries:
            # If no history, return random recommendations
            return available_locations[:n_recommendations]
            
        # Create TF-IDF vectors for user history and locations
        user_text = " ".join(self.queries)
        location_texts = [loc['description'] for loc in available_locations]
        all_texts = [user_text] + location_texts
        
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        user_vector = tfidf_matrix[0]
        location_vectors = tfidf_matrix[1:]
        
        # Calculate similarity scores
        similarities = np.dot(location_vectors, user_vector.T).toarray().flatten()
        
        # Get indices of top recommendations
        top_indices = similarities.argsort()[-n_recommendations:][::-1]
        
        return [available_locations[i] for i in top_indices] 