# main.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math

from models.solar_system import SolarSystem
from ui.control_panel import ControlPanel

# Clase para los botones interactivos
class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 200), hover_color=(120, 120, 220), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.text_color = text_color
        
    def draw(self, surface, font):
        # Dibujar el botón con efecto hover
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)  # Borde blanco
        
        # Dibujar el texto con el color especificado
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        # Verifica si el ratón está sobre el botón
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, clicked):
        # Verifica si el botón fue clickeado
        return self.rect.collidepoint(mouse_pos) and clicked

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
    fullscreen = False
    
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
    
    # Variable para controlar el zoom
    zoom_level = 1.0
    
    # Inicializar contador de años
    elapsed_years = 0.0
    
    # Crear botones interactivos
    button_font = pygame.font.SysFont('Arial', 18)
    speed_up_button = Button(display[0] - 130, 10, 120, 30, "Velocidad +", (50, 120, 200))
    speed_down_button = Button(display[0] - 130, 50, 120, 30, "Velocidad -", (50, 120, 200))
    reset_button = Button(display[0] - 130, 90, 120, 30, "Reset", (200, 80, 80))
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
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
            
            # Manejo del scroll del mouse para zoom
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo
                    mouse_clicked = True
                elif event.button == 4:  # Scroll hacia arriba
                    zoom_level *= 1.1  # Acercar un 10%
                elif event.button == 5:  # Scroll hacia abajo
                    zoom_level *= 0.9  # Alejar un 10%
                    
            control_panel.handle_event(event)
        
        # Actualizar estado de los botones
        speed_up_button.check_hover(mouse_pos)
        speed_down_button.check_hover(mouse_pos)
        reset_button.check_hover(mouse_pos)
        
        # Verificar clics en botones
        if mouse_clicked:
            if speed_up_button.is_clicked(mouse_pos, True):
                solar_system.time_factor *= 2.0  # Duplicar velocidad
            elif speed_down_button.is_clicked(mouse_pos, True):
                solar_system.time_factor /= 2.0  # Reducir velocidad a la mitad
            elif reset_button.is_clicked(mouse_pos, True):
                solar_system.time_factor = 1.0  # Restaurar velocidad original
                elapsed_years = 0.0  # Reiniciar contador de años
        
        # Procesar entradas continuas
        control_panel.handle_user_input()
        
        # Actualizar sistema solar
        solar_system.update()
        
        # Actualizar contador de años (basado en días terrestres)
        elapsed_years += (solar_system.time_factor * 1.0) / 365.0
        
        # Limpiar la pantalla y buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Renderizar la parte 3D con OpenGL
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Aplicar zoom a la cámara
        camera_distance = 500 / zoom_level
        camera_height = 200 / zoom_level
        
        gluLookAt(0, -camera_distance, camera_height,
                  0, 0, 0,
                  0, 0, 1)
        
        # Renderizar sistema solar
        solar_system.render()
        
        # Guardar y restaurar el estado de OpenGL antes de dibujar la interfaz 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], display[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        
        # Ahora renderizamos directamente en la pantalla sin usar overlay
        screen = pygame.display.get_surface()
        
        # Dibujar botones directamente
        speed_up_button.draw(screen, button_font)
        speed_down_button.draw(screen, button_font)
        reset_button.draw(screen, button_font)
        
        # Mostrar información en la interfaz
        font = pygame.font.SysFont('Arial', 18)
        info_font = pygame.font.SysFont('Arial', 16)
        
        # Mostrar años transcurridos con texto blanco brillante
        years_text = f"Años transcurridos: {elapsed_years:.2f}"
        years_surface = font.render(years_text, True, (255, 255, 255))
        screen.blit(years_surface, (10, 10))
        
        # Mostrar velocidad actual con texto blanco brillante
        speed_text = f"Velocidad: {solar_system.time_factor:.1f}x"
        speed_surface = font.render(speed_text, True, (255, 255, 255))
        screen.blit(speed_surface, (10, 40))
        
        # Cambiar el nivel de zoom a blanco puro en lugar de gris
        zoom_text = f"Zoom: {zoom_level:.1f}x"
        zoom_surface = info_font.render(zoom_text, True, (255, 255, 255))  # Cambiado a blanco puro
        screen.blit(zoom_surface, (10, display[1] - 30))
        
        control_panel.render(screen)  # Renderizar texto directamente en la pantalla
        
        # Restaurar el estado de OpenGL para la próxima iteración
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 FPS
    
    # Limpieza de recursos
    solar_system.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()