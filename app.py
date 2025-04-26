import pygame
import cores
import defs

pygame.init()



pygame.mixer.music.load("musicas/musica_de_fundo.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Batalha Naval')


fonte = pygame.font.Font('fonts/CHEDROS Regular.ttf', 72)
fonte2 = pygame.font.Font('fonts/CHEDROS Regular.ttf', 18)


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


img = pygame.image.load('images/capa.jpg').convert_alpha()
img = pygame.transform.scale(img, (1280, 720))

cor_fundo_botao = (100, 50, 16)
cor_fundo_botao_m = (80, 40, 6)
raio_borda = 20
largura_borda = 5


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

    defs.desenhar_botao(screen, cor_fundo_botao_m if rect_texto1.collidepoint(mouse_x, mouse_y) else cor_fundo_botao, rect_texto1, raio_borda, largura_borda)
    defs.desenhar_botao(screen, cor_fundo_botao_m if rect_texto2.collidepoint(mouse_x, mouse_y) else cor_fundo_botao, rect_texto2, raio_borda, largura_borda)
    screen.blit(texto1, texto1_pos)
    screen.blit(texto2, texto2_pos)
    screen.blit(texto3, rect_texto3)
    pygame.display.update()

#====================================================== JOGO COMEÇA AQUI ================================================================


background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (1280, 720))
imagem_explosao = pygame.image.load("images/explosão.png")
imagem_explosao = pygame.transform.scale(imagem_explosao, (50, 50))
explosao_sound = pygame.mixer.Sound("musicas/explosao.mp3")
explosao_sound.set_volume(0.05)


cellsize = 50
rows, cols = 10, 10


pgamegrid = defs.CreateGameGrid(rows, cols, cellsize, (60, 70))
p2gamegrid = defs.CreateGameGrid(rows, cols, cellsize, (1280 - (rows * cellsize) - 60, 70))
pgamelogic = defs.updategamelogic(rows, cols)
p2gamelogic = defs.updategamelogic(rows, cols)
ship_types_p1 = defs.updategamelogic(rows, cols)
ship_types_p2 = defs.updategamelogic(rows, cols)


ships = {"Porta-aviões": 5, "Couraçado": 4, "Cruzador": 3, "Submarino": 3, "Destroyer": 2}
ship_images = {
    "Submarino": {
        "H": pygame.image.load("images/barco 2 horizontal png.png").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("images/barco 2 horizontal png.png").convert_alpha(), -90)
    },
    "Destroyer": {
        "H": pygame.image.load("images/barco 1 horizontal png.png").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("images/barco 1 horizontal png.png").convert_alpha(), -90)
    },
    "Cruzador": {
        "H": pygame.image.load("images/barco 3 horizontal png.png").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("images/barco 3 horizontal png.png").convert_alpha(), -90)
    },
    "Couraçado": {
        "H": pygame.image.load("images/barco 4 horizontal png.png").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("images/barco 4 horizontal png.png").convert_alpha(), -90)
    },
    "Porta-aviões": {
        "H": pygame.image.load("images/barco 5 horizontal png.png").convert_alpha(),
        "V": pygame.transform.rotate(pygame.image.load("images/barco 5 horizontal png.png").convert_alpha(), -90)
    }
}
defs.resize_ship_images(ship_images, cellsize, ships)


orientation = "H"
for player, (grid, logic, ship_types) in enumerate([(pgamegrid, pgamelogic, ship_types_p1), (p2gamegrid, p2gamelogic, ship_types_p2)], start=1):
    for ship_name, ship_size in ships.items():
        defs.place_ship(screen,grid, logic, ship_name, ship_size,ship_types_p1,ship_types_p2
, player,orientation, pgamegrid, p2gamegrid, pgamelogic, p2gamelogic, rows, cols, ships,
ship_images, background, imagem_explosao, cellsize)
        pygame.display.update()

show_ships = False
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
            else:
                target_grid = pgamegrid
                target_logic = pgamelogic

            for rowidx, row in enumerate(target_grid):
                for colidx, (x, y) in enumerate(row):
                    if x <= mouse[0] <= x + cellsize and y <= mouse[1] <= y + cellsize:
                        if target_logic[rowidx][colidx] == 'S':
                            target_logic[rowidx][colidx] = 'X'
                            explosao_sound.play()
                            defs.draw_chat(screen, "Acertou!", current_player)
                        elif target_logic[rowidx][colidx] == ' ':
                            target_logic[rowidx][colidx] = 'A'
                            explosao_sound.play()
                            defs.draw_chat(screen, "Errou! Troca de jogador.", current_player)
                            current_player = 2 if current_player == 1 else 1

                        pygame.display.update()
                        pygame.time.wait(200)
                        break

    defs.showgrid(screen, background, imagem_explosao, cellsize,
                  pgamegrid, p2gamegrid, pgamelogic, p2gamelogic,
                  ship_types_p1, ship_types_p2, ships, ship_images,
                  rows, cols, show_ships)

    if current_player == 1 and defs.check_victory(p2gamelogic):
        defs.show_victory_screen(screen, 1)
        break
    elif current_player == 2 and defs.check_victory(pgamelogic):
        defs.show_victory_screen(screen, 2)
        break

    font = pygame.font.SysFont(None, 27)
    chat_rect = pygame.Rect(50, 650, 1180, 37)
    pygame.draw.rect(screen, cores.Prata, chat_rect)
    display_message = f"É a vez do Jogador {current_player}. {message}"
    text_surface = font.render(display_message, True, cores.Preto)
    screen.blit(text_surface, (chat_rect.x + 10, chat_rect.y + 5))

    pygame.display.update()

pygame.quit()
