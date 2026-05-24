import pygame, sys, os, config, animation

if config.lang == "es_co":
    import lang.es_co as lang
elif config.lang == "en_us":
    import lang.en_us as lang
elif config.lang == "pt_br":
    import lang.pt_br as lang

def howto(eventos):
    config.PANTALLA.fill(config.BLACK)
    
    MOUSE = pygame.mouse.get_pos()
    
    COMO_JUGAR = config.banana(100).render(lang.HOWTO, True, config.PURPLE)
    MOVE = config.banana(50).render(lang.MOVE, True, config.WHITE)
    moveInfo = config.banana(30).render(lang.MOVE_INFO, True, config.PURPLE)
    CAPTURE = config.banana(50).render(lang.CAPTURE, True, config.WHITE)
    captureInfo = config.banana(30).render(lang.CAPTURE_INFO, True, config.PURPLE)
    GOAL = config.banana(50).render(lang.GOAL, True, config.WHITE)
    goalInfo = config.banana(30).render(lang.GOAL_INFO, True, config.PURPLE)
    DEATH = config.banana(50).render(lang.DEATH, True, config.WHITE)
    deathInfo = config.banana(30).render(lang.DEATH_INFO, True, config.PURPLE)
    ATRAS = config.banana(60).render(lang.BACK, True, config.PURPLE)

    COMO_JUGAR_RECT = COMO_JUGAR.get_rect(center=(config.ANCHO // 2, config.ALTO // 8))
    MOVE_RECT = MOVE.get_rect(topleft=(200, config.ALTO // (8/2)))
    moveInfo_rect = moveInfo.get_rect(topleft=(200, config.ALTO // (8/2) + MOVE_RECT.height))
    CAPTURE_RECT = CAPTURE.get_rect(topleft=(200, config.ALTO // (8/3)))
    captureInfo_rect = captureInfo.get_rect(topleft=(200, config.ALTO // (8/3) + CAPTURE_RECT.height))
    GOAL_RECT = GOAL.get_rect(topleft=(200, config.ALTO // (8/4)))
    goalInfo_rect = goalInfo.get_rect(topleft=(200, config.ALTO // (8/4) + GOAL_RECT.height))
    DEATH_RECT = DEATH.get_rect(topleft=(200, config.ALTO // (8/5)))
    deathInfo_rect = deathInfo.get_rect(topleft=(200, config.ALTO // (8/5) + DEATH_RECT.height))
    ATRAS_RECT = ATRAS.get_rect(center=(config.ANCHO // (6/2), config.ALTO // (8/7)))

    if ATRAS_RECT.collidepoint(MOUSE):
        ATRAS = config.banana(60).render(lang.BACK, True, config.PINK)
    if MOVE_RECT.collidepoint(MOUSE):
        config.PANTALLA.blit(moveInfo, moveInfo_rect)
        MOVE = config.banana(50).render(lang.MOVE, True, config.PINK)
        animation.move_howto.actualizar()
        animation.move_howto.dibujar(config.PANTALLA, config.ANCHO//2, 200)
    if CAPTURE_RECT.collidepoint(MOUSE):
        config.PANTALLA.blit(captureInfo, captureInfo_rect)
        CAPTURE = config.banana(50).render(lang.CAPTURE, True, config.PINK)
        animation.capture_howto.actualizar()
        animation.capture_howto.dibujar(config.PANTALLA, config.ANCHO//2, 200)
    if GOAL_RECT.collidepoint(MOUSE):
        config.PANTALLA.blit(goalInfo, goalInfo_rect)
        GOAL = config.banana(50).render(lang.GOAL, True, config.PINK)
        animation.goal_howto.actualizar()
        animation.goal_howto.dibujar(config.PANTALLA, config.ANCHO//2, 200)
    if DEATH_RECT.collidepoint(MOUSE):
        config.PANTALLA.blit(deathInfo, deathInfo_rect)
        DEATH = config.banana(50).render(lang.DEATH, True, config.PINK)
        animation.death_howto.actualizar()
        animation.death_howto.dibujar(config.PANTALLA, config.ANCHO//2, 200)

    config.PANTALLA.blit(COMO_JUGAR, COMO_JUGAR_RECT)
    config.PANTALLA.blit(MOVE, MOVE_RECT)
    config.PANTALLA.blit(CAPTURE, CAPTURE_RECT)
    config.PANTALLA.blit(GOAL, GOAL_RECT)
    config.PANTALLA.blit(DEATH, DEATH_RECT)
    config.PANTALLA.blit(ATRAS, ATRAS_RECT)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if ATRAS_RECT.collidepoint(evento.pos):
                config.estado = config.ESTADO_MENU
        elif evento.type == pygame.KEYDOWN:
            if evento.key == config.teclas["escape"]:
                config.estado = config.ESTADO_MENU