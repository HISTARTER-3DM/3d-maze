import pygame, sys, algorithm, time

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BACKGROUND = (20, 18, 25)
GREEN = (126, 255, 97)
ORANGE = (220, 135, 54)
PLAYER = (128, 128, 128)
CELL_MARGIN = 5

def drawMenu():
    masked_image, masked_image1, masked_image2 = loadImage()
    screen.blit(gameMenuTitle, (100, 100))
    screen.blit(masked_image, ((screen_info.current_w/3)-masked_image.get_width(), (screen_info.current_h/2)-masked_image.get_height()))
    screen.blit(masked_image1, (screen_info.current_w/3+(masked_image.get_width()/2), (screen_info.current_h/2)-masked_image.get_height()))
    screen.blit(masked_image2, ((screen_info.current_w/3)+(masked_image.get_width()*2), (screen_info.current_h/2)-masked_image.get_height()))
    screen.blit(easy, easyRect)
    screen.blit(medium, mediumRect)
    screen.blit(hard, hardRect)
    screen.blit(easyDescription, easyDescriptionRect)
    screen.blit(easy2Description, easy2DescriptionRect)
    screen.blit(mediumDescription, mediumDescriptionRect)
    screen.blit(medium2Description, medium2DescriptionRect)
    screen.blit(hardDescription, hardDescriptionRect)
    screen.blit(hard2Description, hard2DescriptionRect)

