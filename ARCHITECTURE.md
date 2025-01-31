# Arquitectura del Sistema

## Módulos Principales

### 1. Procesamiento de Datos
- `landmark_processor.py`: Extracción y normalización de datos de puntos de interés
- `news_preprocessor.py`: Chunking y embedding de artículos históricos

### 2. Núcleo AI
- `rag_system.py`: Sistema de recuperación aumentada
- `function_router.py`: Enrutador de funciones para el agente

### 3. Backend API
- `chat_router.py`: Endpoints para la interacción con el chatbot
- `map_services.py`: Integración con Mapbox para visualización

### 4. Frontend
- Componente Chat: Interfaz conversacional básica
- Mapa Interactivo: Visualización de ubicaciones sugeridas 