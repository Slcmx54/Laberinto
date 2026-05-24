import pygame, sys, config, animation, reiniciar

from lvl1 import *

if config.lang == "es_co":
    import lang.es_co as lang
elif config.lang == "en_us":
    import lang.en_us as lang
elif config.lang == "pt_br":
    import lang.pt_br as lang

def jugar(eventos):
    global nivel

    config.PANTALLA.fill(config.DARKGRAY)
    pygame.display.set_caption("JUGANDO")
    config.JUGADOR_X = max(0, min(config.JUGADOR_X, 12))
    config.JUGADOR_Y = max(0, min(config.JUGADOR_Y, 8))

    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    pygame.draw.line(config.PANTALLA, config.DARKPINK, (config.PANEL_IZQUIERDO, 0), (config.PANEL_IZQUIERDO, config.ALTO), 5)

    laberinto(config.PANTALLA, config.TAMAÑO_CELDA)

    containers()

    teclas(eventos)

    objectCONT(config.TAMAÑO_OBJETOS, config.YELLOW)

    if not config.OBJETOS_CREADOS:

        for datos in config.OBJETOS_NIVELES[config.NIVEL_ACTUAL]:
            if len(datos) == 3:
                img, pos, tipo = datos[:3]
                
                objetos.append(objeto(img, config.TAMAÑO_CELDA, pos, tipo))

            elif len(datos) == 4:
                img, pos, tipo, requiere = datos

                objetos.append(objeto(img, config.TAMAÑO_CELDA, pos, tipo, requiere))        

        config.OBJETOS_CREADOS = True
    
    for o in objetos:
        if o.tipo.startswith("LLAVE"):
            if o.obtenido:
                continue

        col, fila = o.grid_pos

        distancia_x = abs(col - config.JUGADOR_X)
        distancia_y = abs(fila - config.JUGADOR_Y)

        if distancia_x <= config.radio_vision and distancia_y <= config.radio_vision:
            o.dibujar(config.PANTALLA)
        elif o.tipo == "CORAZON":
            o.dibujar(config.PANTALLA)

    jugador(config.PANTALLA)
    resistencia(0)

    texto_contador = config.banana(30).render(f"{lang.DEATHS}: {config.DEATH_COUNTER}", True, config.WHITE)
    texto_contador_rect = texto_contador.get_rect(topleft=(20, 20))

    config.PANTALLA.blit(texto_contador, texto_contador_rect)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP or evento.key == config.teclas["w"]:
                mover_jugador(0, -1)
            if evento.key == pygame.K_DOWN or evento.key == config.teclas["s"]:
                mover_jugador(0, 1)
            if evento.key == pygame.K_LEFT or evento.key == config.teclas["a"]:
                mover_jugador(-1, 0)
            if evento.key == pygame.K_RIGHT or evento.key == config.teclas["d"]:
                mover_jugador(1, 0)
            if config.MAPA_ACTUAL[config.JUGADOR_Y][config.JUGADOR_X] == 2:
                nivel = str(config.NIVEL_ACTUAL)

                config.NIVELES_COMPLETADOS[config.NIVEL_ACTUAL] = True
                config.config["niveles_completados"][nivel] = True

                best = config.config["death_counter"].get(nivel)

                if best is None or config.DEATH_COUNTER < best:
                    config.config["death_counter"][nivel] = config.DEATH_COUNTER

                config.guardar_config(config.config)

                config.estado = "gameover"
                config.WIN = True
            if evento.key == pygame.K_r:
                reiniciar.reiniciar()
            if evento.key == pygame.K_ESCAPE:
                config.PAUSA_BACKGROUND = config.PANTALLA.copy()
                config.ESTADO_ANTERIOR = config.ESTADO_JUEGO
                config.estado = config.ESTADO_PAUSA
                break

    animation.char_Big.actualizar()
    animation.char_Big.dibujar(config.PANTALLA, 50, 50)
    
    pygame.display.flip()

