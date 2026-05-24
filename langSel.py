import pygame, sys, os, config

if config.lang == "es_co":
    import lang.es_co as lang
elif config.lang == "en_us":
    import lang.en_us as lang
elif config.lang == "pt_br":
    import lang.pt_br as lang

def langSel(eventos):
    MOUSE = pygame.mouse.get_pos()

    if config.hover_lang == None:
        color_colombia = config.PINK if config.opcion_lang == 0 else config.PURPLE
        color_usa = config.PINK if config.opcion_lang == 1 else config.PURPLE
        color_portugues = config.PINK if config.opcion_lang == 2 else config.PURPLE
    else:
        color_colombia = config.PURPLE
        color_usa = config.PURPLE
        color_portugues = config.PURPLE

    IDIOMA = config.hormuz(100).render("Selecciona el idioma", True, config.PURPLE)
    COLOMBIA = config.banana(85).render("ESPAÑOL - COLOMBIA", True, color_colombia)
    USA = config.banana(85).render("ENGLISH - UNITED STATES", True, color_usa)
    PORTUGUES = config.banana(85).render("PORTUGUES - BRASIL", True, color_portugues)

    IDIOMA_RECT = IDIOMA.get_rect(center=(config.ANCHO // 2, 100))
    COLOMBIA_RECT = COLOMBIA.get_rect(center=(config.ANCHO // 2, (config.ALTO // 2) - 50))
    USA_RECT = USA.get_rect(center=(config.ANCHO // 2, (config.ALTO // 2) + 50))
    PORTUGUES_RECT = PORTUGUES.get_rect(center=(config.ANCHO // 2, (config.ALTO // 2) + 150))

    if IDIOMA_RECT.collidepoint(MOUSE):
        IDIOMA = config.hormuz(100).render("Selecciona el idioma", True, config.PINK)
    elif COLOMBIA_RECT.collidepoint(MOUSE):
        COLOMBIA = config.banana(85).render("ESPAÑOL - COLOMBIA", True, config.PINK)
        config.hover_lang = 0
        config.opcion_lang = 0
    elif USA_RECT.collidepoint(MOUSE):
        USA = config.banana(85).render("ENGLISH - UNITED STATES", True, config.PINK)
        config.hover_lang = 1
        config.opcion_lang = 1
    elif PORTUGUES_RECT.collidepoint(MOUSE):
        PORTUGUES = config.banana(85).render("PORTUGUES - BRASIL", True, config.PINK)
        config.hover_lang = 2
        config.opcion_lang = 2
    else:
        config.hover_lang = None

    config.PANTALLA.blit(IDIOMA, IDIOMA_RECT)
    config.PANTALLA.blit(COLOMBIA, COLOMBIA_RECT)
    config.PANTALLA.blit(USA, USA_RECT)
    config.PANTALLA.blit(PORTUGUES, PORTUGUES_RECT)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if COLOMBIA_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_SPLASH

                config.lang = "es_co"

                config.config["lang"] = "es_co"
                config.config["primer_inicio"] = False

                config.guardar_config(config.config)
            if USA_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_SPLASH

                config.lang = "en_us"

                config.config["lang"] = "en_us"
                config.config["primer_inicio"] = False

                config.guardar_config(config.config)
            if PORTUGUES_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_SPLASH

                config.lang = "pt_br"

                config.config["lang"] = "pt_br"
                config.config["primer_inicio"] = False

                config.guardar_config(config.config)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN or evento.key == config.teclas["s"]:
                if config.opcion_lang != 2:
                    config.opcion_lang += 1
                else:
                    config.opcion_lang = 0
            if evento.key == pygame.K_UP or evento.key == config.teclas["w"]:
                if config.opcion_lang != 0:
                    config.opcion_lang -= 1
                else:
                    config.opcion_lang = 2
            config.opcion_lang = max(0, min(2, config.opcion_lang))
            if evento.key == pygame.K_RETURN:
            
                config.estado = config.ESTADO_SPLASH
                if config.hover_lang == 0:
                    config.lang = "es_co"

                    config.config["lang"] = "es_co"
                if config.hover_lang == 1:
                    config.lang = "en_us"

                    config.config["lang"] = "en_us"
                if config.hover_lang == 2:
                    config.lang = "pt_br"

                    config.config["lang"] = "pt_br"
                config.primer_inicio = False
                config.guardar_config(config.config)
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()