import pygame
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class CelestialBody:
    def __init__(self, name, radius, color):
        self.name = name
        self.radius = radius
        self.color = color
        self.x = 0
        self.y = 0
        self.z = 0  # Añadimos coordenada Z
        self.quad = gluNewQuadric()  # Creamos un objeto cuádrico para dibujar esferas
        
    def update(self, time_factor):
        # Método base para actualizar la posición
        pass
        
    def render(self):
        # Método base para dibujar el objeto en 3D
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        # Configurar el material y color
        r, g, b = self.color
        glColor3f(r/255.0, g/255.0, b/255.0)
        ambient = [r/255.0 * 0.2, g/255.0 * 0.2, b/255.0 * 0.2, 1.0]
        diffuse = [r/255.0, g/255.0, b/255.0, 1.0]
        specular = [1.0, 1.0, 1.0, 1.0]
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        
        # Dibujar la esfera
        gluSphere(self.quad, self.radius, 32, 32)
        glPopMatrix()
        
    def cleanup(self):
        # Limpieza de recursos OpenGL
        if self.quad:
            gluDeleteQuadric(self.quad)