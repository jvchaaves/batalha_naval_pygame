import pygame
import cores  

pygame.init()

pygame.mixer.music.load("batalha_naval_pygame/musicas/musica_de_fundo.mp3")
pygame.mixer.music.set_volume(0.2)  
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Batalha Naval')

fonte = pygame.font.Font('batalha_naval_pygame/fonts/CHEDROS Regular.ttf', 72)
fonte2 = pygame.font.Font('batalha_naval_pygame/fonts/CHEDROS Regular.ttf', 18)

texto1 = fonte.render('COMEÇAR', True, (255, 255, 255))
texto2 = fonte.render('CONFIGURAÇÕES', True, (255, 255, 255))
texto3 = fonte2.render('um trabalho feito por: Nathan David, João Rafael, João Vitor Chaves e Diego Sousa', True, (255, 255, 255))

tamanhof_1 = 20
tamanhof_2 = 10

rect_texto1 = texto1.get_rect(topleft=(60, 520))
rect_texto2 = texto2.get_rect(topleft=(60, 620))

rect_texto1 = pygame.Rect(rect_texto1.left - tamanhof_1, rect_texto1.top - tamanhof_2, rect_texto1.width + 2 * tamanhof_1, rect_texto1.height + 2 * tamanhof_2)
rect_texto2 = pygame.Rect(rect_texto2.left - tamanhof_1, rect_texto2.top - tamanhof_2, rect_texto2.width + 2 * tamanhof_1, rect_texto2.height + 2 * tamanhof_2)
rect_texto3 = texto3.get_rect(topleft=(770, 700))

texto1_pos = texto1.get_rect(center=rect_texto1.center)
texto2_pos = texto2.get_rect(center=rect_texto2.center)

img = pygame.image.load('batalha_naval_pygame/images/capa.jpg').convert_alpha()
img = pygame.transform.scale(img, (1280, 720))

cor_fundo_botao = (100, 50, 16)
cor_fundo_botao_m = (80, 40, 6)
raio_borda = 20
largura_borda = 5

def desenhar_botao(screen, cor, rect, raio_borda, largura_borda):
    pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=raio_borda)
    pygame.draw.rect(screen, cor, rect.inflate(-largura_borda*2, -largura_borda*2), border_radius=raio_borda)