def drawMain():
    screen.blit(gameTitle, (100, 220))
    screen.blit(gameDescription, (100, 350))
    screen.blit(crew, (100, 400))
    screen.blit(moveNextForm, ((screen_info.current_w - moveNextForm.get_width())//2, screen_info.current_h - moveNextForm.get_height()*2))

def loadTexts():
    font200 = pygame.font.Font('./font/NeoDunggeunmoPro-Regular.ttf', 100)
    font50 = pygame.font.Font('./font/NeoDunggeunmoPro-Regular.ttf', 50)
    font36 = pygame.font.Font('./font/NeoDunggeunmoPro-Regular.ttf', 36)
    return font200, font50, font36

def loadImage():
    image = pygame.image.load('./data/5x5x5.jpg')
    image1 = pygame.image.load('./data/11x11x11.jpg')
    image2 = pygame.image.load('./data/17x17x17.jpg')
    scaled_image = pygame.transform.scale(image, (rect_size, rect_size))  # 정사각형 크기에 맞게 이미지 크기 조절
    scaled_image1 = pygame.transform.scale(image1, (rect_size, rect_size))  # 정사각형 크기에 맞게 이미지 크기 조절
    scaled_image2 = pygame.transform.scale(image2, (rect_size, rect_size))  # 정사각형 크기에 맞게 이미지 크기 조절
    mask_surface = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
    pygame.draw.rect(mask_surface, (255, 255, 255, 255), (0, 0, rect_size, rect_size))
    masked_image = scaled_image.copy()
    masked_image1 = scaled_image1.copy()
    masked_image2 = scaled_image2.copy()
    masked_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    masked_image1.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    masked_image2.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return masked_image, masked_image2, masked_image2

def runMaze(MAZE_SIZE):
    threeDimensionMaze = algorithm.RandomizedPrim_ThreeDimensionMaze(MAZE_SIZE)
    threeDimensionMazeData = threeDimensionMaze.render()
    cell_size = min(screen_info.current_w // MAZE_SIZE[2], screen_info.current_h // MAZE_SIZE[1])
    center_pos = (screen_info.current_w // 2, screen_info.current_h // 2)
    right_margin = (screen_info.current_w - (cell_size * MAZE_SIZE[1])) / 2
    minimap_cell_size = right_margin / MAZE_SIZE[2]
    minimap_height = minimap_cell_size * MAZE_SIZE[1]
    minimap_center_pos1 = (screen_info.current_w - right_margin / 2, minimap_height / 2)
    minimap_center_pos2 = (screen_info.current_w - right_margin / 2, minimap_height / 2 + minimap_height)
    square_x = 1
    square_y = 1
    square_z = 1
    last_move_time = 0
    DELAY = 0.2
    up_tile = pygame.image.load('./data/up_tile.png')
    up_tile = pygame.transform.scale(up_tile, (cell_size, cell_size))
    down_tile = pygame.image.load('./data/down_tile.png')
    down_tile = pygame.transform.scale(down_tile, (cell_size, cell_size))
    return threeDimensionMazeData, DELAY, square_x, square_y, square_z, cell_size, center_pos, minimap_cell_size, minimap_center_pos1, minimap_center_pos2, up_tile, down_tile, last_move_time

def render_maze(maze_data, z, screen, cell_size, center, player_pos, minimap=False):
    for yi, y in enumerate(maze_data[z]):
        for xi, x in enumerate(y):
            pos = get_pos(xi, yi, cell_size, center)
            if x == 1 or x == 3:
                pygame.draw.rect(screen, WHITE, pos)
            elif x == 10:
                pygame.draw.rect(screen, GREEN, pos)
            elif x == 11:
                pygame.draw.rect(screen, ORANGE, pos)
            if player_pos == (xi, yi):
                color = BLUE if minimap else PLAYER
                pygame.draw.rect(screen, color, pos)

def get_pos(x, y, cell_size, center):
    pos = (CELL_MARGIN / 2 + center[0] + (x - MAZE_SIZE[2] / 2) * cell_size, CELL_MARGIN / 2 + center[1] + (y - MAZE_SIZE[1] / 2) * cell_size, cell_size - CELL_MARGIN, cell_size - CELL_MARGIN)
    return pos

def render_hole(maze_data, z, screen, cell_size, center, up, down):
    for yi, y in enumerate(maze_data[z]):
        for xi, x in enumerate(y):
            pos = get_pos(xi, yi, cell_size, center)
            if maze_data[z - 1][yi][xi] == 3:
                screen.blit(down, pos[:2])
            if maze_data[z + 1][yi][xi] == 3:
                screen.blit(up, pos[:2])

def drawResult():
    gameResultTitle = font50.render('Game result', True, (255, 255, 255))
    gameResultLevel = font36.render('Level', True, (160, 160, 160))
    if level == 1:
        gameResultLevelData = font36.render('Easy', True, (255, 255, 255))
    elif level == 2:
        gameResultLevelData = font36.render('Medium', True, (255, 255, 255))
    elif level == 3:
        gameResultLevelData = font36.render('Hard', True, (255, 255, 255))
    else:
        gameResultLevelData = font36.render('Undi', True, (255, 255, 255))
    gameResultTime = font36.render('Total Time', True, (160, 160, 160))
    gameResultTimeResult = font36.render(str((endTime-startTime))+'s', True, (255, 255, 255))
    gameResultMoveCount = font36.render('move of count', True, (160, 160, 160))
    gameResultMoveCountData = font36.render(str(moveCount)+' times', True, (255, 255, 255))
    moveMenuForm = font50.render('<< Press any key to continue... >>', True, (160, 160, 160))
    screen.blit(gameResultTitle, ((screen_info.current_w-gameResultTitle.get_width())/2, screen_info.current_h/6))
    screen.blit(gameResultLevel, (screen_info.current_w/3, (screen_info.current_h/6)+100))
    screen.blit(gameResultTime, (screen_info.current_w/3, (screen_info.current_h/6)+150))
    screen.blit(gameResultMoveCount, (screen_info.current_w/3, (screen_info.current_h/6)+200))
    screen.blit(gameResultLevelData, ((screen_info.current_w/3)+400, (screen_info.current_h/6)+100))
    screen.blit(gameResultTimeResult, ((screen_info.current_w/3)+400, (screen_info.current_h/6)+150))
    screen.blit(gameResultMoveCountData, ((screen_info.current_w/3)+400, (screen_info.current_h/6)+200))
    screen.blit(moveMenuForm, ((screen_info.current_w-gameResultTitle.get_width()*3)/2, screen_info.current_h/1.2))

if __name__ == '__main__':
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("3D Maze")

    font200, font50, font36 = loadTexts()
    gameTitle = font200.render('3Dimensional Maze', True, (255, 255, 255))
    gameDescription = font36.render('3D and much more difficult than the existing 2D maze', True, (160, 160, 160))
    crew = font36.render('AnSungHyun, ParkJaeWon, HamJuHyuk', True, (201, 52, 31))
    moveNextForm = font50.render('<< Press any key to continue... >>', True, (160, 160, 160))

    gameMenuTitle = font50.render('3D Maze - Set difficulty', True, (255, 255, 255))
    easy = font50.render('Easy', True, (255, 255, 255))
    easyRect = easy.get_rect(topleft=((screen_info.current_w/3)-(easy.get_width()*2), (screen_info.current_h/2)+easy.get_height()))
    medium = font50.render('Medium', True, (255, 255, 255))
    mediumRect = medium.get_rect(topleft=((screen_info.current_w/3)+medium.get_width()*1.5, (screen_info.current_h/2)+medium.get_height()))
    hard = font50.render('Hard', True, (255, 255, 255))
    hardRect = hard.get_rect(topleft=((screen_info.current_w/3)+(hard.get_width()*7), (screen_info.current_h/2)+hard.get_height()))
    easyDescription = font36.render('For beginner', True, (160, 160, 160))
    easyDescriptionRect = easyDescription.get_rect(topleft=((screen_info.current_w/3)-(easyDescription.get_width()*1.3), (screen_info.current_h/2)+(easyDescription.get_height()*3)))
    easy2Description = font36.render('with size 5x5x5', True, (160, 160, 160))
    easy2DescriptionRect = easy2Description.get_rect(topleft=((screen_info.current_w/3)-(easy2Description.get_width()*1.2), (screen_info.current_h/2)+(easy2Description.get_height()*4)))
    mediumDescription = font36.render('For intermediate', True, (160, 160, 160))
    mediumDescriptionRect = mediumDescription.get_rect(topleft=((screen_info.current_w/3)+(mediumDescription.get_width()*0.6), (screen_info.current_h/2)+(mediumDescription.get_height()*3)))
    medium2Description = font36.render('with size 11x11x11', True, (160, 160, 160))
    medium2DescriptionRect = medium2Description.get_rect(topleft=((screen_info.current_w/3)+(medium2Description.get_width()*0.5), (screen_info.current_h/2)+(medium2Description.get_height()*4)))
    hardDescription = font36.render('For professionaluser', True, (160, 160, 160))
    hardDescriptionRect = hardDescription.get_rect(topleft=((screen_info.current_w/3)+(hardDescription.get_width()*1.8), (screen_info.current_h/2)+(hardDescription.get_height()*3)))
    hard2Description = font36.render('with size 17x17x17', True, (160, 160, 160))
    hard2DescriptionRect = hard2Description.get_rect(topleft=((screen_info.current_w/3)+(hard2Description.get_width()*2), (screen_info.current_h/2)+(hard2Description.get_height()*4)))
    screen_info = pygame.display.Info()
    rect_center = (screen_info.current_w // 2, screen_info.current_h // 2)
    rect_size = 300

    level = 0
    running = True
    isMadedMap = False
    screenType = 0
    MAZE_SIZE = 0, 0, 0
    startTime = 0
    endTime = 0
    moveCount = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
        screen.fill(BACKGROUND)
        if screenType == 0:
            drawMain()
        elif screenType == 1:
            startTime = time.time()
            moveCount = 0
            drawMenu()
        elif screenType == 2:
            if not isMadedMap:
                threeDimensionMazeData, DELAY, square_x, square_y, square_z, cell_size, center_pos, minimap_cell_size, minimap_center_pos1, minimap_center_pos2, up_tile, down_tile, last_move_time = runMaze(MAZE_SIZE)
                isMadedMap = True
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] and time.time() - last_move_time > DELAY) and (threeDimensionMazeData[square_z][square_y][square_x - 1] != 0):
                square_x -= 1
                last_move_time = time.time()
                moveCount += 1
            elif (keys[pygame.K_RIGHT] and time.time() - last_move_time > DELAY) and (threeDimensionMazeData[square_z][square_y][square_x + 1] != 0):
                square_x += 1
                last_move_time = time.time()
                moveCount += 1
            elif (keys[pygame.K_UP] and time.time() - last_move_time > DELAY) and (threeDimensionMazeData[square_z][square_y - 1][square_x] != 0):
                square_y -= 1
                last_move_time = time.time()
                moveCount += 1
            elif (keys[pygame.K_DOWN] and time.time() - last_move_time > DELAY) and (threeDimensionMazeData[square_z][square_y + 1][square_x] != 0):
                square_y += 1
                last_move_time = time.time()
                moveCount += 1
            elif (keys[pygame.K_LCTRL] and time.time() - last_move_time > DELAY) and (threeDimensionMazeData[square_z - 1][square_y][square_x] != 0):
                square_z -= 2
                last_move_time = time.time()
                moveCount += 1
            elif (keys[pygame.K_LSHIFT] and time.time() - last_move_time > DELAY) and (threeDimensionMazeData[square_z + 1][square_y][square_x] != 0):
                square_z += 2
                last_move_time = time.time()
                moveCount += 1

            if square_x == MAZE_SIZE[2] - 2 and square_y == MAZE_SIZE[1] - 2 and square_z == MAZE_SIZE[0] - 2:
                endTime = time.time()
                screenType = 3
                isMadedMap = False
            screen.fill(BACKGROUND)
            player_pos = (square_x, square_y)
            render_maze(threeDimensionMazeData, square_z, screen, cell_size, center_pos, player_pos)
            if square_z > 1:
                render_maze(threeDimensionMazeData, square_z - 2, screen, minimap_cell_size, minimap_center_pos2, player_pos, True)
            if square_z < MAZE_SIZE[0] - 2:
                render_maze(threeDimensionMazeData, square_z + 2, screen, minimap_cell_size, minimap_center_pos1, player_pos, True)
            square_pos = get_pos(square_x, square_y, cell_size, center_pos)
            render_hole(threeDimensionMazeData, square_z, screen, cell_size, center_pos, up_tile, down_tile)
        elif screenType == 3: 
            drawResult()

        if screenType != 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (event.type == pygame.KEYDOWN and screenType == 0) or (event.type == pygame.KEYDOWN and screenType == 3):
                    screenType = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    x, y = event.pos
                    if easyRect.collidepoint(x, y) or easyDescriptionRect.collidepoint(x, y) or easy2DescriptionRect.collidepoint(x, y):
                        screenType = 2
                        level = 1
                        MAZE_SIZE = 5, 5, 5
                    elif mediumRect.collidepoint(x, y) or mediumDescriptionRect.collidepoint(x, y) or medium2DescriptionRect.collidepoint(x, y):
                        screenType = 2
                        level = 2
                        MAZE_SIZE = 11, 11, 11
                    elif hardRect.collidepoint(x, y) or hardDescriptionRect.collidepoint(x, y) or hard2DescriptionRect.collidepoint(x, y):
                        screenType = 2
                        level = 3
                        MAZE_SIZE = 17, 17, 17
        pygame.display.update()
    pygame.quit()
    sys.exit()