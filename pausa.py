import pygame, config, reiniciar

if config.lang == "es_co":
    import lang.es_co as lang
elif config.lang == "en_us":
    import lang.en_us as lang
elif config.lang == "pt_br":
    import lang.pt_br as lang

def pausa(eventos):
    config.PANTALLA.blit(config.PAUSA_BACKGROUND, (0, 0))
    config.PANTALLA.blit(config.OVERLAY, (0, 0))

    MOUSE = pygame.mouse.get_pos()

    if config.hover_pausa is None:
        color_menu = config.PINK if config.opcion_pausa == 0 else config.PURPLE
        color_options = config.PINK if config.opcion_pausa == 1 else config.PURPLE
        color_exit = config.PINK if config.opcion_pausa == 2 else config.PURPLE
    else:
        color_menu = config.PURPLE
        color_options = config.PURPLE
        color_exit = config.PURPLE

    titulo = config.hormuz(120).render("PAUSA", True, config.WHITE)
    texto = config.banana(50).render("ESC PARA CONTINUAR", True, config.WHITE)
    MENU = config.banana(85).render("MENU" , True, color_menu)
    OPTIONS = config.banana(85).render(lang.OPTIONS, True, color_options)
    SALIR = config.banana(85).render(lang.EXIT, True, color_exit)

    titulo_rect = titulo.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 - 100))
    texto_rect = texto.get_rect(center=(config.ANCHO // 2, config.ALTO // 2 + 50))
    MENU_RECT = MENU.get_rect(center=(config.ANCHO // (4 / 1), config.ALTO - 100))
    OPTIONS_RECT = OPTIONS.get_rect(center=(config.ANCHO // 2, config.ALTO - 100))
    SALIR_RECT = SALIR.get_rect(center=(config.ANCHO // (4/3), config.ALTO - 100))

    config.hover_pausa = None
    
    if MENU_RECT.collidepoint(MOUSE):
        config.hover_pausa = 0
        MENU = config.banana(85).render("MENU" , True, config.PINK)
        config.opcion_pausa = 0
    elif OPTIONS_RECT.collidepoint(MOUSE):
        config.hover_pausa = 1
        OPTIONS = config.banana(85).render(lang.OPTIONS, True, config.PINK)
        config.opcion_pausa = 1
    elif SALIR_RECT.collidepoint(MOUSE):
        config.hover_pausa = 2
        SALIR = config.banana(85).render(lang.EXIT, True, config.PINK)
        config.opcion_pausa = 2
    else:
        config.hover_pausa = None

    config.PANTALLA.blit(titulo, titulo_rect)
    config.PANTALLA.blit(texto, texto_rect)
    config.PANTALLA.blit(MENU, MENU_RECT)
    config.PANTALLA.blit(OPTIONS, OPTIONS_RECT)
    config.PANTALLA.blit(SALIR, SALIR_RECT)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                config.estado = config.estadoJuegoAnterior
            if evento.key == pygame.K_RIGHT or evento.key == config.teclas["d"]:
                config.opcion_pausa += 1
            if evento.key == pygame.K_LEFT or evento.key == config.teclas["a"]:
                config.opcion_pausa -= 1
            config.opcion_pausa = max(0, min(2, config.opcion_pausa))
            if evento.key == pygame.K_RETURN:
                if config.opcion_pausa == 0:
                    config.estado = config.ESTADO_MENU
                    reiniciar.reiniciar()
                elif config.opcion_pausa == 1:
                    config.estado_anterior = config.ESTADO_PAUSA
                    config.estado = config.ESTADO_OPTIONS
                elif config.opcion_pausa == 2:
                    config.estado_anterior = config.ESTADO_PAUSA
                    config.estado = config.ESTADO_EXIT
            if evento.key == config.teclas["escape"]:
                config.estado = config.estadoJuegoAnterior

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if MENU_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_MENU
                reiniciar.reiniciar()
            if OPTIONS_RECT.collidepoint(evento.pos):
                config.estado_anterior = config.ESTADO_PAUSA
                config.estado = config.ESTADO_OPTIONS
            if SALIR_RECT.collidepoint(evento.pos):
                config.estado_anterior = config.ESTADO_PAUSA
                config.estado = config.ESTADO_EXIT