import pygame
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from models.celestial_body import CelestialBody

class Moon(CelestialBody):
    def __init__(self, distance, radius, color, orbital_period, inclination=0):
        super().__init__("Moon", radius, color)
        self.distance = distance
        self.orbital_period = orbital_period
        self.angle = 0
        self.inclination = inclination * math.pi / 180  # Convertir grados a radianes
        
    def update(self, time_factor, planet_x, planet_y, planet_z):
        self.angle += (2 * math.pi / self.orbital_period) * time_factor
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
            
        # Calcular posición 3D relativa al planeta con inclinación
        orbit_x = self.distance * math.cos(self.angle)
        orbit_y = self.distance * math.sin(self.angle) * math.cos(self.inclination)
        orbit_z = self.distance * math.sin(self.angle) * math.sin(self.inclination)
        
        # Posición final relativa al planeta
        self.x = planet_x + orbit_x
        self.y = planet_y + orbit_y
        self.z = planet_z + orbit_z