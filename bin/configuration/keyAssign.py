import pygame, config

accion_seleccionada = None

def keyAssign(eventos):
    global accion_seleccionada

    if config.lang == "es_co":
        import lang.es_co as lang
    elif config.lang == "en_us":
        import lang.en_us as lang
    elif config.lang == "pt_br":
        import lang.pt_br as lang

    MOUSE = pygame.mouse.get_pos()

    TITLE_KEYA = config.hormuz(70).render(lang.TITLE_KEYA, True, config.PURPLE)

    Arriba = config.banana(85).render(pygame.key.name(config.teclas["w"]).upper(), True, config.PURPLE)
    Abajo = config.banana(85).render(pygame.key.name(config.teclas["s"]).upper(), True, config.PURPLE)
    Izquierda = config.banana(85).render(pygame.key.name(config.teclas["a"]).upper(), True, config.PURPLE)
    Derecha = config.banana(85).render(pygame.key.name(config.teclas["d"]).upper(), True, config.PURPLE)

    TITLE_KEYA_rect = TITLE_KEYA.get_rect(center=(200, 200))
    Arriba_rect = Arriba.get_rect(center=(200, 250))
    Abajo_rect = Abajo.get_rect(center=(200, 350))
    Izquierda_rect = Izquierda.get_rect(center=(100, 350))
    Derecha_rect = Derecha.get_rect(center=(300, 350))

    if Arriba_rect.collidepoint(MOUSE):
        Arriba = config.banana(85).render(pygame.key.name(config.teclas["w"]).upper(), True, config.PINK)
    if Abajo_rect.collidepoint(MOUSE):
        Abajo = config.banana(85).render(pygame.key.name(config.teclas["s"]).upper(), True, config.PINK)
    if Izquierda_rect.collidepoint(MOUSE):
        Izquierda = config.banana(85).render(pygame.key.name(config.teclas["a"]).upper(), True, config.PINK)
    if Derecha_rect.collidepoint(MOUSE):
        Derecha = config.banana(85).render(pygame.key.name(config.teclas["d"]).upper(), True, config.PINK)

    config.PANTALLA.blit(TITLE_KEYA, TITLE_KEYA_rect)
    config.PANTALLA.blit(Arriba, Arriba_rect)
    config.PANTALLA.blit(Abajo, Abajo_rect)
    config.PANTALLA.blit(Izquierda, Izquierda_rect)
    config.PANTALLA.blit(Derecha, Derecha_rect)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if Arriba_rect.collidepoint(evento.pos):
                accion_seleccionada = "w"
                config.estado = config.ESTADO_SEL

            if Abajo_rect.collidepoint(evento.pos):
                accion_seleccionada = "s"
                config.estado = config.ESTADO_SEL

            if Izquierda_rect.collidepoint(evento.pos):
                accion_seleccionada = "a"
                config.estado = config.ESTADO_SEL

            if Derecha_rect.collidepoint(evento.pos):
                accion_seleccionada = "d"
                config.estado = config.ESTADO_SEL

        elif evento.type == pygame.KEYDOWN:
            if accion_seleccionada is not None:
                config.teclas[accion_seleccionada] = evento.key

                accion_seleccionada = None
    return False

def sel(eventos):
    global accion_seleccionada
    config.PANTALLA.blit(config.OVERLAY, (0, 0))

    SEL = config.hormuz(100).render("Presiona una tecla para cambiarla", True, config.WHITE)
    NO = config.hormuz(100).render("Presiona ESC para cancelar", True, config.RED)

    SEL_rect = SEL.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 - 100))
    NO_rect = NO.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 + 100))

    config.PANTALLA.blit(SEL, SEL_rect)
    config.PANTALLA.blit(NO, NO_rect)
    
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                accion_seleccionada = None
                config.estado = config.ESTADO_OPTIONS
                return

            config.teclas[accion_seleccionada] = evento.key
            accion_seleccionada = None
            config.estado = config.ESTADO_OPTIONS