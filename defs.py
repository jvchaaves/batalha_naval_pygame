import pygame
import cores

pygame.init()

def desenhar_botao(screen, cor, rect, raio_borda, largura_borda):
    pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=raio_borda)
    pygame.draw.rect(screen, cor, rect.inflate(-largura_borda*2, -largura_borda*2), border_radius=raio_borda)

def CreateGameGrid(rows, cols, cellsize, pos):
    startx, starty = pos
    cordGrid = []
    for row in range(rows):
        rowx = []
        for col in range(cols):
            rowx.append((startx, starty))
            startx += cellsize
        cordGrid.append(rowx)
        startx = pos[0]
        starty += cellsize
    return cordGrid

def render_player_ships(window, grid, logic, ship_types, rows, cols, ships_dict, ship_images_dict):
    drawn = set()
    for row in range(rows):
        for col in range(cols):
            if (row, col) in drawn:
                continue
            if logic[row][col] == 'S' and ship_types[row][col] != ' ':
                ship_name = ship_types[row][col]
                ship_size = ships_dict[ship_name]
                if col + ship_size <= cols:
                    if all(ship_types[row][col+i] == ship_name for i in range(ship_size)):
                        orientation = "H"
                        window.blit(ship_images_dict[ship_name][orientation], grid[row][col])
                        drawn.update((row, col+i) for i in range(ship_size))
                        continue
                if row + ship_size <= rows:
                    if all(ship_types[row+i][col] == ship_name for i in range(ship_size)):
                        orientation = "V"
                        window.blit(ship_images_dict[ship_name][orientation], grid[row][col])
                        drawn.update((row+i, col) for i in range(ship_size))

def updategamelogic(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def showgrid(window, background, imagem_explosao, cellsize, player1grid, player2grid, pgamelogic, p2gamelogic, ship_types_p1, ship_types_p2, ships, ship_images, rows, cols, show_ships):
    window.blit(background, (0, 0))

    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    font = pygame.font.SysFont('Arial', 24, bold=True)

    title1 = title_font.render('JOGADOR 1', True, cores.VermelhoVinho)
    window.blit(title1, (50, 15))
    title2 = title_font.render('JOGADOR 2', True, cores.VermelhoVinho)
    window.blit(title2, (1280 - (cols * cellsize) - 50, 15))

    for row in range(rows):
        letra = font.render(chr(65 + row), True, cores.Bege)
        window.blit(letra, (25, 80 + row * cellsize))
        window.blit(letra, (1280 - (cols * cellsize) - 85, 80 + row * cellsize))

    for col in range(cols):
        numero = font.render(str(col + 1), True, cores.Bege)
        window.blit(numero, (65 + col * cellsize, 570))
        window.blit(numero, (1280 - (cols * cellsize) - 50 + 50 + (col * cellsize) + cellsize // 2 - 60, 570))

    if show_ships:
        render_player_ships(window, player1grid, pgamelogic, ship_types_p1, rows, cols, ships, ship_images)
        render_player_ships(window, player2grid, p2gamelogic, ship_types_p2, rows, cols, ships, ship_images)

    for row in range(rows):
        for col in range(cols):
            if pgamelogic[row][col] == 'X':
                x, y = player1grid[row][col]
                window.blit(imagem_explosao, (x, y))
            elif p2gamelogic[row][col] == 'X':
                x, y = player2grid[row][col]
                window.blit(imagem_explosao, (x, y))
            elif pgamelogic[row][col] == 'A':
                x, y = player1grid[row][col]
                pygame.draw.circle(window, (0, 255, 255), (x + cellsize // 2, y + cellsize // 2), cellsize // 4)
            elif p2gamelogic[row][col] == 'A':
                x, y = player2grid[row][col]
                pygame.draw.circle(window, (0, 255, 255), (x + cellsize // 2, y + cellsize // 2), cellsize // 4)

    for grid in [player1grid, player2grid]:
        for row in grid:
            for x, y in row:
                pygame.draw.rect(window, cores.Branco, (x, y, cellsize, cellsize), 1)

def draw_chat(window, message, player):
    font = pygame.font.SysFont(None, 27)
    chat_rect = pygame.Rect(50, 650, 1180, 37)
    pygame.draw.rect(window, cores.Prata, chat_rect)
    chat_message = f"Jogador {player}: {message}"
    text_surface = font.render(chat_message, True, cores.Preto)
    window.blit(text_surface, (chat_rect.x + 10, chat_rect.y + 5))

def place_ship(window, grid, logic, ship_name, ship_size,ship_types_p1,ship_types_p2, player, orientation, player1grid, player2grid, pgamelogic, p2gamelogic, rows, cols, ships, ship_images, background, imagem_explosao, cellsize):
    while True:
        showgrid(window, background, imagem_explosao, cellsize, player1grid, player2grid, pgamelogic, p2gamelogic, ship_types_p1, ship_types_p2, ships, ship_images, rows, cols, True)
        draw_chat(window, f"[{orientation}] Posicione o {ship_name} (tamanho {ship_size}) (ESPAÇO para girar)", player)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    orientation = 'V' if orientation == 'H' else 'H'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for rowidx, row in enumerate(grid):
                    for colidx, (x, y) in enumerate(row):
                        if x <= mouse[0] <= x + cellsize and y <= mouse[1] <= y + cellsize:
                            selected_cells = []
                            valid = True
                            for i in range(ship_size):
                                r = rowidx + i if orientation == 'V' else rowidx
                                c = colidx + i if orientation == 'H' else colidx
                                if r >= rows or c >= cols or logic[r][c] != ' ':
                                    valid = False
                                    break
                                selected_cells.append((r, c))
                            if valid:
                                for r, c in selected_cells:
                                    logic[r][c] = 'S'
                                    if player == 1:
                                        ship_types_p1[r][c] = ship_name
                                    else:
                                        ship_types_p2[r][c] = ship_name
                                return
                            else:
                                draw_chat(window, "Posição inválida!", player)
                                pygame.display.update()
                                pygame.time.wait(1000)

def validate_manual_placement(cells):
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    if all(row == rows[0] for row in rows):
        return sorted(cols) == list(range(min(cols), max(cols) + 1))
    elif all(col == cols[0] for col in cols):
        return sorted(rows) == list(range(min(rows), max(rows) + 1))
    return False

def check_victory(opponent_logic):
    return not any(cell == 'S' for row in opponent_logic for cell in row)

def show_victory_screen(window, player):
    window.fill((0, 0, 0))
    pygame.display.update()
    font = pygame.font.SysFont("Arial", 80, bold=True)
    text = font.render(f"JOGADOR {player} VENCEU!", True, (255, 215, 0))
    text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)

def resize_ship_images(ship_images, cellsize, ships):
    for ship_name in ships:
        size = ships[ship_name]
        if ship_name in ship_images:
            ship_images[ship_name]["H"] = pygame.transform.scale(ship_images[ship_name]["H"], (cellsize * size, cellsize))
            ship_images[ship_name]["V"] = pygame.transform.scale(ship_images[ship_name]["V"], (cellsize, cellsize * size))

