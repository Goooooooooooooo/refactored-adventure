    #coding=utf-8

    import pygame
    import sys
    import random
    from pygame.locals import *
    from copy import deepcopy


    W = 800  #窗口宽度
    H = 600  #窗口高度
    size = (W, H)

    #分割窗口
    ROW = 30
    COL = 40

    #格子大小=蛇身子宽度
    cell_size = int(W / COL)

    snake_speed = 10
    #snake_color = (32,71,146)
    snake_color = (118,126,199)
    snake_body_color = (118,126,199)
    food_color = (254,254,254)
    bg_color = (14,14,14)

    #定义坐标
    class Point():
        row = 0
        col = 0
        def __init__(self, row, col):
            self.row = row
            self.col = col
        pass


    #开始信息显示
    def gamestart_info(screen):
        font = pygame.font.SysFont('', 40)
        tip = font.render('press the any key to start the game~', True, (65, 105, 225))
        gamestart = pygame.image.load('gamestart.jpg')
        screen.blit(gamestart, (85, 40))
        screen.blit(tip, (160, 550))
        pygame.display.update()

        while True:  #键盘监听事件
            for event in pygame.event.get():  # event handling loop
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_ESCAPE):
                        terminate()
                    else:
                        return

    #游戏结束信息显示
    def gameover_info(screen):
        font = pygame.font.SysFont('', 40)
        tip = font.render('Press Q or ESC to exit the game', True, (65, 105, 225))
        tip1 = font.render('press the space key to restart the game~', True, (65, 105, 225))
        overimg = pygame.image.load('gameover.jpg')
        screen.blit(overimg, (170, 80))
        screen.blit(tip, (170, 530))
        screen.blit(tip1, (135, 560))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        terminate() 
                    elif event.key == K_SPACE:
                        return True
    #画成绩
    def draw_score(screen,score):
        font = pygame.font.SysFont('', 30)
        scoreSurf = font.render('Score: %s' % score, True, (255,0,0))
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (W - 790, 20)
        screen.blit(scoreSurf, scoreRect)


    #程序终止
    def terminate():
        pygame.quit()
        sys.exit()

    #画线
    def draw_grid(screen):
        for x in range(0, W, cell_size):  # draw 水平 lines
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, H))
        for y in range(0, H, cell_size):  # draw 垂直 lines
            pygame.draw.line(screen, (40, 40, 40), (0, y), (W, y))

    #画图
    def rect(screen, point, color):
        cell_w = W / COL
        cell_h = H / ROW
        
        left = point.col * cell_w
        right = point.row * cell_h
        
        pygame.draw.rect(screen, color, (left, right, cell_w, cell_h))

    #食物随机生成，除蛇所在的坐标
    def food_Position(point):    
        while True:        
            is_coll = False        
            pos = Point(row=random.randint(0, ROW - 1), col=random.randint(0, COL - 1))
            for snake in point:
                if snake.row == pos.row and snake.col == snake.col:                
                    is_coll = True                
                    break        
            if not is_coll:
                break 
        return pos


    #蛇移动
    def snake_move(move, point):
        if move == 'left':
            point.col -= 1
        elif move == 'right':
            point.col += 1
        elif move == 'up':
            point.row -= 1
        elif move == 'down':
            point.row += 1
        return point

    def main():

        #蛇移动初始方向
        move = 'left'
        score = 0
        copy_snake = []
        
        #初始化蛇
        snake_head = Point(row=int(ROW/2), col=int(COL/2))
        snake_body = [
                    Point(row=snake_head.row, col=snake_head.col+1),
                    Point(row=snake_head.row, col=snake_head.col+2)
                ]
        
        #深度复制蛇坐标，在坐标以外，窗口范围内随机生成食物坐标
        copy_snake = deepcopy(snake_body)
        copy_snake.insert(0, snake_head)
        food = food_Position(copy_snake)
        
            
        while True:
            screen.fill(bg_color)
            pygame.draw.line(screen, (40, 40, 40), (0, 0), (W, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 273 or event.key == 119:
                        if move != 'down':
                            move = 'up'
                    if event.key == 274 or event.key == 115:
                        if move != 'up':
                            move = 'down'
                    if event.key == 276 or event.key == 97:
                        if move != 'right':
                            move = 'left'
                    if event.key == 275 or event.key == 100:
                        if move != 'left':
                            move = 'right'
            
            #移动
            snake_body.insert(0, Point(snake_head.row, snake_head.col))
            snake_head = snake_move(move, snake_head)
        
            #检测
            is_dead=False
            #蛇头撞墙
            if snake_head.col < 0 or snake_head.row < 0 or snake_head.col > COL or snake_head.row > ROW:
                is_dead = True
            #蛇头撞到蛇身
            for body in snake_body:        
                if snake_head.col==body.col and snake_head.row==body.row:       
                    is_dead = True            
                    break
            if is_dead:
                break  
            
            #判断是否吃到食物,吃到食物：重新生成食物
            eat=(snake_head.row==food.row and snake_head.col==food.col)
            if eat:
                copy_snake = deepcopy(snake_body)
                copy_snake.insert(0, snake_head)
                food = food_Position(copy_snake)
                score += 1
            if not eat:
                snake_body.pop() 
        
        #     #画网线
        #     draw_grid(screen)
        
            draw_score(screen,score)
            
            #画食物
            rect(screen, food, food_color)
            #画蛇
            rect(screen, snake_head, snake_color)
            for body in snake_body:
                rect(screen, body, snake_body_color)
            
            #pygame.display.flip()
            pygame.display.update()
            snake_speed_clock.tick(snake_speed)


    pygame.init() # 模块初始化
    snake_speed_clock = pygame.time.Clock() # 创建Pygame时钟对象
    screen = pygame.display.set_mode(size) #
    #设置标题    
    pygame.display.set_caption("Python Snake Game") 
    #填充背景颜色
    screen.fill(bg_color)
    pygame.mixer.music.load("snake.mp3")
    gamestart_info(screen)


    quit = True
    while quit:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
        main()
        quit = gameover_info(screen)



