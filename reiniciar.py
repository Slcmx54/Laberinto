import config, jugar, copy

from lvl1 import *

MAPAS = {
    1: mapa1,
    2: mapa2,
    3: mapa3,
    4: mapa4,
    5: mapa5,
    6: mapa6
}

def obtener_mapa(nivel):
    return copy.deepcopy(MAPAS[nivel])

def reiniciar():
    global MAPAS
    jugar.objetos.clear()
    config.OBJETOS_CREADOS = False
    config.INVENTARIO.clear()
    config.HISTORIAL.clear()
    config.JUGADOR_X = 0
    config.JUGADOR_Y = 0
    config.radio_vision = 2
    
    jugar.resistencia(0)

    config.MAPA_ACTUAL = obtener_mapa(config.NIVEL_ACTUAL)

    config.actualizar_radio()

def reiniciar_json():
    CONFIG_DEFAULT = {
        "lang": "es-co",
        "radio_vision": 2,
        "fullscreen": False,
        "fps": 60,
        "primer_inicio" : False,
        "niveles_completados": {
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
            "6": False
        },
        "death_counter": {
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None
        }
    }
    config.guardar_config(CONFIG_DEFAULT)