def laberinto(pantalla, tamaño):
    for f in range(config.FILAS):
        for c in range(config.COLUMNAS):

            distancia_x = abs(c - config.JUGADOR_X)
            distancia_y = abs(f - config.JUGADOR_Y)

            if distancia_x <= config.radio_vision and distancia_y <= config.radio_vision:

                x, y = grid_to_pixel(c, f)

                rect = pygame.Rect(x, y, tamaño, tamaño)

                if config.MAPA_ACTUAL[f][c] == 0:
                    pygame.draw.rect(pantalla, config.YELLOW, rect, 2, border_radius=12)
                if config.MAPA_ACTUAL[f][c] == 1:
                    pygame.draw.rect(pantalla, config.DARKPINK, rect, border_radius=12)
                    pygame.draw.rect(pantalla, config.BLACK, rect, 2, border_radius=12)
                if config.MAPA_ACTUAL[f][c] == 2:
                    pygame.draw.rect(pantalla, config.GREEN, rect, border_radius=12)
                if config.MAPA_ACTUAL[f][c] == 3:
                    #pygame.draw.rect(pantalla, config.ORANGE, rect, border_radius=12)
                    pygame.draw.rect(pantalla, config.YELLOW, rect, 2, border_radius=12)
                    animation.e1_idle.actualizar()
                    animation.e1_idle.dibujar(pantalla, x - 10, y)
                    corazonEn((c, f))
                if config.MAPA_ACTUAL[f][c] == 4:
                    #pygame.draw.rect(pantalla, config.RED, rect, border_radius=12)
                    pygame.draw.rect(pantalla, config.YELLOW, rect, 2, border_radius=12)
                    animation.e2_idle.actualizar()
                    animation.e2_idle.dibujar(pantalla, x - 10, y)
                    corazonEn((c - 0.1, f))
                    corazonEn((c + 0.1, f))
                if config.MAPA_ACTUAL[f][c] == 5:
                    #pygame.draw.rect(pantalla, config.DARKRED, rect, border_radius=12)
                    pygame.draw.rect(pantalla, config.YELLOW, rect, 2, border_radius=12)
                    animation.e3_idle.actualizar()
                    animation.e3_idle.dibujar(pantalla, x - 10, y)
                    corazonEn((c, f))
                    corazonEn((c + 0.2, f))
                    corazonEn((c - 0.2, f))

def dispJugador(tamaño, x, y):
    x = 80
    y = 80
    pygame.draw.rect(config.PANTALLA, config.RED, (x, y, tamaño - x, tamaño - y))

def jugador(pantalla):

    x, y = grid_to_pixel(config.JUGADOR_X - 1, config.JUGADOR_Y - 1)

    x += config.TAMAÑO_CELDA
    y += config.TAMAÑO_CELDA

    #pygame.draw.rect(pantalla, color, (x, y, tamaño, tamaño), border_radius=10)
    animation.char_idle.actualizar()
    animation.char_idle.dibujar(pantalla, x, y)

class objeto:
    def __init__(self, imagen, tamaño, grid_pos, tipo, requiere=None):
        self.tamaño = tamaño
        self.grid_pos = grid_pos
        self.tipo = tipo
        self.requiere = requiere
        self.obtenido = False
        self.estado = "cerrado"

        self.imagenes = {
            "cerrado": pygame.transform.scale(
                pygame.image.load(imagen).convert_alpha(),
                (int(tamaño * 0.8), int(tamaño * 0.8))
            )
        }

        self.imagen = self.imagenes["cerrado"]

    def dibujar(self, pantalla):
        columna, fila = self.grid_pos
        x, y = grid_to_pixel(columna, fila)
        pantalla.blit(self.imagen, (x + 2, y))
        
    def cambiar_estado(self, estado):

        self.estado = estado

        if self.tipo == "COFREA":

            rutas = {
                "cerrado": "media/img/COFREA-C.png",
                "contenido": "media/img/COFREA-CON.png",
                "abierto": "media/img/COFREA-A.png"
            }

        elif self.tipo == "COFREV":

            rutas = {
                "cerrado": "media/img/COFREV-C.png",
                "contenido": "media/img/COFREV-CON.png",
                "abierto": "media/img/COFREV-A.png"
            }

        elif self.tipo == "COFRER":

            rutas = {
                "cerrado": "media/img/COFRER-C.png",
                "contenido": "media/img/COFRER-CON.png",
                "abierto": "media/img/COFRER-A.png"
            }

        imagen = pygame.image.load(rutas[estado]).convert_alpha()

        self.imagen = pygame.transform.scale(imagen, (int(self.tamaño * 0.8), int(self.tamaño * 0.8)))