menu_ativo = True
while menu_ativo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if rect_texto1.collidepoint(mouse_x, mouse_y):
                menu_ativo = False

            if rect_texto2.collidepoint(mouse_x, mouse_y):
                print("Você clicou em CONFIGURAÇÕES!")

    screen.blit(img, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()

    desenhar_botao(screen, cor_fundo_botao_m if rect_texto1.collidepoint(mouse_x, mouse_y) else cor_fundo_botao, rect_texto1, raio_borda, largura_borda)
    desenhar_botao(screen, cor_fundo_botao_m if rect_texto2.collidepoint(mouse_x, mouse_y) else cor_fundo_botao, rect_texto2, raio_borda, largura_borda)

    screen.blit(texto1, texto1_pos)
    screen.blit(texto2, texto2_pos)
    screen.blit(texto3, rect_texto3)
    pygame.display.update()

#====================================================== JOGO COMEÇA AQUI ================================================================


background = pygame.image.load("batalha_naval_pygame/images/background.jpg") 
background = pygame.transform.scale(background, (1280, 720))

cellsize = 50

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Batalha Naval')

imagem_explosao = pygame.image.load("batalha_naval_pygame/images/explosão.png")
imagem_explosao = pygame.transform.scale(imagem_explosao, (cellsize, cellsize))
explosao_sound = pygame.mixer.Sound("batalha_naval_pygame/musicas/explosao.mp3")
explosao_sound.set_volume(0.05)


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

def showgrid(window, cellsize, player1grid, player2grid, pgamelogic, p2gamelogic, rows, cols):
    
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
    
    drawn_cells = set()
    for row in range(rows):
        for col in range(cols):
            if pgamelogic[row][col] == 'S' and (row, col) not in drawn_cells:
                ship_name = ship_types_p1[row][col]
                ship_size = ships[ship_name]
                x, y = player1grid[row][col]

                is_horizontal = False
                is_vertical = False
                
                if col + ship_size - 1 < cols:
                    if all(pgamelogic[row][col+i] == 'S' for i in range(ship_size)):
                        is_horizontal = True
    
                if not is_horizontal and row + ship_size - 1 < rows:
                    if all(pgamelogic[row+i][col] == 'S' for i in range(ship_size)):
                        is_vertical = True
                
                if is_horizontal:
                    orientation = "H"
                    ship_cells = [(row, col+i) for i in range(ship_size)]
                    window.blit(ship_images[ship_name][orientation], (x, y))
                    drawn_cells.update(ship_cells)
                elif is_vertical:
                    orientation = "V"
                    ship_cells = [(row+i, col) for i in range(ship_size)]
                    window.blit(ship_images[ship_name][orientation], (x, y))
                    drawn_cells.update(ship_cells)

    drawn_cells.clear()
    for row in range(rows):
        for col in range(cols):
            if p2gamelogic[row][col] == 'S' and (row, col) not in drawn_cells:
                ship_name = ship_types_p2[row][col]
                ship_size = ships[ship_name]
                x, y = player2grid[row][col]
                
                is_horizontal = False
                is_vertical = False
                
                if col + ship_size - 1 < cols:
                    if all(p2gamelogic[row][col+i] == 'S' for i in range(ship_size)):
                        is_horizontal = True
                
                if not is_horizontal and row + ship_size - 1 < rows:
                    if all(p2gamelogic[row+i][col] == 'S' for i in range(ship_size)):
                        is_vertical = True
                
                if is_horizontal:
                    orientation = "H"
                    ship_cells = [(row, col+i) for i in range(ship_size)]
                    window.blit(ship_images[ship_name][orientation], (x, y))
                    drawn_cells.update(ship_cells)
                elif is_vertical:
                    orientation = "V"
                    ship_cells = [(row+i, col) for i in range(ship_size)]
                    window.blit(ship_images[ship_name][orientation], (x, y))
                    drawn_cells.update(ship_cells)
    
    for row in range(rows):
        for col in range(cols):
            if pgamelogic[row][col] == 'X':
                x, y = player1grid[row][col]
                window.blit(imagem_explosao, (x, y)) 


            if p2gamelogic[row][col] == 'X':
                x, y = player2grid[row][col]
                window.blit(imagem_explosao, (x, y))
    
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

orientation = "H"

def place_ship(grid, logic, ship_name, ship_size, player):
    global orientation
    print(f'Jogador {player}, posicione o {ship_name} (tamanho {ship_size}).')

    while True:
        showgrid(screen, cellsize, pgamegrid, p2gamegrid, pgamelogic, p2gamelogic, rows, cols)
        draw_chat(screen, f"[{orientation}] Posicione o {ship_name} (tamanho {ship_size}) (espaço para rotacionar o navio)", player)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    orientation = 'V' if orientation == 'H' else 'H'
                    print(f"Orientação agora: {orientation}") 
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
                                draw_chat(screen, "Posição inválida! Fora da grade ou sobreposição.", player)
                                pygame.display.update()
                                pygame.time.wait(1000)
                            break
def validate_manual_placement(cells):
   
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    if all(row == rows[0] for row in rows):  
        return sorted(cols) == list(range(min(cols), max(cols) + 1))
    elif all(col == cols[0] for col in cols): 
        return sorted(rows) == list(range(min(rows), max(rows) + 1))
    return False

def check_victory(player_logic):

    for row in player_logic:
        for cell in row:
            if cell == 'S':
                return False
    return True

def show_victory_screen(window, player):

    window.fill((0, 0, 0))
    pygame.display.update()

    font = pygame.font.SysFont("Arial", 80, bold=True)
    text = font.render(f"JOGADOR {player} VENCEU!", True, (255, 215, 0))
    text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))

    for alpha in range(0, 256, 5):
        window.fill((0, 0, 0))
        text.set_alpha(alpha)
        window.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(20)

    pygame.time.wait(3000)

def resize_ship_images():
    for ship_name in ships:  
        size = ships[ship_name]
        if ship_name in ship_images:
            img_h = ship_images[ship_name]["H"]
            new_width = cellsize * size
            new_height = cellsize
            ship_images[ship_name]["H"] = pygame.transform.scale(img_h, (new_width, new_height))
            
            img_v = ship_images[ship_name]["V"]
            new_width = cellsize
            new_height = cellsize * size
            ship_images[ship_name]["V"] = pygame.transform.scale(img_v, (new_width, new_height))


