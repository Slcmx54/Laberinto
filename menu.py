import pygame, sys, os, config

if config.lang == "es_co":
    import lang.es_co as lang
elif config.lang == "en_us":
    import lang.en_us as lang
elif config.lang == "pt_br":
    import lang.pt_br as lang

if not hasattr(config, "menu_salir_started"):
    config.menu_salir_started = True
    config.menu_salir_state = 0
    config.menu_salir_timer = pygame.time.get_ticks()

    config.menu_salir_y = config.ALTO + 300

def menu(eventos):
    if not config.menu_initialized:
        config.menu_start_time = pygame.time.get_ticks()

        config.menu_jugar_y = config.ALTO + 200
        config.menu_howto_x = -300
        config.menu_options_x = config.ANCHO + 300
        config.menu_salir_y = config.ALTO + 500

        config.menu_initialized = True
    now = pygame.time.get_ticks()
    config.PANTALLA.fill(config.DARKGRAY)
    pygame.display.set_caption("Menu")

    dt = config.clock.get_time() / 1000
    speed = 6

    if config.hover_menu == None:
        color_howto = config.PINK if config.opcion_menu == 0 else config.PURPLE
        color_jugar = config.PINK if config.opcion_menu == 1 else config.PURPLE
        color_options = config.PINK if config.opcion_menu == 2 else config.PURPLE
        color_salir = config.PINK if config.opcion_menu == 3 else config.PURPLE
    else:
        color_howto = config.PURPLE
        color_jugar = config.PURPLE
        color_options = config.PURPLE
        color_salir = config.PURPLE

    MOUSE = pygame.mouse.get_pos()
    
    NOMBRE = config.hormuz(150).render(lang.TITLE, True, config.PURPLE)
    NOMBRE_RECT = NOMBRE.get_rect(center=(config.ANCHO // (4/2), 200))
    target_y = config.ALTO - 250
    config.menu_jugar_y = lerp(config.menu_jugar_y, target_y, dt * speed)

    JUGAR = config.banana(85).render(lang.PLAY, True, color_jugar)
    JUGAR_RECT = JUGAR.get_rect(center=(config.ANCHO // 2, config.menu_jugar_y))
    HOWTO = config.banana(85).render(lang.HOWTO, True, color_howto)
    target_x = config.ANCHO // 4
    config.menu_howto_x = lerp(config.menu_howto_x, target_x, dt * speed)

    HOWTO_RECT = HOWTO.get_rect(center=(config.menu_howto_x, config.ALTO - 250))
    OPTIONS = config.banana(85).render(lang.OPTIONS, True, color_options)
    target_x = config.ANCHO * 3 // 4
    config.menu_options_x = lerp(config.menu_options_x, target_x, dt * speed)

    OPTIONS_RECT = OPTIONS.get_rect(center=(config.menu_options_x, config.ALTO - 250))
    SALIR = config.banana(85).render(lang.EXIT, True, color_salir)
    
    if config.menu_salir_state == 0:
        target = config.ALTO - 1
        config.menu_salir_y = lerp(config.menu_salir_y, target, dt * 10)

        if abs(config.menu_salir_y - target) < 2:
            config.menu_salir_state = 1
            config.menu_salir_timer = now
        
    elif config.menu_salir_state == 1:
        if now - config.menu_salir_timer > 5000:
            config.menu_salir_state = 2
    
    elif config.menu_salir_state == 2:
        target = config.ALTO - 150
        config.menu_salir_y = lerp(config.menu_salir_y, target, dt * 3)

    SALIR_RECT = SALIR.get_rect(center=(config.ANCHO // 2, config.menu_salir_y))
    if NOMBRE_RECT.collidepoint(MOUSE):
        NOMBRE = config.hormuz(150).render(lang.TITLE, True, config.PINK)
    elif JUGAR_RECT.collidepoint(MOUSE):
        config.hover_menu = 0
        config.opcion_menu = 1
        JUGAR = config.banana(85).render(lang.PLAY, True, config.PINK)
    elif HOWTO_RECT.collidepoint(MOUSE):
        config.hover_menu = 1
        config.opcion_menu = 0
        HOWTO = config.banana(85).render(lang.HOWTO, True, config.PINK)
    elif OPTIONS_RECT.collidepoint(MOUSE):
        config.hover_menu = 2
        config.opcion_menu = 2
        OPTIONS = config.banana(85).render(lang.OPTIONS, True, config.PINK)
    elif SALIR_RECT.collidepoint(MOUSE):
        config.hover_menu = 3
        config.opcion_menu = 3
        SALIR = config.banana(85).render(lang.EXIT, True, config.PINK)
    else:
        config.hover_menu = None

    config.PANTALLA.blit(NOMBRE, NOMBRE_RECT)
    config.PANTALLA.blit(JUGAR, JUGAR_RECT)
    config.PANTALLA.blit(HOWTO, HOWTO_RECT)
    config.PANTALLA.blit(OPTIONS, OPTIONS_RECT)
    config.PANTALLA.blit(SALIR, SALIR_RECT)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT or evento.key == config.teclas["a"]:
                if config.opcion_menu == 0:
                    config.opcion_menu = 3
                else:
                    config.opcion_menu -= 1
            if evento.key == pygame.K_RIGHT or evento.key == config.teclas["d"]:
                if config.opcion_menu == 3:
                    config.opcion_menu = 0
                else:
                    config.opcion_menu += 1
            if evento.key == pygame.K_UP or evento.key == config.teclas["w"]:
                if config.opcion_menu == 3:
                    config.opcion_menu = 1
                else:
                    OPTACTUAL = config.opcion_menu
                    config.opcion_menu = OPTACTUAL
            if evento.key == pygame.K_DOWN or  evento.key == config.teclas["s"]:
                if config.opcion_menu != 1:
                    config.opcion_menu = 1
                else:
                    config.opcion_menu = 3
            config.opcion_menu = max(0, min(3, config.opcion_menu))
            if evento.key == pygame.K_RETURN:
                if config.opcion_menu == 0:
                    config.estado = config.ESTADO_HOWTO
                if config.opcion_menu == 1:
                    config.estado = config.ESTADO_LVL
                if config.opcion_menu == 2:
                    config.estado_anterior = config.ESTADO_MENU
                    config.estado = config.ESTADO_OPTIONS
                if config.opcion_menu == 3:
                    config.estado_anterior = config.ESTADO_MENU
                    config.estado = config.ESTADO_EXIT
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if JUGAR_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_LVL
            if HOWTO_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_HOWTO
            if OPTIONS_RECT.collidepoint(evento.pos):
                config.estado_anterior = config.ESTADO_MENU
                config.estado = config.ESTADO_OPTIONS
            if SALIR_RECT.collidepoint(evento.pos):
                config.estado_anterior = config.ESTADO_MENU
                config.estado = config.ESTADO_EXIT

opcion = 0
hover = None

def seguro(eventos):
    global opcion, hover

    if config.lang == "es_co":
        import lang.es_co as lang
    elif config.lang == "en_us":
        import lang.en_us as lang
    elif config.lang == "pt_br":
        import lang.pt_br as lang

    config.PANTALLA.fill(config.DARKGRAY)
    if hover == None:
        color_sí = config.RED if opcion == 0 else config.PURPLE
        color_no = config.GREEN if opcion == 1 else config.PURPLE
    else:
        color_sí = config.PURPLE
        color_no = config.PURPLE

    SEGURO = config.banana(85).render(lang.SURE, True, config.PURPLE)
    YES = config.banana(85).render(lang.YES, True, color_sí)
    NO = config.banana(85).render(lang.NO, True, color_no)

    SEGURO_RECT = SEGURO.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
    YES_RECT = YES.get_rect(center=(config.ANCHO // 2 - 100, config.ALTO // 2 + 100))
    NO_RECT = NO.get_rect(center=(config.ANCHO // 2 + 100, config.ALTO // 2 + 100))
    
    if YES_RECT.collidepoint(pygame.mouse.get_pos()):
        hover = "yes"
        YES = config.banana(85).render(lang.YES, True, config.RED)
        opcion = 0
    elif NO_RECT.collidepoint(pygame.mouse.get_pos()):
        hover = "no"
        NO = config.banana(85).render(lang.NO, True, config.GREEN)
        opcion = 1
    else: 
        hover = None

    config.PANTALLA.blit(SEGURO, SEGURO_RECT)
    config.PANTALLA.blit(YES, YES_RECT)
    config.PANTALLA.blit(NO, NO_RECT)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                opcion += 1
            if evento.key == pygame.K_LEFT:
                opcion -= 1
            opcion = max(0, min(1, opcion))
            if evento.key == pygame.K_RETURN:
                if opcion == 0:
                    pygame.quit()
                    sys.exit()
                elif opcion == 1:
                    config.estado = config.estado_anterior
            if evento.key == config.teclas["escape"]:
                config.estado = config.ESTADO_EXIT
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if YES_RECT.collidepoint(evento.pos):
                pygame.quit()
                sys.exit()
            if NO_RECT.collidepoint(evento.pos):
                config.estado = config.estado_anterior

def lerp(a, b, t):
    return a + (b - a) * t