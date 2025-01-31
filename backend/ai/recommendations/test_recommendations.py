from engine import UserProfile

def test_recommendation_engine():
    # Crear instancia del perfil de usuario
    user = UserProfile()
    
    # Datos de prueba - Lugares disponibles
    available_locations = [
        {
            "id": "old_san_juan",
            "name": "Viejo San Juan",
            "description": "Centro histórico colonial con arquitectura española, fortalezas y calles empedradas."
        },
        {
            "id": "el_yunque",
            "name": "El Yunque",
            "description": "Bosque tropical lluvioso con senderos, cascadas y vistas panorámicas."
        },
        {
            "id": "flamenco_beach",
            "name": "Playa Flamenco",
            "description": "Hermosa playa con arena blanca y aguas cristalinas en Culebra."
        },
        {
            "id": "arecibo_observatory",
            "name": "Observatorio de Arecibo",
            "description": "Centro científico y astronómico con el radiotelescopio más grande."
        }
    ]
    
    # Probar actualización de intereses
    print("\n1. Probando actualización de intereses:")
    queries = [
        "Me gustaría visitar lugares históricos y arquitectura colonial",
        "Busco actividades al aire libre y naturaleza",
        "¿Hay playas bonitas cerca de San Juan?"
    ]
    
    for query in queries:
        user.update_interests(query)
        print(f"\nQuery: {query}")
        print("Top intereses:", user.get_top_interests(3))
    
    # Probar historial de visitas
    print("\n2. Probando registro de visitas:")
    user.add_visited_location("old_san_juan", rating=4.5)
    user.add_visited_location("el_yunque", rating=5.0)
    print("Historial de visitas:", user.visit_history)
    
    # Probar recomendaciones
    print("\n3. Probando sistema de recomendaciones:")
    recommendations = user.get_recommendations(available_locations, n_recommendations=2)
    print("\nRecomendaciones principales:")
    for rec in recommendations:
        print(f"- {rec['name']}: {rec['description'][:100]}...")

if __name__ == "__main__":
    test_recommendation_engine() 