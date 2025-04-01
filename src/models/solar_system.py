import pygame
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from models.planet import Planet

class SolarSystem:
    def __init__(self):
        self.sun_radius = 30
        self.planets = []
        self.time_factor = 1.0
        
        # Crear planetas con inclinaciones reales aproximadas
        # (nombre, distancia al sol, radio, color, periodo orbital, inclinación)
        self.planets.append(Planet("Mercurio", 70, 5, (200, 200, 200), 88, 7))
        self.planets.append(Planet("Venus", 100, 8, (255, 190, 0), 225, 3.4))
        self.planets.append(Planet("Tierra", 130, 10, (0, 100, 255), 365, 0))
        self.planets.append(Planet("Marte", 170, 7, (255, 50, 0), 687, 1.9))
        self.planets.append(Planet("Júpiter", 230, 20, (255, 200, 100), 4333, 1.3))
        self.planets.append(Planet("Saturno", 290, 17, (255, 220, 150), 10759, 2.5))
        self.planets.append(Planet("Urano", 340, 14, (180, 220, 255), 30687, 0.8))
        self.planets.append(Planet("Neptuno", 380, 14, (50, 50, 255), 60190, 1.8))

        # Cuadric para el sol
        self.sun_quad = gluNewQuadric()
        
        # Inicializar rotación de la vista
        self.rotation_x = 0
        self.rotation_y = 0

    def update(self):
        for planet in self.planets:
            planet.update(self.time_factor)
            
    def render(self):
        # Aplicar rotación de la vista
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        # Dibujar el sol
        glPushMatrix()
        glColor3f(1.0, 1.0, 0.0)
        
        # Configurar luz para el sol
        light_position = [0, 0, 0, 1.0]
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [1.0, 1.0, 0.8, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        
        # Material para el sol
        ambient = [1.0, 1.0, 0.0, 1.0]
        diffuse = [1.0, 1.0, 0.0, 1.0]
        specular = [1.0, 1.0, 1.0, 1.0]
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
        
        gluSphere(self.sun_quad, self.sun_radius, 32, 32)
        glPopMatrix()
        
        # Dibujar planetas
        for planet in self.planets:
            planet.render()
            
    def add_moon(self, planet_index):
        if 0 <= planet_index < len(self.planets):
            self.planets[planet_index].add_moon()
            
    def remove_moon(self, planet_index):
        if 0 <= planet_index < len(self.planets):
            self.planets[planet_index].remove_moon()
            
    def get_planet_count(self):
        return len(self.planets)
        
    def get_planet_name(self, index):
        if 0 <= index < len(self.planets):
            return self.planets[index].name
        return ""
        
    def get_moon_count(self, index):
        if 0 <= index < len(self.planets):
            return self.planets[index].moon_count
        return 0
        
    def get_planet(self, planet_name):
        for planet in self.planets:
            if planet.name == planet_name:
                return planet
        return None
        
    def rotate_view(self, dx, dy):
        # Rotar la vista basado en el arrastre del ratón
        self.rotation_y += dx * 0.5
        self.rotation_x += dy * 0.5
        
        # Limitar la rotación vertical para evitar giros extraños
        if self.rotation_x > 90:
            self.rotation_x = 90
        if self.rotation_x < -90:
            self.rotation_x = -90
            
    def cleanup(self):
        # Limpiar recursos de OpenGL
        gluDeleteQuadric(self.sun_quad)
        for planet in self.planets:
            planet.cleanup()