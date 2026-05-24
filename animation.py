import pygame, os, config

class Animacion:
    def __init__(self, carpeta, velocidad=0.15, escala=None, flip=False):
        self.flip = flip
        self.frames = []

        archivos = sorted(os.listdir(carpeta))

        for archivo in archivos:
            ruta = os.path.join(carpeta, archivo)

            imagen = pygame.image.load(ruta).convert_alpha()
            imagen = pygame.transform.flip(imagen, flip, False)

            if escala:
                imagen = pygame.transform.scale(imagen, escala)

            self.frames.append(imagen)

        self.frame_actual = 0
        self.velocidad = velocidad

    def actualizar(self):
        self.frame_actual += self.velocidad

        if self.frame_actual >= len(self.frames):
            self.frame_actual = 0

    def dibujar(self, pantalla, x, y):

        imagen = self.frames[int(self.frame_actual)]

        pantalla.blit(imagen, (x, y))


e1_idle = Animacion("media/img/e1_idle", velocidad=0.01, escala=(config.TAMAÑO_CELDA + 20, config.TAMAÑO_CELDA + 20), flip=True)
e2_idle = Animacion("media/img/e2_idle", velocidad=0.01, escala=(config.TAMAÑO_CELDA + 20, config.TAMAÑO_CELDA + 20), flip=True)
e3_idle = Animacion("media/img/e3_idle", velocidad=0.01, escala=(config.TAMAÑO_CELDA + 20, config.TAMAÑO_CELDA + 20), flip=True)

e1_dead = Animacion("media/img/e1_dead", velocidad=0.01, escala=(config.TAMAÑO_CELDA + 20, config.TAMAÑO_CELDA + 20), flip=True)
e2_dead = Animacion("media/img/e2_dead", velocidad=0.01, escala=(config.TAMAÑO_CELDA + 20, config.TAMAÑO_CELDA + 20), flip=True)
e3_dead = Animacion("media/img/e3_dead", velocidad=0.01, escala=(config.TAMAÑO_CELDA + 20, config.TAMAÑO_CELDA + 20), flip=True)

char_idle = Animacion("media/img/char_idle", velocidad=0.1, escala=(config.TAMAÑO_CELDA, config.TAMAÑO_CELDA))
char_dead = Animacion("media/img/char_dead", velocidad=0.1, escala=(config.TAMAÑO_CELDA, config.TAMAÑO_CELDA))

char_Big = Animacion("media/img/char_idle", velocidad=0.1, escala=(config.PANEL_IZQUIERDO - 80, config.PANEL_IZQUIERDO - 80))

move_howto = Animacion("media/videos/move", velocidad=0.08, escala=(config.ANCHO - 800, config.ALTO - 400))
capture_howto = Animacion("media/videos/capture", velocidad=0.05, escala=(config.ANCHO - 800, config.ALTO - 400))
goal_howto = Animacion("media/videos/goal", velocidad=0.04, escala=(config.ANCHO - 800, config.ALTO - 400))
death_howto = Animacion("media/videos/die", velocidad=0.04, escala=(config.ANCHO - 800, config.ALTO - 400))