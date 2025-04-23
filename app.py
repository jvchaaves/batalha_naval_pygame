import pygame
import cores  

pygame.init()

background = pygame.image.load(r'C:\Users\joaov\OneDrive\Área de Trabalho\programação\pygame\batalha_naval_pygame\background.jpg')  
background = pygame.transform.scale(background, (1280, 720))

def CreateGameGrid(rows, cols, cellsize, pos):
    startx = pos [0]
    starty = pos[1]
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

def updategamelogic(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def showgrid(window, cellsize, player1grid, player2grid, pgamelogic,p2gamelogic):
    
    window.blit(background,(0,0))
    
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    font = pygame.font.SysFont('Arial', 24, bold=  True)
    title1 = title_font.render('JOGADOR 1', True, cores.VermelhoVinho)
    window.blit(title1, (50, 15))
    title2 = title_font.render('JOGADOR 2', True, cores.VermelhoVinho)
    window.blit(title2, (1280 - (cols * cellsize) - 50, 15))

    for row in range(10):
        letra = font.render(chr(65 + row), True, cores.Bege)
        window.blit(letra, (25, 80 + row * cellsize))
    for col in range(10):
        numero = font.render(str(col + 1), True, cores.Bege)
        window.blit(numero, (65 + col * cellsize, 570))

    for row in range(10):
        letra = font.render(chr(65 + row), True, cores.Bege)
        window.blit(letra, (1280 - (cols * cellsize) - 85, 80 + row * cellsize))
    for col in range(10):
        numero = font.render(str(col + 1), True, cores.Bege)
        window.blit(numero, (1280 - (cols * cellsize) - 50 + 50 + (col * cellsize) + cellsize//2 - 60, 570))
    
    for row in range(rows):
        for col in range(cols):
            if pgamelogic[row][col] == 'S':
                x, y = player1grid[row][col]
                pygame.draw.rect(window, cores.Azul, (x, y, cellsize, cellsize))
            
            if p2gamelogic[row][col] == 'S':
                x, y = player2grid[row][col]
                pygame.draw.rect(window, cores.Verde, (x, y, cellsize, cellsize))

    
    for grid in [player1grid, player2grid]:
        for row in grid:
            for x, y in row:
                pygame.draw.rect(window, cores.Branco, (x, y, cellsize, cellsize), 1)

def printgamelogic(pgamelogic, p2gamelogic):
    print('player 1 grid'.center(50, '#'))
    for row in pgamelogic:
        print(row)
    print('player 2 grid'.center(50, '#'))
    for row in p2gamelogic:
        print(row)

def draw_chat(window, message, player):
    font = pygame.font.SysFont(None, 27)

    chat_rect = pygame.Rect(50, 650, 1180, 37)
    pygame.draw.rect(window, cores.Prata, chat_rect)

    chat_message = f"Jogador {player}: {message}"
    text_surface = font.render(chat_message, True, cores.Preto)
    window.blit(text_surface, (chat_rect.x + 10, chat_rect.y + 5))

def place_ship(grid, logic, ship_name, ship_size, player):
    print(f'Jogador {player}, posicione o {ship_name} (tamanho {ship_size}).')
    selected_cells = []
    
    while len(selected_cells) < ship_size:
        screen.fill(cores.AzulTurquesa)
        showgrid(screen, cellsize, pgamegrid, p2gamegrid, pgamelogic, p2gamelogic)
        draw_chat(screen, f'Posicione o {ship_name} (tamanho {ship_size}) - Selecione {ship_size} ', player)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                for rowidx, row in enumerate(grid):
                    for colidx, (x, y) in enumerate(row):
                        if x <= mouse[0] <= x + cellsize and y <= mouse[1] <= y + cellsize:
                            if logic[rowidx][colidx] == ' ':
                                if not selected_cells:
                                    selected_cells.append((rowidx, colidx))
                                    logic[rowidx][colidx] = 'S'
                                else:
                                    last_row, last_col = selected_cells[-1]
                                    same_row = rowidx == last_row and abs(colidx - last_col) == 1
                                    same_col = colidx == last_col and abs(rowidx - last_row) == 1
                                    
                                    if (same_row or same_col) and len(selected_cells) < ship_size:
                                        selected_cells.append((rowidx, colidx))
                                        logic[rowidx][colidx] = 'S'
                                    else:
                                        draw_chat(screen, "Selecione células adjacentes em linha reta!", player)
                                        pygame.display.update()
                                        pygame.time.wait(1000)
                            else:
                                draw_chat(screen, "Célula já ocupada!", player)
                                pygame.display.update()
                                pygame.time.wait(1000)
                            break

        if len(selected_cells) == ship_size:
            rows = [cell[0] for cell in selected_cells]
            cols = [cell[1] for cell in selected_cells]


            if not (all(r == rows[0] for r in rows) or all(c == cols[0] for c in cols)):
                draw_chat(screen, "Navio deve ser em linha reta horizontal ou vertical!", player)
                pygame.display.update()
                pygame.time.wait(1500)

                for row, col in selected_cells:
                    logic[row][col] = ' '
                selected_cells = []


def validate_manual_placement(cells):
   
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    if all(row == rows[0] for row in rows):  
        return sorted(cols) == list(range(min(cols), max(cols) + 1))
    elif all(col == cols[0] for col in cols): 
        return sorted(rows) == list(range(min(rows), max(rows) + 1))
    return False


ships = {"Porta-aviões": 5,"Couraçado": 4,"Cruzador": 3,"Submarino": 3,"Destroyer": 2}
cols= 10
rows = 10
cellsize = 50

screen = pygame.display.set_mode((1280, 720))

pgamegrid = CreateGameGrid(rows, cols, cellsize, (60, 70))
pgamelogic = updategamelogic(rows, cols)

p2gamegrid = CreateGameGrid(rows, cols, cellsize, (1280 - (rows * cellsize) - 60, 70))
p2gamelogic = updategamelogic(rows, cols)

printgamelogic(pgamelogic, p2gamelogic)

for player, (grid, logic) in enumerate([(pgamegrid, pgamelogic), (p2gamegrid, p2gamelogic)], start=1):
    for ship_name, ship_size in ships.items():
        place_ship(grid, logic, ship_name, ship_size, player)
        showgrid(screen, cellsize, pgamegrid, p2gamegrid,pgamelogic,p2gamelogic)
        pygame.display.update()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    showgrid(screen, cellsize, pgamegrid, p2gamegrid,p2gamelogic,pgamelogic)

for rowidx, row in enumerate(pgamegrid):
            for colidx, (x, y) in enumerate(row):
                if pgamelogic[rowidx][colidx] == 'X':
                    pygame.draw.line(screen, cores.Vermelho, (x, y), (x + cellsize, y + cellsize), 3)
                    pygame.draw.line(screen, cores.Vermelho, (x + cellsize, y), (x, y + cellsize), 3)

for rowidx, row in enumerate(p2gamegrid):
    for colidx, (x, y) in enumerate(row):
            if p2gamelogic[rowidx][colidx] == 'X':
                pygame.draw.line(screen, cores.Vermelho, (x, y), (x + cellsize, y + cellsize), 3)
                pygame.draw.line(screen, cores.Vermelho, (x + cellsize, y), (x, y + cellsize), 3)

    pygame.display.update()
    

pygame.quit()
