# Sistema Solar Animación 3D

Este proyecto es una animación interactiva en 3D del sistema solar, donde los usuarios pueden visualizar los planetas y sus lunas, modificar el número de lunas por planeta, ajustar la velocidad de la simulación y hacer zoom o rotar la vista.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
sistema-solar-animacion
├── src
│   ├── main.py                # Punto de entrada de la aplicación
│   ├── animation              # Módulo de animación
│   │   ├── __init__.py
│   │   └── renderer.py        # Clase para renderizar cuerpos celestes
│   ├── models                 # Módulo de modelos
│   │   ├── __init__.py
│   │   ├── celestial_body.py   # Clase base para cuerpos celestes
│   │   ├── planet.py          # Clase para planetas
│   │   ├── moon.py            # Clase para lunas
│   │   └── solar_system.py     # Clase para gestionar el sistema solar
│   ├── data                   # Módulo de datos
│   │   ├── __init__.py
│   │   └── planets_data.py     # Datos predefinidos sobre los planetas
│   └── ui                     # Módulo de interfaz de usuario
│       ├── __init__.py
│       └── control_panel.py    # Clase para el panel de control
├── config.json                # Configuración del proyecto
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del proyecto
```

## Instalación

1. Clona el repositorio en tu máquina local:
   ```bash
   git clone https://github.com/Highlander2003/sistema-solar-animacion
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd sistema-solar-animacion
   ```
3. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la animación del sistema solar, utiliza el siguiente comando desde la raíz del proyecto:

```bash
python src/main.py
```

### Controles

- **Zoom**: Usa la rueda del ratón para acercar o alejar la vista.
- **Rotación**: Mantén presionado el botón izquierdo del ratón y arrastra para rotar la cámara.
- **Velocidad**:
  - Usa los botones interactivos en la interfaz para aumentar o disminuir la velocidad de la simulación.
  - También puedes restablecer la velocidad a su valor original.
- **Interacción con planetas**:
  - Usa las flechas del teclado para seleccionar un planeta.
  - Usa las flechas `↑` y `↓` para agregar o quitar lunas al planeta seleccionado.

### Información en pantalla

- **Años transcurridos**: Muestra el tiempo simulado en años terrestres.
- **Velocidad actual**: Indica la velocidad de la simulación en relación al tiempo real.
- **Nivel de zoom**: Muestra el nivel de zoom actual.

## Requisitos

- Python 3.9 o superior
- Dependencias listadas en `requirements.txt`:
  - `pygame`
  - `PyOpenGL`
  - `numpy`

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
