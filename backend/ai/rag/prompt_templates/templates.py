from typing import Optional
from .base import PromptTemplate

class TravelQueryTemplate(PromptTemplate):
    """
    Plantilla para consultas relacionadas con viajes y turismo.
    """
    
    def __init__(self):
        template = """
Por favor, ayuda al usuario con su consulta sobre viajes en Puerto Rico.

Consulta del usuario: {query}

Información relevante del destino:
{context}

Por favor, proporciona una respuesta detallada y útil que:
1. Responda directamente a la consulta del usuario
2. Incluya información específica y relevante del contexto proporcionado
3. Sugiera recomendaciones prácticas cuando sea apropiado
4. Mencione las fuentes de información cuando sea relevante
"""
        super().__init__(template)
        
    def format(self, **kwargs) -> str:
        if not self.validate_inputs(**kwargs):
            raise ValueError("Faltan variables requeridas: 'query' y 'context'")
        return self.template.format(**kwargs)
    
    def get_system_prompt(self) -> Optional[str]:
        return """Eres un experto en turismo y cultura de Puerto Rico. Tu objetivo es proporcionar información precisa, 
útil y culturalmente sensible sobre destinos, historia y experiencias en Puerto Rico. Debes:
- Ser preciso y basarte en hechos
- Respetar y promover la cultura local
- Proporcionar consejos prácticos y relevantes
- Mencionar fuentes cuando sea posible
- Ser amigable y profesional"""

class HistoricalQueryTemplate(PromptTemplate):
    """
    Plantilla para consultas relacionadas con historia y eventos históricos.
    """
    
    def __init__(self):
        template = """
Por favor, ayuda al usuario con su consulta sobre la historia de Puerto Rico.

Consulta del usuario: {query}

Fuentes históricas relevantes:
{context}

Por favor, proporciona una respuesta que:
1. Presente los hechos históricos de manera precisa y cronológica
2. Contextualice los eventos dentro de la historia más amplia de Puerto Rico
3. Cite las fuentes históricas relevantes
4. Explique la importancia o impacto de estos eventos
"""
        super().__init__(template)
        
    def format(self, **kwargs) -> str:
        if not self.validate_inputs(**kwargs):
            raise ValueError("Faltan variables requeridas: 'query' y 'context'")
        return self.template.format(**kwargs)
    
    def get_system_prompt(self) -> Optional[str]:
        return """Eres un historiador experto en la historia de Puerto Rico. Tu objetivo es proporcionar información 
histórica precisa y bien contextualizada. Debes:
- Mantener la objetividad histórica
- Citar fuentes primarias cuando estén disponibles
- Explicar el contexto histórico más amplio
- Conectar eventos pasados con su relevancia actual
- Ser respetuoso al discutir temas históricos sensibles"""

class CulturalQueryTemplate(PromptTemplate):
    """
    Plantilla para consultas relacionadas con cultura, tradiciones y costumbres.
    """
    
    def __init__(self):
        template = """
Por favor, ayuda al usuario con su consulta sobre la cultura de Puerto Rico.

Consulta del usuario: {query}

Información cultural relevante:
{context}

Por favor, proporciona una respuesta que:
1. Explique los aspectos culturales de manera respetuosa y auténtica
2. Proporcione contexto sobre las tradiciones y costumbres
3. Destaque la importancia cultural y significado
4. Mencione cómo los visitantes pueden experimentar o apreciar estos aspectos culturales
"""
        super().__init__(template)
        
    def format(self, **kwargs) -> str:
        if not self.validate_inputs(**kwargs):
            raise ValueError("Faltan variables requeridas: 'query' y 'context'")
        return self.template.format(**kwargs)
    
    def get_system_prompt(self) -> Optional[str]:
        return """Eres un experto en la cultura y tradiciones de Puerto Rico. Tu objetivo es compartir y explicar 
aspectos culturales de manera respetuosa y auténtica. Debes:
- Presentar la información cultural con respeto y autenticidad
- Explicar el significado y la importancia de las tradiciones
- Proporcionar contexto cultural relevante
- Sugerir formas apropiadas de experimentar la cultura
- Ser sensible a aspectos culturales delicados"""
