Este proyecto consiste en el desarrollo de un sistema de gestión de parqueadero utilizando los principios de la Programación Orientada a Objetos (POO) en Python.

Estructura del Proyecto
El sistema fue dividido en tres clases principales:


Clase Vehiculo: Representa los datos y comportamientos de un vehículo, incluyendo su placa, tipo, hora de entrada, tipo de cliente, número de visitas y ubicación geográfica.


Clase Parqueo: Encargada de la lógica principal del sistema, como el registro de entradas y salidas, manejo de cupos, almacenamiento de datos en un archivo JSON y recuperación del historial.


Clase Funciones: Contiene todas las funcionalidades adicionales del sistema, como:

Generación de reportes en CSV.
Visualización de estadísticas mediante gráficos.
Generación de mapas con la ubicación de los vehículos.
Alertas inteligentes sobre cupos y tiempos de parqueo.



Además se incluye una función auxiliar para generar ubicaciones aleatorias dentro del campus universitario, simulando la geolocalización de los vehículos.

Optimización Realizada

La principal optimización fue la modularización del código. En lugar de tener toda la lógica en un solo archivo, se separaron las responsabilidades en clases bien definidas. Esto permite:

Reutilización de código: Las clases pueden ser reutilizadas en otros proyectos o ampliadas fácilmente.
Mantenimiento más sencillo: Al estar organizado, es más fácil identificar errores o realizar mejoras.
Escalabilidad: Se pueden agregar nuevas funcionalidades sin afectar el núcleo del sistema.

Elemento Innovador
El elemento innovador más destacado es la integración de geolocalización y visualización en mapas. Utilizando la biblioteca folium, el sistema permite generar un mapa interactivo que muestra la ubicación actual o última conocida de un vehículo dentro del campus. Esta funcionalidad no solo mejora la experiencia del usuario, sino que también introduce un componente visual moderno y útil para la gestión del parqueadero.