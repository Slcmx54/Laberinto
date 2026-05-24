import pygame, config, jugar, copy

from lvl1 import *

if config.lang == "es_co":
    import lang.es_co as lang
elif config.lang == "en_us":
    import lang.en_us as lang
elif config.lang == "pt_br":
    import lang.pt_br as lang

lvlUnc = pygame.image.load("media/lvls/lvlUnc.png").convert_alpha()
lvl1_img = pygame.image.load("media/lvls/lvl1-completed.png").convert_alpha()
lvl2_img = pygame.image.load("media/lvls/lvl2-completed.png").convert_alpha()
lvl3_img = pygame.image.load("media/lvls/lvl3-completed.png").convert_alpha()
lvl4_img = pygame.image.load("media/lvls/lvl4-completed.png").convert_alpha()
lvl5_img = pygame.image.load("media/lvls/lvl5-completed.png").convert_alpha()
lvl6_img = pygame.image.load("media/lvls/lvl6-completed.png").convert_alpha()

ANCHO_LVL = config.ANCHO // 3 - 80
ALTO_LVL = config.ALTO // 3

lvlUnc = pygame.transform.scale(lvlUnc, (ANCHO_LVL, ALTO_LVL))

imagenes = [
    pygame.transform.scale(lvl1_img, (ANCHO_LVL, ALTO_LVL)),
    pygame.transform.scale(lvl2_img, (ANCHO_LVL, ALTO_LVL)),
    pygame.transform.scale(lvl3_img, (ANCHO_LVL, ALTO_LVL)),
    pygame.transform.scale(lvl4_img, (ANCHO_LVL, ALTO_LVL)),
    pygame.transform.scale(lvl5_img, (ANCHO_LVL, ALTO_LVL)),
    pygame.transform.scale(lvl6_img, (ANCHO_LVL, ALTO_LVL))
]

mapas = [
    mapa1,
    mapa2,
    mapa3,
    mapa4,
    mapa5,
    mapa6
]

rects = []

POR_FILA = 3

ESPACIO_X = 40
ESPACIO_Y = 50

x_inicial = 80
y_inicial = 120

for i, imagen in enumerate(imagenes):
    fila = i // POR_FILA
    columna = i % POR_FILA

    x = x_inicial + columna * (ANCHO_LVL + ESPACIO_X)
    y = y_inicial + fila * (ALTO_LVL + ESPACIO_Y)

    rect = imagen.get_rect(topleft=(x, y))
    rects.append(rect)


def cargar_nivel(numero):
    config.NIVEL_ACTUAL = numero
    config.MAPA_ACTUAL = copy.deepcopy(mapas[numero - 1])
    config.JUGADOR_X = 0
    config.JUGADOR_Y = 0
    config.INVENTARIO.clear()
    config.HISTORIAL.clear()
    jugar.objetos.clear()
    config.OBJETOS_CREADOS = False
    config.actualizar_radio()
    config.estado = config.ESTADO_JUEGO

def lvl(eventos):
    config.PANTALLA.fill(config.DARKGRAY)

    mouse = pygame.mouse.get_pos()

    ATRAS = config.banana(85).render(lang.BACK, True, config.PURPLE)
    ATRAS_RECT = ATRAS.get_rect(center=(config.ANCHO // 2, config.ALTO - 50))

    if ATRAS_RECT.collidepoint(mouse):
        ATRAS = config.banana(85).render(lang.BACK, True, config.PINK)

    config.PANTALLA.blit(ATRAS, ATRAS_RECT)

    for i, rect in enumerate(rects, start=1):
        completado = config.config["niveles_completados"][str(i)]
        desbloqueado = False

        if i == 1:
            desbloqueado = True

        elif config.config["niveles_completados"][str(i - 1)]:
            desbloqueado = True

        if completado:
            config.PANTALLA.blit(imagenes[i - 1], rect)
            config.PANTALLA.blit(config.banana(30).render(f"Nivel {i}", True, (255, 255, 255)), (rect.x + 10, rect.y + 10))
            if config.config["death_counter"][str(i)] is not None:
                contador = config.config["death_counter"][str(i)]
                contador_texto = config.banana(30).render(f"Muertes: {contador}", True, (255, 255, 255))
                contador_rect = contador_texto.get_rect(bottomleft=(rect.x + 10, rect.bottom - 10))
                config.PANTALLA.blit(contador_texto, contador_rect)
            else:
                contador = config.config["death_counter"][str(i)]
                contador_texto = config.banana(30).render(f"Muertes:", True, (255, 255, 255))
                contador_rect = contador_texto.get_rect(bottomleft=(rect.x + 10, rect.bottom - 10))
                config.PANTALLA.blit(contador_texto, contador_rect)


        elif desbloqueado:
            config.PANTALLA.blit(lvlUnc, rect)
            texto = config.banana(30).render("JUGAR", True, (255, 255, 255))
            texto_rect = texto.get_rect(center=rect.center)
            config.PANTALLA.blit(texto, texto_rect)

        else:
            config.PANTALLA.blit(lvlUnc, rect)

        config.hover_lvls = any(rect.collidepoint(mouse) for rect in rects)

        if rect.collidepoint(mouse):
            config.hover_lvls = True
            pygame.draw.rect(config.PANTALLA, config.PURPLE, rect.inflate(10, 10), 4, border_radius=12)
            config.opcion_lvls = i - 1
        elif not config.hover_lvls and config.opcion_lvls == i - 1:
            pygame.draw.rect(config.PANTALLA, config.PURPLE, rect.inflate(14, 14), 4, border_radius=12)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(rects, start=1):
                desbloqueado = False
                if i == 1:
                    desbloqueado = True
                elif config.config["niveles_completados"][str(i - 1)]:
                    desbloqueado = True
                if rect.collidepoint(evento.pos):
                    if desbloqueado:
                        cargar_nivel(i)
            if ATRAS_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_MENU

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                config.opcion_lvls += 1
            if evento.key == pygame.K_LEFT:
                config.opcion_lvls -= 1
            if evento.key == pygame.K_UP:
                config.opcion_lvls -= 3
            if evento.key == pygame.K_DOWN:
                config.opcion_lvls += 3
            config.opcion_lvls = max(0, min(5, config.opcion_lvls))
            if evento.key == pygame.K_RETURN:
                cargar_nivel(config.opcion_lvls + 1)
            if evento.key == config.teclas["escape"]:
                config.estado = config.ESTADO_MENU