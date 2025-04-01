# main.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

from models.solar_system import SolarSystem
from ui.control_panel import ControlPanel

def init_opengl(width, height):
    # Configurar vista 3D
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 1, 2000.0)  # Aumentado el valor de lejanía para poder hacer más zoom
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Posición inicial de la cámara
    gluLookAt(0, -500, 200,  # posición de la cámara
              0, 0, 0,       # punto al que mira
              0, 0, 1)       # vector "arriba"
    
    # Habilitar iluminación
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

def main():
    pygame.init()
    
    # Obtener información sobre la pantalla
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    
    # Usar pantalla completa o una ventana grande
    fullscreen = False  # Cambiado a False por defecto para abrir en ventana
    
    if fullscreen:
        # Configuración de pantalla completa
        display = (screen_width, screen_height)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
    else:
        # Configuración de ventana que ocupa casi toda la pantalla
        display = (int(screen_width * 0.9), int(screen_height * 0.9))
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
    pygame.display.set_caption("Sistema Solar 3D")
    
    # Configurar OpenGL con las dimensiones actuales
    init_opengl(display[0], display[1])
    
    # Inicializar el sistema solar
    solar_system = SolarSystem()
    control_panel = ControlPanel(solar_system)
    
    # Crear superficie para texto 2D
    overlay = pygame.Surface(display, pygame.SRCALPHA)
    
    # Variable para controlar el zoom
    zoom_level = 1.0
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Permitir salir de pantalla completa con ESC
                if event.key == pygame.K_ESCAPE and fullscreen:
                    running = False
                # Alternar entre pantalla completa y ventana con F11
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        display = (screen_width, screen_height)
                        pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
                    else:
                        display = (int(screen_width * 0.9), int(screen_height * 0.9))
                        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
                    init_opengl(display[0], display[1])
                    overlay = pygame.Surface(display, pygame.SRCALPHA)
            
            # Manejo del scroll del mouse para zoom
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll hacia arriba
                    zoom_level *= 1.1  # Acercar un 10%
                elif event.button == 5:  # Scroll hacia abajo
                    zoom_level *= 0.9  # Alejar un 10%
                    
            control_panel.handle_event(event)
        
        # Añadir esta línea para procesar entradas continuas
        control_panel.handle_user_input()
        
        # Actualizar sistema solar
        solar_system.update()
        
        # Limpiar la pantalla y buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Empezar a dibujar en 3D con zoom aplicado
        glLoadIdentity()
        
        # Aplicar zoom a la cámara
        camera_distance = 500 / zoom_level  # Ajustar distancia según nivel de zoom
        camera_height = 200 / zoom_level    # Ajustar altura según nivel de zoom
        
        gluLookAt(0, -camera_distance, camera_height,  # posición de la cámara con zoom
                  0, 0, 0,       # punto al que mira
                  0, 0, 1)       # vector "arriba"
        
        # Renderizar sistema solar
        solar_system.render()
        
        # Volver a modo 2D para la interfaz
        overlay.fill((0, 0, 0, 0))  # Limpiar overlay transparente
        
        # Mostrar nivel de zoom en la interfaz
        font = pygame.font.SysFont('Arial', 16)
        zoom_text = f"Zoom: {zoom_level:.1f}x"
        zoom_surface = font.render(zoom_text, True, (255, 255, 255))
        overlay.blit(zoom_surface, (10, display[1] - 30))
        
        control_panel.render(overlay)  # Renderizar texto en el overlay
        
        # Blitear el overlay en la pantalla
        screen = pygame.display.get_surface()
        screen.blit(overlay, (0, 0))
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)  # Cambiado a 60 FPS para mejor rendimiento
    
    # Limpieza de recursos
    solar_system.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()