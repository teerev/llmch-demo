ACTIVIDADES = [
    {
        "titulo": "Asamblea sobre igualdad de género",
        "descripcion": "Charla guiada con estudiantes sobre derechos y respeto.",
    },
    {
        "titulo": "Mural colaborativo",
        "descripcion": "Creación de un mural con mensajes de mujeres de la comunidad escolar.",
    },
    {
        "titulo": "Lectura de biografías",
        "descripcion": "Lectura en clase de mujeres destacadas en ciencia, arte y deporte.",
    },
    {
        "titulo": "Taller de ciencia con referentes",
        "descripcion": "Actividad práctica mostrando aportes de científicas.",
    },
]


def listar_actividades():
    """Devuelve la lista fija de actividades del Día de la Mujer.

    Se retorna una copia superficial para evitar modificaciones accidentales.
    """

    return list(ACTIVIDADES)
