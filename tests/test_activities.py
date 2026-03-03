from womens_day.activities import ACTIVIDADES, listar_actividades


def test_actividades_literal_exacta():
    expected = [
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

    assert ACTIVIDADES == expected


def test_listar_actividades_devuelve_mismo_contenido():
    expected = [
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

    assert listar_actividades() == expected
