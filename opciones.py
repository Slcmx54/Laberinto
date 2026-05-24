import pygame, config

from configuration.keyAssign import keyAssign

def opciones(eventos):
    config.PANTALLA.fill(config.DARKGRAY)
    pygame.display.set_caption("Opciones")
    
    if config.lang == "es_co":
        import lang.es_co as lang
    elif config.lang == "en_us":
        import lang.en_us as lang
    elif config.lang == "pt_br":
        import lang.pt_br as lang

    keyAssign(eventos)

    TITLE = config.hormuz(60).render(lang.TITLE_OP, True, config.PURPLE)
    TITLE_RECT = TITLE.get_rect(center=(config.ANCHO // 2, 100))

    config.PANTALLA.blit(TITLE, TITLE_RECT)

    MOUSE = pygame.mouse.get_pos()

    BACK = config.banana(50).render(lang.BACK, True, config.PURPLE)
    IDIOMA = config.hormuz(50).render(lang.LANG_CHOOSE, True, config.PURPLE)
    COLOMBIA = config.banana(35).render("ESPAÑOL - COLOMBIA", True, config.PURPLE)
    USA = config.banana(35).render("ENGLISH - UNITED STATES", True, config.PURPLE)

    BACK_RECT = BACK.get_rect(center=(200, config.ALTO - 200))
    IDIOMA_RECT = IDIOMA.get_rect(center=(config.ANCHO // (4/3), 200))
    COLOMBIA_RECT = COLOMBIA.get_rect(center=(config.ANCHO // (4/3), 150 + 100))
    USA_RECT = USA.get_rect(center=(config.ANCHO // (4/3), 150 + 125))

    if BACK_RECT.collidepoint(MOUSE):
        BACK = config.banana(50).render(lang.BACK, True, config.PINK)
    if IDIOMA_RECT.collidepoint(MOUSE):
        IDIOMA = config.hormuz(50).render(lang.LANG_CHOOSE, True, config.PINK)
    if COLOMBIA_RECT.collidepoint(MOUSE):
        COLOMBIA = config.banana(35).render("ESPAÑOL - COLOMBIA", True, config.PINK)
    if USA_RECT.collidepoint(MOUSE):
        USA = config.banana(35).render("ENGLISH - UNITED STATES", True, config.PINK)

    config.PANTALLA.blit(BACK, BACK_RECT)
    config.PANTALLA.blit(IDIOMA, IDIOMA_RECT)
    config.PANTALLA.blit(COLOMBIA, COLOMBIA_RECT)
    config.PANTALLA.blit(USA, USA_RECT)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if COLOMBIA_RECT.collidepoint(evento.pos):
                config.lang = "es_co"
                config.config["lang"] = "es_co"
                config.guardar_config(config.config)
            if USA_RECT.collidepoint(evento.pos):
                config.lang = "en_us"
                config.config["lang"] = "en_us"
                config.guardar_config(config.config)
            if BACK_RECT.collidepoint(evento.pos):
                config.estado = config.estado_anterior
        elif evento.type == pygame.KEYDOWN:
            if evento.key == config.teclas["escape"]:
                config.estado = config.estado_anterior