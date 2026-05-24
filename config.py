import pygame, os, json, copy

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
    
pygame.init()

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

CONFIG_FILE = "configuration/config.json"

def cargar_config():

    if os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)

        for clave, valor in CONFIG_DEFAULT.items():
            if clave not in config:
                config[clave] = valor

        return config

    with open(CONFIG_FILE, "w", encoding="utf-8") as archivo:
        json.dump(CONFIG_DEFAULT, archivo, indent=4)

    return CONFIG_DEFAULT

def guardar_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as archivo:
        json.dump(config, archivo, indent=4)

config = cargar_config()

clock = pygame.time.Clock()

info = pygame.display.Info()

ANCHO, ALTO = info.current_w, info.current_h

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))

PANEL_IZQUIERDO = ANCHO * 0.25
PANEL_DERECHO = ANCHO - PANEL_IZQUIERDO

TAMAÑO_CELDA = PANEL_DERECHO // 13

OFFSET = TAMAÑO_CELDA * 0.05

PANEL_ABAJO_IZQUIERDA = (0, ALTO - 100)

ESTADO_SPLASH = "splash"
ESTADO_MENU = "menu"
ESTADO_JUEGO = "juego"
ESTADO_PAUSA = "pausa"
ESTADO_HOWTO = "howto"
ESTADO_OPTIONS = "opciones"
ESTADO_GAMEOVER = "gameover"
ESTADO_LANG = "lang"
ESTADO_EXIT = "exit"
ESTADO_SEL = "sel"
ESTADO_LVL = "lvl"

estadoJuegoAnterior = ESTADO_JUEGO
estado_anterior = estadoJuegoAnterior

if config["primer_inicio"]:
    estado = ESTADO_LANG
else:
    estado = ESTADO_SPLASH

#COLORES
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
DARKPINK = (199, 21, 133)
LIGHTPINK = (255, 20, 147)
DARKGRAY = (30, 30, 30)
ORANGE = (255, 165, 0)
DARKRED = (139, 0, 0)

def get_font(font, size):
    return pygame.font.SysFont(font, size)

HORMUZ = "font/Hormuz.otf"
BANANA = "font/Banana.otf"

def hormuz(size):
    return pygame.font.Font(HORMUZ, size)

def banana(size):
    return pygame.font.Font(BANANA, size)

JUGADOR_Y = 0
JUGADOR_X = 0

HISTORIAL = [(JUGADOR_X, JUGADOR_Y)]

TAMAÑO_OBJETOS = 90

FILAS = 9   
COLUMNAS = 13

OFFSET_X = PANEL_IZQUIERDO + OFFSET
OFFSET_Y = (ALTO - (FILAS * TAMAÑO_CELDA)) // 2

WIN = False

OBJETOS_CREADOS = False

INVENTARIO = []

lang = config["lang"]

OVERLAY = pygame.Surface((ANCHO, ALTO))
OVERLAY.set_alpha(180)
OVERLAY.fill((0, 0, 0))

PAUSA_BACKGROUND = None

DEATH_COUNTER = 0
BEST_DEATHS = None

teclas = {
    "enter": pygame.K_RETURN,
    "escape": pygame.K_ESCAPE,
    "space": pygame.K_SPACE,
    "r": pygame.K_r,
    "o": pygame.K_o,
    "h": pygame.K_h,
    "m": pygame.K_m,
    "q": pygame.K_q,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "w": pygame.K_w,
    "s": pygame.K_s,
    "a": pygame.K_a,
    "d": pygame.K_d,
}

opcion_menu = 1
hover_menu = None

opcion_pausa = 0
hover_pausa = None

opcion_lvl = 1
hover_lvl = None

opcion_lang = 0
hover_lang = None

opcion_lvls = 0
hover_lvls = False

opcion_gameover = 0
hover_gameover = None

opcion_salir = 1

MAPA_ACTUAL = obtener_mapa(1)
NIVEL_ACTUAL = 1

def actualizar_radio():
    global radio_vision

    if NIVEL_ACTUAL == 6:
        radio_vision = 1
    else:
        radio_vision = config["radio_vision"]

radio_vision = config["radio_vision"] if NIVEL_ACTUAL != 6 else 1