objetos = []

def posiciones():
    pass

def grid_to_pixel(columna, fila):

    x = config.OFFSET_X + columna * config.TAMAÑO_CELDA
    y = config.OFFSET_Y + fila * config.TAMAÑO_CELDA

    return x, y

def hayPared(col, fila):
    if (
        fila < 0 or
        fila >= len(config.MAPA_ACTUAL) or
        col < 0 or
        col >= len(config.MAPA_ACTUAL[0])
    ):
        return True

    return config.MAPA_ACTUAL[fila][col] == 1

def enemigo(col, fila):

    valor = config.MAPA_ACTUAL[fila][col]

    enemigos = {
        3: "COFREA",
        4: "COFREV",
        5: "COFRER"
    }

    if valor in enemigos:
        return enemigos[valor]

    return None

def mover_jugador(dx, dy):
    for obj in objetos:
        if obj.tipo == "COFREA" and obj.obtenido:
            if config.NIVEL_ACTUAL == 6:
                config.radio_vision = 1
            else:
                config.radio_vision = 3
            break

    nuevo_x = config.JUGADOR_X + dx
    nuevo_y = config.JUGADOR_Y + dy

    if hayPared(nuevo_x, nuevo_y):
        return

    requiere = enemigo(nuevo_x, nuevo_y)

    if requiere:
        if requiere not in config.INVENTARIO:
            config.estado = "gameover"
            config.DEATH_COUNTER += 1
            return
        else:
            config.MAPA_ACTUAL[nuevo_y][nuevo_x] = 0

    obj = obtenerObjeto(nuevo_x, nuevo_y)

    if obj:

        if obj.requiere:
            if obj.requiere not in config.INVENTARIO:
                return

        if obj.tipo not in config.INVENTARIO:
            config.INVENTARIO.append(obj.tipo)

        obj.obtenido = True
    
        if obj.tipo == "LLAVEA":
            for c in objetos:
                if c.tipo == "COFREA":
                    c.cambiar_estado("contenido")

        if obj.tipo == "LLAVEV":
            for c in objetos:
                if c.tipo == "COFREV":
                    c.cambiar_estado("contenido")

        if obj.tipo == "LLAVER":
            for c in objetos:
                if c.tipo == "COFRER":
                    c.cambiar_estado("contenido")

        if obj.tipo == "COFREA" and obj.obtenido == True:
            obj.cambiar_estado("abierto")

        if obj.tipo == "COFREV" and obj.obtenido == True:
            obj.cambiar_estado("abierto")

        if obj.tipo == "COFRER" and obj.obtenido == True:
            obj.cambiar_estado("abierto")

    config.JUGADOR_X = nuevo_x
    config.JUGADOR_Y = nuevo_y

    config.HISTORIAL.append((nuevo_x, nuevo_y))

def obtenerObjeto(col, fila):
    for o in objetos:
        if o.grid_pos == (col, fila):
            if o.tipo.startswith("LLAVE") and o.obtenido == True:
                continue
            if o.tipo == "COFREA" and o.obtenido == True:
                continue
            return o
    return None