ship_images = {
    "Submarino": {
        "H": pygame.image.load("batalha_naval_pygame/images/barco 2 horizontal.jpg").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("batalha_naval_pygame/images/barco 2 horizontal.jpg").convert_alpha(), -90)
    },
    "Destroyer": {
        "H": pygame.image.load("batalha_naval_pygame/images/barco 1 horizontal.jpg").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("batalha_naval_pygame/images/barco 1 horizontal.jpg").convert_alpha(), -90)
        },
    "Cruzador": {
        "H": pygame.image.load("batalha_naval_pygame/images/barco 3 horizontal.jpg").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("batalha_naval_pygame/images/barco 3 horizontal.jpg").convert_alpha(), -90) 
        },
    "Couraçado": {
        "H": pygame.image.load("batalha_naval_pygame/images/barco 4 horizontal.jpg").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("batalha_naval_pygame/images/barco 4 horizontal.jpg").convert_alpha(), -90)
        },
    "Porta-aviões": {
        "H": pygame.image.load("batalha_naval_pygame/images/barco 5 horizontal.jpg").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("batalha_naval_pygame/images/barco 5 horizontal.jpg").convert_alpha(), -90)
        },
    
}

ships = {"Porta-aviões": 5,"Couraçado": 4,"Cruzador": 3,"Submarino": 3,"Destroyer": 2}

resize_ship_images()

cols= 10
rows = 10
cellsize = 50

pgamelogic = updategamelogic(rows, cols)
ship_types_p1 = updategamelogic(rows, cols)

p2gamelogic = updategamelogic(rows, cols)
ship_types_p2 = updategamelogic(rows, cols)
pgamelogic = updategamelogic(rows, cols)

pgamegrid = CreateGameGrid(rows, cols, cellsize, (60, 70))
p2gamegrid = CreateGameGrid(rows, cols, cellsize, (1280 - (rows * cellsize) - 60, 70))
p2gamelogic = updategamelogic(rows, cols)

printgamelogic(pgamelogic, p2gamelogic)

for player, (grid, logic) in enumerate([(pgamegrid, pgamelogic), (p2gamegrid, p2gamelogic)], start=1):
    for ship_name, ship_size in ships.items():
        place_ship(grid, logic, ship_name, ship_size, player)
        showgrid(screen, cellsize, pgamegrid, p2gamegrid,pgamelogic,p2gamelogic, rows, cols)
        pygame.display.update()

message = "Clique para Atirar!"
current_player = 1

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if current_player == 1:
                target_grid = p2gamegrid  
                target_logic = p2gamelogic
                player_grid = pgamegrid 
            
            else:
                target_grid = pgamegrid 
                target_logic = pgamelogic
                player_grid = p2gamegrid 
    
            for rowidx, row in enumerate(target_grid):
                for colidx, (x, y) in enumerate(row):
                    if x <= mouse[0] <= x + cellsize and y <= mouse[1] <= y + cellsize:
                        if target_logic[rowidx][colidx] == 'S':
                            target_logic[rowidx][colidx] = 'X'
                            explosao_sound.play()
                            draw_chat(screen, f"Jogador {current_player} acertou!", current_player)
                        elif target_logic[rowidx][colidx] == ' ': 
                            target_logic[rowidx][colidx] = 'A'
                            explosao_sound.play()
                            draw_chat(screen, f"Jogador {current_player} errou. Troca de jogador!", current_player)
                            current_player = 2 if current_player == 1 else 1 

                        pygame.display.update()  
                        pygame.time.wait(200)  
                        break 

        showgrid(screen, cellsize, pgamegrid, p2gamegrid, pgamelogic, p2gamelogic, rows, cols)

    if check_victory(pgamelogic):
        show_victory_screen(screen, 1)
        break 
    elif check_victory(p2gamelogic):
        show_victory_screen(screen, 2)
        break 

    font = pygame.font.SysFont(None, 27)
    display_message = f"É a vez do Jogador {current_player}. {message}"
    chat_rect = pygame.Rect(50, 650, 1180, 37)
    pygame.draw.rect(screen, cores.Prata, chat_rect)
    text_surface = font.render(display_message, True, cores.Preto)
    screen.blit(text_surface, (chat_rect.x + 10, chat_rect.y + 5))

    pygame.display.update()

pygame.quit()