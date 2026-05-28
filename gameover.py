import pygame, config, reiniciar

from lvl1 import *

from jugar import objetos

def gameover(eventos):

    MOUSE = pygame.mouse.get_pos()
    
    if config.lang == "es_co":
        import lang.es_co as lang
    elif config.lang == "en_us":
        import lang.en_us as lang
    elif config.lang == "pt_br":
        import lang.pt_br as lang

    if config.WIN: 
        config.PANTALLA.fill(config.BLACK)

        if config.hover_gameover is None:
            color_atras = config.PINK if config.opcion_gameover == 0 else config.PURPLE
            color_reboot = config.PINK if config.opcion_gameover == 1 else config.PURPLE
            color_siguiente = config.PINK if config.opcion_gameover == 2 else config.PURPLE
        else:
            color_atras = config.PURPLE
            color_reboot = config.PURPLE
            color_siguiente = config.PURPLE
        
        GANASTE = config.banana(200).render(lang.WINNER, True, config.PURPLE)
        REBOOT = config.banana(60).render(lang.RESTART, True, color_reboot)
        ATRAS = config.banana(60).render(lang.BACK, True, color_atras)
        SIGUIENTE = config.banana(60).render(lang.NEXT, True, color_siguiente)
        FINALIZADO = config.banana(60).render(lang.THEEND, True, color_siguiente)
        TOTAL = config.banana(60).render(f"{config.NIVEL_ACTUAL} / 6", True, config.PURPLE)

        GANASTE_RECT = GANASTE.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
        REBOOT_RECT = REBOOT.get_rect(center=(config.ANCHO // (6/4), (config.ALTO // 2) + 200))
        ATRAS_RECT = ATRAS.get_rect(center=(config.ANCHO // (6/2), (config.ALTO // 2) + 200))
        SIGUIENTE_RECT = SIGUIENTE.get_rect(center=(config.ANCHO // 2, config.ALTO - 75))
        FINALIZADO_RECT = FINALIZADO.get_rect(center=(config.ANCHO // 2, config.ALTO - 75))
        TOTAL_RECT = TOTAL.get_rect(center=(config.ANCHO // 2, 100))

        if REBOOT_RECT.collidepoint(MOUSE):
            config.hover_gameover = 1
            REBOOT = config.banana(60).render(lang.RESTART, True, config.PINK)
            config.opcion_gameover = 1
        elif ATRAS_RECT.collidepoint(MOUSE):
            config.hover_gameover = 0
            ATRAS = config.banana(60).render(lang.BACK, True, config.PINK)
            config.opcion_gameover = 0
        elif SIGUIENTE_RECT.collidepoint(MOUSE):
            config.hover_gameover = 2
            SIGUIENTE = config.banana(60).render(lang.NEXT, True, config.PINK)
            config.opcion_gameover = 2
        else:
            config.hover_gameover = None

        config.PANTALLA.blit(GANASTE, GANASTE_RECT)
        config.PANTALLA.blit(REBOOT, REBOOT_RECT)
        config.PANTALLA.blit(ATRAS, ATRAS_RECT)
        config.PANTALLA.blit(TOTAL, TOTAL_RECT)
        if config.NIVEL_ACTUAL < 6:
            config.PANTALLA.blit(SIGUIENTE, SIGUIENTE_RECT)
        if config.NIVEL_ACTUAL > 6:
            config.PANTALLA.blit(FINALIZADO, FINALIZADO_RECT)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if REBOOT_RECT.collidepoint(evento.pos):
                    config.estado = config.ESTADO_JUEGO
                    reiniciar.reiniciar()
                    config.opcion_gameover = 1
                    config.DEATH_COUNTER = 0
                if ATRAS_RECT.collidepoint(evento.pos):
                    config.estado = config.ESTADO_MENU
                    reiniciar.reiniciar()
                    config.opcion_gameover = 1
                    config.DEATH_COUNTER = 0
                if SIGUIENTE_RECT.collidepoint(evento.pos):
                    siguiente_nivel()
                    config.WIN = False
                    config.estado = config.ESTADO_JUEGO
                    config.DEATH_COUNTER = 0
                    config.opcion_gameover = 0
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT or evento.key == config.teclas["d"]:
                    config.opcion_gameover = 1
                if evento.key == pygame.K_LEFT or evento.key == config.teclas["a"]:
                    config.opcion_gameover = 0
                if evento.key == pygame.K_DOWN or evento.key == config.teclas["s"] and config.NIVEL_ACTUAL < 6:
                    config.opcion_gameover = 2
                if evento.key == pygame.K_UP or evento.key == config.teclas["w"] and config.NIVEL_ACTUAL < 6:
                    config.opcion_gameover = 0
                if config.NIVEL_ACTUAL < 6:
                    config.opcion_gameover = max(0, min(2, config.opcion_gameover))
                else:
                    config.opcion_gameover = max(0, min(1, config.opcion_gameover))
                if evento.key == config.teclas["enter"]:
                    if config.opcion_gameover == 0:
                        config.estado = config.ESTADO_JUEGO
                        reiniciar.reiniciar()
                        config.opcion_gameover = 0
                        config.DEATH_COUNTER = 0
                    elif config.opcion_gameover == 1:
                        config.estado = config.ESTADO_MENU
                        reiniciar.reiniciar()
                        config.opcion_gameover = 0
                        config.DEATH_COUNTER = 0
                    elif config.opcion_gameover == 2 and config.NIVEL_ACTUAL < 6:
                        siguiente_nivel()
                        config.WIN = False
                        config.estado = config.ESTADO_JUEGO
                        config.DEATH_COUNTER = 0
                        config.opcion_gameover = 0

    if not config.WIN:
        config.PANTALLA.fill(config.BLACK)

        if config.hover_gameover is None:
            color_atras = config.PINK if config.opcion_gameover == 0 else config.PURPLE
            color_reboot = config.PINK if config.opcion_gameover == 1 else config.PURPLE
        else:
            color_atras = config.PURPLE
            color_reboot = config.PURPLE

        MOUSE = pygame.mouse.get_pos()
        
        PERDISTE = config.banana(200).render(lang.LOSER, True, config.PURPLE)
        REBOOT = config.banana(60).render(lang.RESTART, True, color_reboot)
        ATRAS = config.banana(60).render(lang.BACK, True, color_atras)
        TOTAL = config.banana(60).render(f"{config.NIVEL_ACTUAL} / 6", True, config.PURPLE)

        PERDISTE_RECT = PERDISTE.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
        REBOOT_RECT = REBOOT.get_rect(center=(config.ANCHO // (6/4), (config.ALTO // 2) + 200))
        ATRAS_RECT = ATRAS.get_rect(center=(config.ANCHO // (6/2), (config.ALTO // 2) + 200))
        TOTAL_RECT = TOTAL.get_rect(center=(config.ANCHO // 2, 100))

        if REBOOT_RECT.collidepoint(MOUSE):
            config.hover_gameover = 1
            REBOOT = config.banana(60).render(lang.RESTART, True, config.PINK)
            config.opcion_gameover = 1
        elif ATRAS_RECT.collidepoint(MOUSE):
            config.hover_gameover = 0
            ATRAS = config.banana(60).render(lang.BACK, True, config.PINK)
            config.opcion_gameover = 0
        else:
            config.hover_gameover = None

        config.PANTALLA.blit(PERDISTE, PERDISTE_RECT)        
        config.PANTALLA.blit(REBOOT, REBOOT_RECT)
        config.PANTALLA.blit(ATRAS, ATRAS_RECT)
        config.PANTALLA.blit(TOTAL, TOTAL_RECT)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if REBOOT_RECT.collidepoint(evento.pos):
                    config.estado = config.ESTADO_JUEGO
                    reiniciar.reiniciar()
                    config.opcion_gameover = 0
                if ATRAS_RECT.collidepoint(evento.pos):
                    config.estado = config.ESTADO_MENU
                    reiniciar.reiniciar()
                    config.opcion_gameover = 0
                    config.DEATH_COUNTER = 0
            if evento.type == pygame.KEYDOWN:
                if evento.key == config.teclas["escape"]:
                    config.estado = config.ESTADO_MENU
                    reiniciar.reiniciar()
                    config.opcion_gameover = 0
                if evento.key == pygame.K_RIGHT or evento.key == config.teclas["d"]:
                    config.opcion_gameover = 1
                if evento.key == pygame.K_LEFT or evento.key == config.teclas["a"]:
                    config.opcion_gameover = 0
                config.opcion_gameover = max(0, min(1, config.opcion_gameover))
                if evento.key == config.teclas["enter"]:
                    if config.opcion_gameover == 0:
                        config.estado = config.ESTADO_JUEGO
                        reiniciar.reiniciar()
                        config.opcion_gameover = 0
                    elif config.opcion_gameover == 1:
                        config.estado = config.ESTADO_MENU
                        reiniciar.reiniciar()
                        config.opcion_gameover = 0
                        config.DEATH_COUNTER = 0

def siguiente_nivel():

    config.NIVEL_ACTUAL += 1

    if config.NIVEL_ACTUAL == 2:
        config.MAPA_ACTUAL = config.obtener_mapa(2)

    elif config.NIVEL_ACTUAL == 3:
        config.MAPA_ACTUAL = config.obtener_mapa(3)

    elif config.NIVEL_ACTUAL == 4:
        config.MAPA_ACTUAL = config.obtener_mapa(4)

    elif config.NIVEL_ACTUAL == 5:
        config.MAPA_ACTUAL = config.obtener_mapa(5)

    elif config.NIVEL_ACTUAL == 6:
        config.MAPA_ACTUAL = config.obtener_mapa(6)

    else:
        config.estado = "gameover"
        config.WIN = True
        return

    objetos.clear()
    config.OBJETOS_CREADOS = False

    config.INVENTARIO.clear()

    config.JUGADOR_X = 0
    config.JUGADOR_Y = 0

    config.HISTORIAL = [(0, 0)]

    config.radio_vision = 2