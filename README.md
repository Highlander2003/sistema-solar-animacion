# Sistema Solar Animación

Este proyecto es una animación interactiva del sistema solar, donde los usuarios pueden visualizar los planetas y sus lunas, así como modificar el número de lunas por planeta.

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

1. Clona el repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Instala las dependencias necesarias ejecutando:

```
pip install -r requirements.txt
```

## Uso

Para ejecutar la animación del sistema solar, utiliza el siguiente comando:

```
python src/main.py
```

Una vez que la aplicación esté en funcionamiento, podrás interactuar con el panel de control para modificar el número de lunas por planeta y observar los cambios en tiempo real.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un issue o envía un pull request.