CORAZON = pygame.image.load("media/img/CORAZÓN.png").convert_alpha()

splash_start = pygame.time.get_ticks()
logo = pygame.image.load("media/logo.png").convert_alpha()

splash_phase = "in"
splash_alpha = 0

nombre_estudiante = "Salomé Cáliz"

texto_creditos = ""
texto_ing = "Ingeniería Informática"
creditos_alpha = 0
creditos_phase = "in"
creditos_start = pygame.time.get_ticks()

menu_start_time = 0

menu_jugar_y = 0
menu_howto_x = 0
menu_options_x = 0

menu_salir_state = 0
menu_salir_timer = 0
menu_salir_y = 0

menu_initialized = False

OBJETOS_NIVELES = {

    1: [
        ("media/img/LLAVEA.png", (4, 0), "LLAVEA"),
        ("media/img/LLAVEV.png", (5, 8), "LLAVEV"),
        ("media/img/LLAVER.png", (8, 1), "LLAVER"),

        ("media/img/COFREA-C.png", (0, 4), "COFREA", "LLAVEA"),
        ("media/img/COFREV-C.png", (10, 6), "COFREV", "LLAVEV"),
        ("media/img/COFRER-C.png", (3, 8), "COFRER", "LLAVER")
    ],

    2: [
        ("media/img/LLAVEA.png", (2, 2), "LLAVEA"),
        ("media/img/LLAVEV.png", (9, 6), "LLAVEV"),
        ("media/img/LLAVER.png", (12, 0), "LLAVER"),

        ("media/img/COFREA-C.png", (5, 4), "COFREA", "LLAVEA"),
        ("media/img/COFREV-C.png", (0, 8), "COFREV", "LLAVEV"),
        ("media/img/COFRER-C.png", (12, 8), "COFRER", "LLAVER")
    ],

    3: [
        ("media/img/LLAVEA.png", (0, 8), "LLAVEA"),
        ("media/img/LLAVEV.png", (2, 4), "LLAVEV"),
        ("media/img/LLAVER.png", (7, 2), "LLAVER"),

        ("media/img/COFREA-C.png", (12, 8), "COFREA", "LLAVEA"),
        ("media/img/COFREV-C.png", (11, 1), "COFREV", "LLAVEV"),
        ("media/img/COFRER-C.png", (6, 1), "COFRER", "LLAVER")
    ],
    4: [
        ("media/img/LLAVEA.png", (8, 7), "LLAVEA"),
        ("media/img/LLAVEV.png", (4, 4), "LLAVEV"),
        ("media/img/LLAVER.png", (6, 5), "LLAVER"),

        ("media/img/COFREA-C.png", (10, 8), "COFREA", "LLAVEA"),
        ("media/img/COFREV-C.png", (0, 8), "COFREV", "LLAVEV"),
        ("media/img/COFRER-C.png", (12, 8), "COFRER", "LLAVER")
    ],
    5: [
        ("media/img/LLAVEA.png", (12, 0), "LLAVEA"),
        ("media/img/LLAVEV.png", (10, 2), "LLAVEV"),
        ("media/img/LLAVER.png", (14, 0), "LLAVER"),

        ("media/img/COFREA-C.png", (2, 0), "COFREA", "LLAVEA"),
        ("media/img/COFREV-C.png", (4, 2), "COFREV", "LLAVEV"),
        ("media/img/COFRER-C.png", (14, 8), "COFRER", "LLAVER")
    ],
    6: [
        ("media/img/LLAVEA.png", (2, 0), "LLAVEA"),
        ("media/img/LLAVEV.png", (12, 0), "LLAVEV"),
        ("media/img/LLAVER.png", (14, 0), "LLAVER"),

        ("media/img/COFREA-C.png", (0, 4), "COFREA", "LLAVEA"),
        ("media/img/COFREV-C.png", (0, 8), "COFREV", "LLAVEV"),
        ("media/img/COFRER-C.png", (14, 0), "COFRER", "LLAVER")
    ],
}

NIVELES_COMPLETADOS = {
    "1": False,
    "2": False,
    "3": False,
    "4": False,
    "5": False,
    "6": False
}