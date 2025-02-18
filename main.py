import os
import pygame
import sys
import random

# --- Configuración del juego ---
WIDTH, HEIGHT = 900, 900  # Tamaño de la ventana
ROWS, COLS = 10, 10  # Dimensiones de la cuadrícula
CELL_SIZE = WIDTH // COLS  # Tamaño de cada celda

# Probabilidad para que una celda interior se convierta en obstáculo
OBSTACLE_PROBABILITY = 0.02

# Definición de tipos de celda
EMPTY = 0  # Celda vacía
WALL = 1  # Pared u obstáculo (incluye borde y obstáculos aleatorios)
FILLED_X = 2  # Celda llena por movimiento horizontal (derecha o izquierda)
FILLED_Y = 3  # Celda llena por movimiento vertical (arriba o abajo)

# Velocidad de movimiento en píxeles por frame (para mayor o menor suavizado)
SPEED = 7


# --- Función para cargar imágenes usando ruta relativa ---
def load_images():
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "images")

    cat_img = pygame.image.load(os.path.join(image_path, "cat.png")).convert_alpha()
    wall_img = pygame.image.load(os.path.join(image_path, "wall.png")).convert_alpha()
    filledX_img = pygame.image.load(
        os.path.join(image_path, "filledX.png")
    ).convert_alpha()
    filledY_img = pygame.image.load(
        os.path.join(image_path, "filledY.png")
    ).convert_alpha()

    # Escalar las imágenes al tamaño de cada celda
    cat_img = pygame.transform.scale(cat_img, (CELL_SIZE, CELL_SIZE))
    wall_img = pygame.transform.scale(wall_img, (CELL_SIZE, CELL_SIZE))
    filledX_img = pygame.transform.scale(filledX_img, (CELL_SIZE, CELL_SIZE))
    filledY_img = pygame.transform.scale(filledY_img, (CELL_SIZE, CELL_SIZE))

    return cat_img, wall_img, filledX_img, filledY_img


# --- Creación del nivel con obstáculos aleatorios ---
def create_level():
    global OBSTACLE_PROBABILITY
    # Se crea una cuadrícula llena de celdas vacías
    grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
    # Agregar paredes en el borde del nivel
    for i in range(ROWS):
        grid[i][0] = WALL
        grid[i][COLS - 1] = WALL
    for j in range(COLS):
        grid[0][j] = WALL
        grid[ROWS - 1][j] = WALL
    # Agregar obstáculos aleatorios en el interior
    for i in range(1, ROWS - 1):
        for j in range(1, COLS - 1):
            if random.random() < OBSTACLE_PROBABILITY:
                grid[i][j] = WALL
    return grid


# --- Función para dibujar los elementos (sin líneas de cuadrícula) ---
def draw_grid(screen, grid, cat_pixel_pos, images):
    cat_img, wall_img, filledX_img, filledY_img = images
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            # Fondo de la celda
            pygame.draw.rect(screen, (255, 255, 255), rect)
            # Dibujar paredes y celdas llenas según corresponda
            if grid[row][col] == WALL:
                screen.blit(wall_img, rect)
            elif grid[row][col] == FILLED_X:
                screen.blit(filledX_img, rect)
            elif grid[row][col] == FILLED_Y:
                screen.blit(filledY_img, rect)
    # Dibujar a Longcat (la cabeza) en su posición actual (en píxeles)
    cat_rect = pygame.Rect(
        int(cat_pixel_pos[0]), int(cat_pixel_pos[1]), CELL_SIZE, CELL_SIZE
    )
    screen.blit(cat_img, cat_rect)


# --- Función para calcular el camino de movimiento ---
def get_movement_path(grid, cat_pos, direction):
    row, col = cat_pos
    drow, dcol = direction
    path = []
    while True:
        next_row = row + drow
        next_col = col + dcol
        # Verificar límites y obstáculo
        if next_row < 0 or next_row >= ROWS or next_col < 0 or next_col >= COLS:
            break
        if grid[next_row][next_col] != EMPTY:
            break
        path.append((next_row, next_col))
        row, col = next_row, next_col
    return path


