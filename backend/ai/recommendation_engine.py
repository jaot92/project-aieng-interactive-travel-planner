from collections import defaultdict

class UserProfile:
    def __init__(self):
        self.interests = defaultdict(int)
        
    def update_interests(self, query: str):
        # Lógica básica de NLP para extraer intereses
        keywords = extract_keywords(query)
        for word in keywords:
            self.interests[word] += 1 