from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class PromptTemplate(ABC):
    """
    Clase base abstracta para todas las plantillas de prompts.
    Define la interfaz común que todas las plantillas deben implementar.
    """
    
    def __init__(self, template: str):
        """
        Inicializa la plantilla con un texto base.
        
        Args:
            template (str): El texto base de la plantilla con placeholders
        """
        self.template = template
        
    @abstractmethod
    def format(self, **kwargs) -> str:
        """
        Formatea la plantilla con los valores proporcionados.
        
        Args:
            **kwargs: Variables para formatear la plantilla
            
        Returns:
            str: La plantilla formateada
        """
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> Optional[str]:
        """
        Retorna el prompt del sistema asociado con esta plantilla.
        
        Returns:
            Optional[str]: El prompt del sistema o None si no hay uno
        """
        pass
    
    def validate_inputs(self, **kwargs) -> bool:
        """
        Valida que todos los inputs necesarios estén presentes.
        
        Args:
            **kwargs: Variables a validar
            
        Returns:
            bool: True si todos los inputs necesarios están presentes
        """
        required_vars = self._get_template_variables()
        return all(var in kwargs for var in required_vars)
    
    def _get_template_variables(self) -> set:
        """
        Extrae las variables de la plantilla.
        
        Returns:
            set: Conjunto de nombres de variables en la plantilla
        """
        import re
        # Busca patrones como {variable} en la plantilla
        pattern = r'\{([^}]+)\}'
        return set(re.findall(pattern, self.template))
