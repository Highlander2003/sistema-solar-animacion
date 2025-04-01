import pygame

class ControlPanel:
    def __init__(self, solar_system):
        self.solar_system = solar_system
        self.selected_planet = 0
        self.font = pygame.font.SysFont('Arial', 14)
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.needs_refresh = False

    def display(self):
        # Aquí se implementaría la lógica para mostrar la interfaz gráfica
        pass

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
        # Bandera para indicar que se requiere actualizar la visualización
        self.needs_refresh = True
        
        # En este caso, con OpenGL la actualización real ocurre en cada fotograma en el bucle principal,
        # pero podríamos realizar ciertos cálculos aquí si fuera necesario
        
        # Por ejemplo, si tuviéramos vistas específicas o cámaras preconfiguradas:
        if self.selected_planet >= 0 and self.selected_planet < self.solar_system.get_planet_count():
            # Actualizar propiedades específicas para el planeta seleccionado
            planet_name = self.solar_system.get_planet_name(self.selected_planet)
            print(f"Planeta {planet_name} actualizado - Lunas: {self.solar_system.get_moon_count(self.selected_planet)}")

    def handle_user_input(self):
        """
        Maneja entradas continuas del usuario como teclas presionadas,
        en lugar de eventos discretos que se manejan en handle_event.
        Debe llamarse en cada fotograma.
        """
        # Obtener estado de teclas presionadas
        keys = pygame.key.get_pressed()
        
        # Control de velocidad de simulación
        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            self.solar_system.time_factor *= 1.05  # Aumentar velocidad
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.solar_system.time_factor *= 0.95  # Disminuir velocidad
            
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
                
        # Control de rotación con el ratón
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo
                self.dragging = True
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Calcular el desplazamiento del ratón
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]
            self.solar_system.rotate_view(dx, dy)
            self.last_mouse_pos = event.pos

    def render(self, screen):
        # Mostrar instrucciones
        instructions = [
            "Flechas izquierda/derecha: Seleccionar planeta",
            "Flecha arriba: Agregar luna",
            "Flecha abajo: Quitar luna",
            "Arrastrar con el ratón: Rotar vista",
            f"Planeta seleccionado: {self.solar_system.get_planet_name(self.selected_planet)}",
            f"Número de lunas: {self.solar_system.get_moon_count(self.selected_planet)}"
        ]
        
        for i, text in enumerate(instructions):
            surface = self.font.render(text, True, (255, 255, 255))
            screen.blit(surface, (10, 10 + i * 20))