def objectCONT(tamaño, color):
    posiciones = {
        "LLAVEA": (
            (config.PANEL_IZQUIERDO - tamaño) // (4/1) - 40,
            config.ALTO // 2
        ),

        "LLAVEV": (
            (config.PANEL_IZQUIERDO - tamaño) // (4/2),
            config.ALTO // 2
        ),

        "LLAVER": (
            (config.PANEL_IZQUIERDO - tamaño) // (4/3) + 40,
            config.ALTO // 2
        ),

        "COFREA": (
            (config.PANEL_IZQUIERDO - tamaño) // (4/1) - 40,
            config.ALTO // 2 + tamaño + 20
        ),

        "COFREV": (
            (config.PANEL_IZQUIERDO - tamaño) // (4/2),
            config.ALTO // 2 + tamaño + 20
        ),

        "COFRER": (
            (config.PANEL_IZQUIERDO - tamaño) // (4/3) + 40,
            config.ALTO // 2 + tamaño + 20
        )
    }

    for obj in objetos:

        if obj.obtenido:
            x, y = posiciones[obj.tipo]
            
            nombre = obj.tipo
            nameObj = obj.tipo
            if nombre == "COFREA":
                nameObj = "LAMP"
            elif nombre == "COFREV":
                nameObj = "SWORD"
            elif nombre == "COFRER":
                nameObj = "SHIELD"

            cofrev_obtenido = any(
                o.tipo == "COFREV" and o.obtenido
                for o in objetos
            )

            if nombre == "COFREA" and not cofrev_obtenido:
                image = pygame.image.load("media/img/LAMP.png")
                image = pygame.transform.scale(image, (tamaño - 20, tamaño - 20))

                image2 = pygame.image.load("media/img/KNIVE.png")
                image2 = pygame.transform.scale(image2, (tamaño - 20, tamaño - 20))
                image2 = pygame.transform.rotate(image2, 90)
                
                if config.NIVEL_ACTUAL == 6:
                    config.PANTALLA.blit(image2, (x + 10, y + 10))
                else:
                    config.PANTALLA.blit(image2, (x + 10, y + 10))
                    config.PANTALLA.blit(image, (x + 10, y + 10))
            else:
                image = pygame.image.load(f"media/img/{nameObj}.png")
                image = pygame.transform.scale(image, (tamaño - 20, tamaño - 20))

                image_rect = image.get_rect(center=(x + tamaño // 2, y + tamaño // 2))

                config.PANTALLA.blit(image, image_rect)

def regresar_movimiento():
    if len(config.HISTORIAL) > 1:
        config.HISTORIAL.pop()
        x, y = config.HISTORIAL[-1]
        config.JUGADOR_X = x
        config.JUGADOR_Y = y

def resistencia(cantidad):

    heart = pygame.image.load("media/img/CORAZÓN.png").convert_alpha()
    heart = pygame.transform.scale(heart, (config.TAMAÑO_OBJETOS - 40, config.TAMAÑO_OBJETOS - 40))

    cantidad = 0

    for o in objetos:
        if o.tipo == "COFREA" and o.obtenido:
            cantidad = 1

        if o.tipo == "COFREV" and o.obtenido:
            cantidad = 2

        if o.tipo == "COFRER" and o.obtenido:
            cantidad = 3

    for i in range(cantidad):
        config.PANTALLA.blit(heart, (config.PANEL_IZQUIERDO - 75, 130 + (i * 50)))

def containers():
    pygame.draw.rect(config.PANTALLA, config.DARKPINK, ((config.PANEL_IZQUIERDO - config.TAMAÑO_OBJETOS) // (4/1) - 40, config.ALTO //2, config.TAMAÑO_OBJETOS, config.TAMAÑO_OBJETOS), border_radius=12)
    pygame.draw.rect(config.PANTALLA, config.DARKPINK, ((config.PANEL_IZQUIERDO - config.TAMAÑO_OBJETOS) // (4/2), config.ALTO //2, config.TAMAÑO_OBJETOS, config.TAMAÑO_OBJETOS), border_radius=12)
    pygame.draw.rect(config.PANTALLA, config.DARKPINK, ((config.PANEL_IZQUIERDO - config.TAMAÑO_OBJETOS) // (4/3) + 40, config.ALTO //2, config.TAMAÑO_OBJETOS, config.TAMAÑO_OBJETOS), border_radius=12)
    pygame.draw.rect(config.PANTALLA, config.DARKPINK, ((config.PANEL_IZQUIERDO - config.TAMAÑO_OBJETOS) // (4/1) - 40, config.ALTO //2 + 110, config.TAMAÑO_OBJETOS, config.TAMAÑO_OBJETOS), border_radius=12)
    pygame.draw.rect(config.PANTALLA, config.DARKPINK, ((config.PANEL_IZQUIERDO - config.TAMAÑO_OBJETOS) // (4/2), config.ALTO //2 + 110, config.TAMAÑO_OBJETOS, config.TAMAÑO_OBJETOS), border_radius=12)
    pygame.draw.rect(config.PANTALLA, config.DARKPINK, ((config.PANEL_IZQUIERDO - config.TAMAÑO_OBJETOS) // (4/3) + 40, config.ALTO //2 + 110, config.TAMAÑO_OBJETOS, config.TAMAÑO_OBJETOS), border_radius=12)

def teclas(eventos):
    MOUSE = pygame.mouse.get_pos()

    Arriba = config.banana(85).render(pygame.key.name(config.teclas["w"]).upper(), True, config.PURPLE)
    Abajo = config.banana(85).render(pygame.key.name(config.teclas["s"]).upper(), True, config.PURPLE)
    Izquierda = config.banana(85).render(pygame.key.name(config.teclas["a"]).upper(), True, config.PURPLE)
    Derecha = config.banana(85).render(pygame.key.name(config.teclas["d"]).upper(), True, config.PURPLE)

    centro = config.PANEL_IZQUIERDO // 2

    Arriba_rect = Arriba.get_rect(center=(centro, config.ALTO - 130))
    Abajo_rect = Abajo.get_rect(center=(centro, config.ALTO - 80))
    Izquierda_rect = Izquierda.get_rect(center=(centro - 100, config.ALTO - 80))
    Derecha_rect = Derecha.get_rect(center=(centro + 100, config.ALTO - 80))

    W = pygame.Rect(0, 0, 100, 50)
    W.center = (centro, config.ALTO - 130)
    S = pygame.Rect(0, 0, 100, 50)
    S.center = (centro, config.ALTO - 80)
    A = pygame.Rect(0, 0, 100, 50)
    A.center = (centro - 100, config.ALTO - 80)
    D = pygame.Rect(0, 0, 100, 50)
    D.center = (centro + 100, config.ALTO - 80)

    W2 = pygame.draw.rect(config.PANTALLA, config.DARKPINK, W, border_radius=12)
    S2 = pygame.draw.rect(config.PANTALLA, config.DARKPINK, S, border_radius=12)
    A2 = pygame.draw.rect(config.PANTALLA, config.DARKPINK, A, border_radius=12)
    D2 = pygame.draw.rect(config.PANTALLA, config.DARKPINK, D, border_radius=12)

    if W2.collidepoint(MOUSE):
        Arriba = config.banana(85).render(pygame.key.name(config.teclas["w"]).upper(), True, config.PINK)
    if S2.collidepoint(MOUSE):
        Abajo = config.banana(85).render(pygame.key.name(config.teclas["s"]).upper(), True, config.PINK)
    if A2.collidepoint(MOUSE):
        Izquierda = config.banana(85).render(pygame.key.name(config.teclas["a"]).upper(), True, config.PINK)
    if D2.collidepoint(MOUSE):
        Derecha = config.banana(85).render(pygame.key.name(config.teclas["d"]).upper(), True, config.PINK)

    config.PANTALLA.blit(Arriba, Arriba_rect)
    config.PANTALLA.blit(Abajo, Abajo_rect)
    config.PANTALLA.blit(Izquierda, Izquierda_rect)
    config.PANTALLA.blit(Derecha, Derecha_rect)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if W2.collidepoint(evento.pos):
                mover_jugador(0, -1)
            elif S2.collidepoint(evento.pos):
                mover_jugador(0, 1)
            elif A2.collidepoint(evento.pos):
                mover_jugador(-1, 0)
            elif D2.collidepoint(evento.pos):
                mover_jugador(1, 0)

def corazonEn(grid_pos):

    x = grid_pos[0] * config.TAMAÑO_CELDA
    y = grid_pos[1] * config.TAMAÑO_CELDA

    CORAZON = pygame.transform.scale(config.CORAZON, (15, 15))
    image_rect = CORAZON.get_rect(center=((x + config.TAMAÑO_CELDA // 2 + config.PANEL_IZQUIERDO, y + config.TAMAÑO_CELDA // 2)))
    
    config.PANTALLA.blit(CORAZON, image_rect)