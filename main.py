import pygame, sys, config, reiniciar

from menu import menu, seguro
from jugar import jugar
from opciones import opciones
from howto import howto
from gameover import gameover
from langSel import langSel
from pausa import pausa
from configuration.keyAssign import sel
from lvls import lvl

pygame.init()

icono = pygame.image.load("media/img/char_idle/1.png")
pygame.display.set_icon(icono)

config.splash_start = pygame.time.get_ticks()

def main():
    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar.reiniciar()

        if config.estado == config.ESTADO_SPLASH:
            splash(eventos)
        elif config.estado == config.ESTADO_MENU:
            menu(eventos)
        elif config.estado == config.ESTADO_JUEGO:
            jugar(eventos)
        elif config.estado == config.ESTADO_HOWTO:
            howto(eventos)
        elif config.estado == config.ESTADO_OPTIONS:
            opciones(eventos)
        elif config.estado == config.ESTADO_GAMEOVER:
            gameover(eventos)
        elif config.estado == config.ESTADO_LANG:
            langSel(eventos)
        elif config.estado == config.ESTADO_EXIT:
            seguro(eventos)
        elif config.estado == config.ESTADO_PAUSA:
            pausa(eventos)
        elif config.estado == config.ESTADO_SEL:
            sel(eventos)
        elif config.estado == config.ESTADO_LVL:
            lvl(eventos)

        config.clock.tick(config.config["fps"])

        pygame.display.update()

def splash(eventos):

    config.PANTALLA.fill(config.BLACK)

    logo = config.logo.copy()

    t = pygame.time.get_ticks() - config.splash_start

    if config.splash_phase == "in":
        config.splash_alpha += 5
        if config.splash_alpha >= 255:
            config.splash_alpha = 255
            config.splash_phase = "hold"
            config.hold_start = pygame.time.get_ticks()

    elif config.splash_phase == "hold":
        if pygame.time.get_ticks() - config.hold_start > 2000:
            config.splash_phase = "out"

    elif config.splash_phase == "out":
        config.splash_alpha -= 5
        if config.splash_alpha <= 0:
            creditos(eventos)

    # aplicar alpha
    logo.set_alpha(max(0, min(255, config.splash_alpha)))

    rect = logo.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))
    config.PANTALLA.blit(logo, rect)

    pygame.display.flip()

def creditos(eventos):

    config.PANTALLA.fill(config.BLACK)

    if config.lang == "es_co":
        import lang.es_co as lang
    elif config.lang == "en_us":
        import lang.en_us as lang
    elif config.lang == "pt_br":
        import lang.pt_br as lang

    texto_creditos = f"{lang.MADEBY}{config.nombre_estudiante}"

    font = config.banana(60)
    texto = font.render(texto_creditos, True, config.WHITE)

    texto.set_alpha(config.creditos_alpha)

    rect = texto.get_rect(center=(config.ANCHO // 2, config.ALTO // 2))

    if config.creditos_phase == "in":
        config.creditos_alpha += 5
        if config.creditos_alpha >= 255:
            config.creditos_alpha = 255
            config.creditos_phase = "hold"
            config.creditos_hold = pygame.time.get_ticks()

    elif config.creditos_phase == "hold":
        if pygame.time.get_ticks() - config.creditos_hold > 2500:
            config.creditos_phase = "out"

    elif config.creditos_phase == "out":
        config.creditos_alpha -= 5
        if config.creditos_alpha <= 0:
            config.estado = config.ESTADO_MENU

    config.PANTALLA.blit(texto, rect)

if __name__ == '__main__':
    main()