import pygame
from pygame.locals import *

class ControlPanel:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.selected_planet = 0
        self.font = pygame.font.SysFont('Arial', 14)
        self.title_font = pygame.font.SysFont('Arial', 18, bold=True)
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.needs_refresh = False
        
        # Panel lateral izquierdo
        self.panel_width = 200
        self.panel_color = (30, 30, 50, 180)  # Color con transparencia
        
        # Control de velocidad
        self.slider_rect = pygame.Rect(20, 200, 160, 20)
        self.slider_handle_rect = pygame.Rect(90, 195, 12, 30)  # Posición inicial centrada
        self.slider_dragging = False
        self.min_time_factor = 0.1
        self.max_time_factor = 5.0
        
        # Contador de tiempo
        self.elapsed_days = 0
        self.elapsed_years = 0
        self.days_per_update = 1  # Días simulados por actualización
        self.days_in_year = 365

    def display(self, screen):
        """
        Maneja la lógica de visualización del panel de control.
        Determina si el panel debe mostrarse y prepara los datos necesarios antes de renderizar.
        
        Args:
            screen: Superficie de pygame donde se dibujará el panel
        """
        # Actualizar la posición del deslizador según el factor de tiempo actual
        self._update_slider_position()
        
        # Verificar si hay cambios que requieren actualización visual
        if self.needs_refresh:
            # Resetear la bandera de actualización
            self.needs_refresh = False
            
            # Aquí podrías implementar animaciones o efectos visuales
            # al producirse cambios en el sistema (como agregar/quitar lunas)
        
        # Actualizar la información del planeta seleccionado si ha cambiado
        planet_name = self.solar_system.get_planet_name(self.selected_planet)
        current_moons = self.solar_system.get_moon_count(self.selected_planet)
        
        # Si hay datos del sistema solar que necesitan ser actualizados antes de mostrar,
        # se podrían procesar aquí
        
        # Renderizar el panel con la información actualizada
        self.render(screen)

    def update_moons(self, planet_name, number_of_moons):
        planet = self.solar_system.get_planet(planet_name)
        if planet:
            planet.set_number_of_moons(number_of_moons)
            self.refresh_display()

    def refresh_display(self):
        """
        Actualiza la visualización cuando ocurren cambios en el sistema solar.
        Este método se llama después de actualizar las lunas de un planeta.
        """
        self.needs_refresh = True
        
        if self.selected_planet >= 0 and self.selected_planet < self.solar_system.get_planet_count():
            planet_name = self.solar_system.get_planet_name(self.selected_planet)
            print(f"Planeta {planet_name} actualizado - Lunas: {self.solar_system.get_moon_count(self.selected_planet)}")
    
    def update_time(self):
        """
        Actualiza los contadores de días y años basado en la velocidad de simulación
        """
        days_increment = self.days_per_update * self.solar_system.time_factor
        self.elapsed_days += days_increment
        
        # Convertir a años cuando sea necesario
        if self.elapsed_days >= self.days_in_year:
            years_to_add = int(self.elapsed_days / self.days_in_year)
            self.elapsed_years += years_to_add
            self.elapsed_days -= years_to_add * self.days_in_year

    def handle_user_input(self):
        """
        Maneja entradas continuas del usuario como teclas presionadas,
        en lugar de eventos discretos que se manejan en handle_event.
        Debe llamarse en cada fotograma.
        """
        # Obtener estado de teclas presionadas
        keys = pygame.key.get_pressed()
        
        # Control de velocidad de simulación con teclas (mantener esta funcionalidad)
        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            self.solar_system.time_factor *= 1.05  # Aumentar velocidad
            self._update_slider_position()
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.solar_system.time_factor *= 0.95  # Disminuir velocidad
            self._update_slider_position()
            
        # Zoom con teclas Z/X
        if keys[pygame.K_z]:
            # Acercar cámara
            glMatrixMode(GL_MODELVIEW)
            glTranslatef(0, 20, -10)
        if keys[pygame.K_x]:
            # Alejar cámara
            glMatrixMode(GL_MODELVIEW)
            glTranslatef(0, -20, 10)
            
        # Restablecer vista
        if keys[pygame.K_r]:
            # Resetear la rotación de vista
            self.solar_system.rotation_x = 0
            self.solar_system.rotation_y = 0

    def handle_event(self, event):
        # Gestionar el deslizador de velocidad
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verificar si se hizo clic en el control deslizante
            if self.slider_handle_rect.collidepoint(event.pos):
                self.slider_dragging = True
            # Mantener el código existente para arrastrar la vista
            else:
                self.dragging = True
                self.last_mouse_pos = event.pos
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_dragging = False
            self.dragging = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.slider_dragging:
                # Actualizar posición del control deslizante
                new_x = max(self.slider_rect.left, min(event.pos[0], self.slider_rect.right))
                self.slider_handle_rect.centerx = new_x
                
                # Calcular factor de tiempo basado en la posición del deslizador
                slider_range = self.slider_rect.width
                position_ratio = (new_x - self.slider_rect.left) / slider_range
                self.solar_system.time_factor = self.min_time_factor + position_ratio * (self.max_time_factor - self.min_time_factor)
                
            # Código existente para el arrastre de la vista
            elif self.dragging:
                # Calcular el desplazamiento del ratón
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                self.solar_system.rotate_view(dx, dy)
                self.last_mouse_pos = event.pos
        
        if event.type == pygame.KEYDOWN:
            # Cambiar planeta seleccionado
            if event.key == pygame.K_LEFT:
                self.selected_planet = (self.selected_planet - 1) % self.solar_system.get_planet_count()
            elif event.key == pygame.K_RIGHT:
                self.selected_planet = (self.selected_planet + 1) % self.solar_system.get_planet_count()
            # Agregar/quitar lunas
            elif event.key == pygame.K_UP:
                self.solar_system.add_moon(self.selected_planet)
            elif event.key == pygame.K_DOWN:
                self.solar_system.remove_moon(self.selected_planet)

    def _update_slider_position(self):
        """
        Actualiza la posición del control deslizante basado en el factor de tiempo actual
        """
        ratio = (self.solar_system.time_factor - self.min_time_factor) / (self.max_time_factor - self.min_time_factor)
        self.slider_handle_rect.centerx = self.slider_rect.left + ratio * self.slider_rect.width

    def render(self, screen):
        # Dibujar panel lateral
        panel_surface = pygame.Surface((self.panel_width, screen.get_height()), pygame.SRCALPHA)
        panel_surface.fill(self.panel_color)
        
        # Título del panel
        title = self.title_font.render("CONTROL DE SISTEMA", True, (255, 255, 255))
        panel_surface.blit(title, (20, 20))
        
        # Información de tiempo
        time_title = self.font.render("TIEMPO TRANSCURRIDO:", True, (200, 200, 255))
        panel_surface.blit(time_title, (20, 60))
        
        years_text = self.font.render(f"Años: {self.elapsed_years:.1f}", True, (255, 255, 255))
        panel_surface.blit(years_text, (20, 80))
        
        days_text = self.font.render(f"Días: {self.elapsed_days:.1f}", True, (255, 255, 255))
        panel_surface.blit(days_text, (20, 100))
        
        # Control de velocidad
        speed_title = self.font.render("VELOCIDAD DE SIMULACIÓN:", True, (200, 200, 255))
        panel_surface.blit(speed_title, (20, 160))
        
        factor_text = self.font.render(f"Factor: x{self.solar_system.time_factor:.2f}", True, (255, 255, 255))
        panel_surface.blit(factor_text, (20, 180))
        
        # Dibujar deslizador
        pygame.draw.rect(panel_surface, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(panel_surface, (200, 200, 200), self.slider_handle_rect)
        
        # Etiquetas min/max
        min_label = self.font.render(f"{self.min_time_factor}x", True, (255, 255, 255))
        panel_surface.blit(min_label, (self.slider_rect.left - 5, self.slider_rect.bottom + 5))
        
        max_label = self.font.render(f"{self.max_time_factor}x", True, (255, 255, 255))
        panel_surface.blit(max_label, (self.slider_rect.right - 25, self.slider_rect.bottom + 5))
        
        # Mostrar información del planeta seleccionado
        planet_info_title = self.font.render("PLANETA SELECCIONADO:", True, (200, 200, 255))
        panel_surface.blit(planet_info_title, (20, 260))
        
        planet_name = self.solar_system.get_planet_name(self.selected_planet)
        planet_text = self.font.render(f"{planet_name}", True, (255, 255, 255))
        panel_surface.blit(planet_text, (20, 280))
        
        moons_text = self.font.render(f"Lunas: {self.solar_system.get_moon_count(self.selected_planet)}", True, (255, 255, 255))
        panel_surface.blit(moons_text, (20, 300))
        
        # Instrucciones de control
        instructions_title = self.font.render("CONTROLES:", True, (200, 200, 255))
        panel_surface.blit(instructions_title, (20, 340))
        
        instructions = [
            "← / →: Cambiar planeta",
            "↑: Agregar luna",
            "↓: Quitar luna",
            "Arrastrar: Rotar vista",
            "Z/X: Acercar/Alejar"
        ]
        
        for i, text in enumerate(instructions):
            instr_text = self.font.render(text, True, (220, 220, 220))
            panel_surface.blit(instr_text, (20, 360 + i * 20))
        
        # Mostrar el panel en la pantalla
        screen.blit(panel_surface, (0, 0))