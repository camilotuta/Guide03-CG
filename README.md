# Longcat

Longcat es un juego desarrollado en Python utilizando la librería Pygame. En este juego, el jugador controla un gato que se desplaza por una cuadrícula, dejando un rastro a medida que se mueve. El objetivo es atrapar al gato llenando el mayor porcentaje posible de celdas en la zona interior del tablero. Si al quedar atrapado el gato se han llenado al menos el 80% de las celdas, ganas; de lo contrario, pierdes.

![Gameplay](/images/image.png) ![Gameplay2](/images/image-1.png) ![win](/images/image-2.png) ![fail](/images/image-3.png)

## Características

- **Cuadrícula de juego:** 10 filas x 10 columnas en una ventana de 900x900 píxeles.
- **Obstáculos:** El borde del nivel siempre es un obstáculo (pared), y se añaden obstáculos aleatorios en el interior con una probabilidad configurable.
- **Movimiento suave:** El gato se mueve de forma animada a lo largo de la cuadrícula.
- **Relleno de celdas:** Cada movimiento deja una marca en las celdas, diferenciada según si el movimiento fue horizontal o vertical.
- **Dificultad progresiva:** Al reiniciar el juego, la probabilidad de obstáculos aumenta, haciendo el juego más desafiante.
- **Pantalla de Game Over:** Se muestra un resumen del desempeño con la opción de reiniciar o salir.

## Instalación y Requisitos

### Requisitos

- Python 3.x
- Pygame

### Instalación de Pygame

Instala Pygame mediante pip:

```bash
pip install pygame
```

### Archivos del Proyecto

- **main.py:** Archivo principal que contiene toda la lógica del juego.
- **images/**: Carpeta que debe incluir las siguientes imágenes:
  - `cat.png`: Imagen del gato (Longcat).
  - `wall.png`: Imagen que representa las paredes y obstáculos.
  - `filledX.png`: Imagen para marcar celdas llenadas por movimientos horizontales.
  - `filledY.png`: Imagen para marcar celdas llenadas por movimientos verticales.

## Cómo Jugar

1. **Ejecución del juego:**

   Ejecuta el juego con el siguiente comando:

   ```bash
   python main.py
   ```

2. **Controles:**

   - **Flechas del teclado:** Mover al gato en la dirección deseada (arriba, abajo, izquierda o derecha).
   - **R:** Reiniciar el juego después de un Game Over.
   - **Q:** Salir del juego.

3. **Mecánica del juego:**

   - Al presionar una tecla de dirección, el gato se desplaza en esa dirección hasta chocar con un obstáculo o el borde de la cuadrícula.
   - Cada celda por la que pasa el gato se marca con una imagen que indica el tipo de movimiento (horizontal o vertical).
   - Cuando el gato no tiene más celdas vacías a las que moverse, se considera atrapado y se calcula el porcentaje de celdas llenadas.
   - **Resultado:**
     - **Ganar:** Si el porcentaje de celdas llenadas es mayor o igual al 80%.
     - **Perder:** Si el porcentaje es menor al 80%.
   - Al reiniciar el juego, la probabilidad de aparición de obstáculos aumenta, incrementando la dificultad progresivamente.

## Estructura del Código

El código se organiza en varias funciones clave:

- **Carga de Imágenes (`load_images`):** Carga y escala las imágenes de cat, paredes y marcas de movimiento.
- **Creación del Nivel (`create_level`):** Genera la cuadrícula, define el borde como obstáculos y añade obstáculos aleatorios en el interior.
- **Dibujo de la Cuadrícula (`draw_grid`):** Dibuja cada celda, incluyendo el fondo, obstáculos y las marcas dejadas por el gato, además de posicionar la imagen del gato.
- **Cálculo del Movimiento (`get_movement_path`):** Determina la trayectoria del gato en función de la dirección de movimiento, hasta encontrar un obstáculo.
- **Verificación de Atrapamiento (`is_trapped`):** Comprueba si el gato está rodeado y no tiene celdas vacías adyacentes.
- **Actualización del Movimiento (`update_movement`):** Realiza el movimiento suave del gato hacia la siguiente celda en la trayectoria.
- **Pantalla de Game Over (`show_game_over_screen`):** Muestra el resultado final, indicando si ganaste o perdiste, y permite reiniciar o salir del juego.

## Créditos y Licencia

Este juego fue creado como proyecto en Python utilizando Pygame. Asegúrate de que la carpeta `images` se encuentre en el mismo directorio que `main.py` para que el juego funcione correctamente.

**Licencia:** [Especifica la licencia aquí, por ejemplo, MIT License]

---

¡Disfruta atrapando a Longcat y pon a prueba tus habilidades estratégicas!
