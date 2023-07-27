#Program: Trajectory of a projectile during a volcanic eruption
#Version: 1.0
#Developer: Emiliano Vivas Rodríguez
#Contact: a01424732@tec.mx
#Since: 2021/10/10

from pygame import *
import sys, math

ALTO, ANCHO = 650, 1250
bola, fondo = image.load("bola.png"), image.load("volcan.png")

class Proyectil(sprite.Sprite):

    def __init__(self, x, y):
        self.angulo = 45
        self.velocidad = 50
        self.tiempo = 0
        self.x = x
        self.y = y
        self.disparar = False
        self.xreal = x
        self.yreal = ALTO - self.y
        self.vectorVelocidad = [0 , 0]
        self.velocidadX = 0
        self.velocidadY = 0
        self.resistencia = 0.47

    def update(self):
        self.velocidadX = self.velocidad * math.cos(math.radians(self.angulo))
        self.velocidadY = self.velocidad * math.sin(math.radians(self.angulo))
        if self.disparar:
            u = self.velocidad/2
            self.xreal = (u*math.cos(math.radians(math.pi)) * self.tiempo + (self.velocidadX - u*math.cos(math.radians(math.pi)))*(1-math.exp(-self.resistencia*self.tiempo))/self.resistencia) if self.velocidadX > 1e-14 else 0
            self.yreal = (9.81/self.resistencia+self.velocidadY-u*math.sin(math.radians(math.pi))) * (1-math.exp(-self.resistencia*self.tiempo))/self.resistencia-(9.81/self.resistencia-u*math.sin(math.radians(math.pi)))*self.tiempo
            self.x = self.xreal
            self.y = ALTO - self.yreal
        if self.y > ALTO or self.x > ANCHO:
            self.x = 0
            self.y = ALTO
            self.disparar = False

def main():
    global bola
    init()
    screen = display.set_mode((ANCHO, ALTO))
    display.set_icon(bola)
    bola = transform.scale(image.load("bola.png"), (35, 35))
    display.set_caption("Trayectoria de un proyectil durante una erupción volcánica.")
    proyectil = Proyectil(0, ALTO)
    key.set_repeat(1, 80)
    clock = time.Clock()
    while True:
        tick = clock.tick(60)
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == K_SPACE or e.key == K_RETURN:
                    proyectil.tiempo = 0
                    proyectil.disparar = True
                elif not proyectil.disparar:
                    if e.key == K_UP:
                        if proyectil.angulo < 90: proyectil.angulo += 1
                    elif e.key == K_DOWN:
                        if proyectil.angulo > 0: proyectil.angulo -= 1
                    elif e.key == K_RIGHT:
                        if proyectil.velocidad < 1000: proyectil.velocidad += 1
                    elif e.key == K_LEFT:
                        if proyectil.velocidad > 10: proyectil.velocidad -= 1
                    elif e.key == K_PLUS or e.key == K_KP_PLUS:
                        if proyectil.resistencia < 3: proyectil.resistencia += 0.01
                    elif e.key == K_MINUS or e.key == K_KP_MINUS:
                        if proyectil.resistencia > 0.01:
                            proyectil.resistencia -= 0.01
                elif e.key == K_ESCAPE: sys.exit()
        if proyectil.disparar: proyectil.tiempo += (tick / 1000)
        rectangle = Surface((screen.get_width()//4, 450))
        rectangle.set_alpha(200)
        rectangle.fill((0, 0, 0))
        proyectil.vectorVelocidad = [proyectil.velocidadX-proyectil.resistencia*proyectil.tiempo, proyectil.velocidadY -2 *9.81*proyectil.tiempo]
        proyectil.update()
        dato = ['', '', "Ángulo:   " + str(proyectil.angulo) + '°', '',
        "Tiempo:   " + str(round(proyectil.tiempo, 2)) + "   s", '',
        "Vector posición:   " + str(round((proyectil.xreal**2 + proyectil.yreal**2)**0.5, 2)) + "   m",
        "Posición:   (" + str(round(proyectil.xreal, 2)) + " , " + str(round(proyectil.yreal, 2)) + ")   m", '',
        '', "Vector velocidad:   " + str(round((proyectil.vectorVelocidad[0]**2 + proyectil.vectorVelocidad[1]**2)**0.5, 2)) + "   m / s",
        "Velocidad:   (" + str(round(proyectil.vectorVelocidad[0], 2)) + " , " + str(round(proyectil.vectorVelocidad[1], 2)) + ")   m / s", '', 
        '', "Resistencia del aire:   " + str(round(proyectil.resistencia, 2))]
        razon = screen.get_width() - rectangle.get_width() + 30
        screen.fill((255, 255, 255))
        screen.blit(fondo,(0,0))
        screen.blit(rectangle, (razon - 30, 0))
        if proyectil.disparar: screen.blit(font.Font(None, 24).render("Simulación actual.", 1, (255, 255, 255)), (razon, 25))
        else: screen.blit(font.Font(None, 24).render("Simulación anterior.", 1, (255, 255, 255)), (razon, 25))
        screen.blit(font.Font(None, 18).render("^ para incrementar; v para decrementar.", 1, (255, 255, 255)), (razon, 75))
        screen.blit(font.Font(None, 18).render("> para incrementar; < para decrementar.", 1, (255, 255, 255)), (razon, 275))
        screen.blit(font.Font(None, 18).render("+ para incrementar; - para decrementar.", 1, (255, 255, 255)), (razon, 375))
        for index in range(len(dato)): screen.blit(font.Font(None, 22).render(dato[index], 1, (255, 255, 255)), (razon, (index + 2) * 25))
        screen.blit(bola, (int(proyectil.x) - bola.get_width()//2, int(proyectil.y) - bola.get_height()//2))
        display.flip()

if __name__ == "__main__": main()