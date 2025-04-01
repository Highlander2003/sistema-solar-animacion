class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render_planets(self, planets):
        for planet in planets:
            self.draw_planet(planet)

    def render_moons(self, moons):
        for moon in moons:
            self.draw_moon(moon)

    def draw_planet(self, planet):
        # Implementación para dibujar un planeta en la pantalla
        pass

    def draw_moon(self, moon):
        # Implementación para dibujar una luna en la pantalla
        pass