# --- Función para verificar si Longcat está encerrado ---
def is_trapped(grid, cat_pos):
    row, col = cat_pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for drow, dcol in directions:
        new_row, new_col = row + drow, col + dcol
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            if grid[new_row][new_col] == EMPTY:
                return False
    return True


# --- Función de movimiento suave ---
def update_movement(cat_pixel_pos, target_pixel):
    x, y = cat_pixel_pos
    target_x, target_y = target_pixel

    if x != target_x:
        if abs(target_x - x) <= SPEED:
            x = target_x
        else:
            x += SPEED if target_x > x else -SPEED
    if y != target_y:
        if abs(target_y - y) <= SPEED:
            y = target_y
        else:
            y += SPEED if target_y > y else -SPEED

    reached = x == target_x and y == target_y
    return (x, y), reached


# --- Función para contar bloques ocupados ---
def count_filled_blocks(grid):
    count = 0
    for row in grid:
        for cell in row:
            if cell in (FILLED_X, FILLED_Y):
                count += 1
    return count


# --- Función que ejecuta un nivel y retorna el resultado ---
def run_level(screen, clock, font):
    images = load_images()
    grid = create_level()

    valid_positions = [
        (i, j)
        for i in range(1, ROWS - 1)
        for j in range(1, COLS - 1)
        if grid[i][j] == EMPTY
    ]
    if not valid_positions:
        print("No hay celdas disponibles para iniciar el juego.")
        pygame.quit()
        sys.exit()
    cat_grid_pos = random.choice(valid_positions)
    cat_pixel_pos = (cat_grid_pos[1] * CELL_SIZE, cat_grid_pos[0] * CELL_SIZE)

    moving = False
    current_path = []
    target_pixel = None
    move_direction = (0, 0)
    fill_type = FILLED_X

    running = True
    game_over = False
    game_result = None
    filled_blocks = 0
    percentage = 0.0

    while running:
        clock.tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not moving:
                if event.key == pygame.K_UP:
                    direction = (-1, 0)
                elif event.key == pygame.K_DOWN:
                    direction = (1, 0)
                elif event.key == pygame.K_LEFT:
                    direction = (0, -1)
                elif event.key == pygame.K_RIGHT:
                    direction = (0, 1)
                else:
                    direction = None

                if direction is not None:
                    path = get_movement_path(grid, cat_grid_pos, direction)
                    if len(path) == 0:
                        if is_trapped(grid, cat_grid_pos):
                            filled_blocks = count_filled_blocks(grid)
                            total_cells = (ROWS - 2) * (COLS - 2)
                            percentage = (filled_blocks / total_cells) * 100
                            game_over = True
                            if percentage >= 80:
                                game_result = "win"
                            else:
                                game_result = "lose"
                            running = False
                        else:
                            # Si no hay camino y no está atrapado, se ignora el input.
                            pass
                    else:
                        moving = True
                        current_path = path
                        move_direction = direction
                        fill_type = FILLED_X if direction[1] != 0 else FILLED_Y
                        next_cell = current_path[0]
                        target_pixel = (
                            next_cell[1] * CELL_SIZE,
                            next_cell[0] * CELL_SIZE,
                        )

        if moving:
            cat_pixel_pos, reached = update_movement(cat_pixel_pos, target_pixel)
            if reached:
                grid[cat_grid_pos[0]][cat_grid_pos[1]] = fill_type
                cat_grid_pos = current_path.pop(0)
                if current_path:
                    next_cell = current_path[0]
                    target_pixel = (next_cell[1] * CELL_SIZE, next_cell[0] * CELL_SIZE)
                else:
                    moving = False
                    if is_trapped(grid, cat_grid_pos):
                        filled_blocks = count_filled_blocks(grid)
                        total_cells = (ROWS - 2) * (COLS - 2)
                        percentage = (filled_blocks / total_cells) * 100
                        game_over = True
                        if percentage >= 80:
                            game_result = "win"
                        else:
                            game_result = "lose"
                        running = False

        screen.fill((0, 0, 0))
        draw_grid(screen, grid, cat_pixel_pos, images)

        # Actualizar y dibujar contador de porcentaje en la esquina superior derecha
        filled_blocks = count_filled_blocks(grid)
        total_cells = (ROWS - 2) * (COLS - 2)
        percentage = (filled_blocks / total_cells) * 100 if total_cells > 0 else 0
        text = font.render(f"{percentage:.1f}%", True, (255, 255, 255))
        text_rect = text.get_rect(topright=(WIDTH - 10, 10))

        # Fondo semi-transparente para el contador
        bg_surface = pygame.Surface(
            (text_rect.width + 10, text_rect.height + 10), pygame.SRCALPHA
        )
        bg_surface.fill((0, 0, 0, 128))
        screen.blit(bg_surface, (text_rect.left - 5, text_rect.top - 5))
        screen.blit(text, text_rect)

        pygame.display.flip()

    return game_result, filled_blocks, percentage


