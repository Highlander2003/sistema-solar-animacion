import pygame
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from models.celestial_body import CelestialBody
from models.moon import Moon

class Planet(CelestialBody):
    def __init__(self, name, distance, radius, color, orbital_period, inclination=0):
        super().__init__(name, radius, color)
        self.distance = distance
        self.orbital_period = orbital_period
        self.angle = 0
        self.moons = []
        self.moon_count = 0
        self.inclination = inclination * math.pi / 180  # Convertir grados a radianes
        
    def update(self, time_factor):
        # Actualiza la posición basada en el periodo orbital
        self.angle += (2 * math.pi / self.orbital_period) * time_factor
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
            
        # Calcular posición en 3D con inclinación orbital
        self.x = self.distance * math.cos(self.angle)
        self.y = self.distance * math.sin(self.angle) * math.cos(self.inclination)
        self.z = self.distance * math.sin(self.angle) * math.sin(self.inclination)
            
        # Actualizar las lunas
        for moon in self.moons:
            moon.update(time_factor, self.x, self.y, self.z)
            
    def render(self):
        # Dibujar la órbita
        glPushMatrix()
        glColor3f(0.2, 0.2, 0.2)
        glRotatef(self.inclination * 180 / math.pi, 1, 0, 0)
        
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            angle = 2 * math.pi * i / 100
            x = self.distance * math.cos(angle)
            y = self.distance * math.sin(angle)
            glVertex3f(x, y, 0)
        glEnd()
        glPopMatrix()
        
        # Dibujar el planeta
        super().render()
        
        # Dibujar las lunas
        for moon in self.moons:
            moon.render()
            
    def add_moon(self):
        moon_dist = self.radius * 2 + len(self.moons) * 5
        new_moon = Moon(moon_dist, 2, (200, 200, 200), 30)
        self.moons.append(new_moon)
        self.moon_count += 1
        
    def remove_moon(self):
        if self.moons:
            self.moons.pop()
            self.moon_count -= 1
            
    def set_number_of_moons(self, number):
        current = len(self.moons)
        if number > current:
            # Añadir lunas
            for _ in range(number - current):
                self.add_moon()
        elif number < current:
            # Quitar lunas
            for _ in range(current - number):
                self.remove_moon()
                
    def cleanup(self):
        super().cleanup()
        for moon in self.moons:
            moon.cleanup()