# --- Pantalla de Game Over con opción de reinicio ---
def draw_text_with_outline(
    surface, text, font, pos, text_color, outline_color, outline_width=2
):
    # Dibuja el texto con un contorno para mejorar su visibilidad
    x, y = pos
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                surface.blit(outline_surface, (x + dx, y + dy))
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, pos)


def show_game_over_screen(screen, clock, font, filled_blocks, percentage, game_result):
    # Se definen fuentes diferenciadas para el título y las instrucciones
    title_font = pygame.font.SysFont(None, 48)
    instr_font = pygame.font.SysFont(None, 36)

    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Fondo oscuro semi-transparente para centrar la atención en el mensaje
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Caja central con esquinas redondeadas y borde
        box_width, box_height = 850, 200
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2 - 30
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(screen, (30, 30, 30), box_rect, border_radius=20)
        pygame.draw.rect(screen, (200, 200, 200), box_rect, width=3, border_radius=20)

        # Mensaje principal con colores según el resultado
        if game_result == "win":
            msg = f"¡Ganaste! Bloques ocupados: {filled_blocks} - {percentage:.1f}% completado."
            text_color = (0, 255, 0)
        else:
            msg = f"¡Perdiste! Bloques ocupados: {filled_blocks} - {percentage:.1f}% completado."
            text_color = (255, 0, 0)

        title_surface = title_font.render(msg, True, text_color)
        title_rect = title_surface.get_rect(
            center=(WIDTH // 2, box_y + box_height // 2 - 30)
        )
        # Dibujar el texto con contorno para resaltarlo
        draw_text_with_outline(
            screen,
            msg,
            title_font,
            title_rect.topleft,
            text_color,
            (0, 0, 0),
            outline_width=2,
        )

        # Mensaje de instrucciones
        instr = "Presiona R para reiniciar o Q para salir."
        instr_surface = instr_font.render(instr, True, (255, 255, 255))
        instr_rect = instr_surface.get_rect(
            center=(WIDTH // 2, box_y + box_height // 2 + 40)
        )
        draw_text_with_outline(
            screen,
            instr,
            instr_font,
            instr_rect.topleft,
            (255, 255, 255),
            (0, 0, 0),
            outline_width=2,
        )

        pygame.display.flip()


# --- Bucle principal del juego ---
def main():
    global OBSTACLE_PROBABILITY
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Longcat")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    while True:
        game_result, filled_blocks, percentage = run_level(screen, clock, font)
        show_game_over_screen(
            screen, clock, font, filled_blocks, percentage, game_result
        )
        # Al reiniciar se incrementa OBSTACLE_PROBABILITY en 0.001
        OBSTACLE_PROBABILITY += 0.01


if __name__ == "__main__":
    main()
