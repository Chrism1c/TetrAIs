
    
def convert_to_pixel_coords(boxx, boxy):
    ### Converte le coordinate xy della board nelle corrispettive coordinate xy della loro locazione sullo schermo 
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))



def draw_box(boxx, boxy, color, pixelx=None, pixely=None):
    ### Disegna ogni singolo blocco (ogni tetramino ha 4 blocchi) alle coordinate xy della board. 
    ### Se pixelx & pixely sono avvalorati disegna quel pixel (next tetramino)
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx is None and pixely is None:
        pixelx, pixely = convert_to_pixel_coords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF,  COLORS[color],(pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    #pygame.draw.rect(DISPLAYSURF,  LIGHTCOLORS[color],(pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))



def draw_board(board):
    ### Disegna la board costrunendone il bordo, sfondo e le singole box (pixel) dei tetramini
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            draw_box(x, y, board[x][y])



def draw_status(score, level, best_move):

    ### Scrive le informazioni di gioco sullo schermo
    # draw the score text
    #randCol = random_color()
    score_surf = BASICFONT.render('# Lines: %s' % score, True, TEXTCOLOR)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(score_surf, score_rect)

    # draw the level text
    level_surf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(level_surf, level_rect)

    # draw the best_move text
    move_surf = BASICFONT.render('Current Move: %s' % best_move, True, TEXTCOLOR)
    move_rect = move_surf.get_rect()
    move_rect.topleft = (WINDOWWIDTH - 200, 80)
    DISPLAYSURF.blit(move_surf, move_rect)



def draw_piece(piece, pixelx=None, pixely=None):
    ### disegna un pezzo. Se pixelx e pixely non sono avvalorate usa le coordinate contenute in piece
    shape_to_draw = PIECES[piece['shape']][piece['rotation']]
    if pixelx is None and pixely is None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convert_to_pixel_coords(piece['x'], piece['y'])

    ### Disegna ogni box che compone il pezzo che vuole disegnare
    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shape_to_draw[y][x] != BLANK:
                draw_box(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))



def draw_next_piece(piece):
    #global GlobalNextPiece
    ### Disegan il prossimo tetramino sulla sideBar
    # draw the "next" text
    #GlobalNextPiece = piece
    #print("GlobalNextPiece = ",GlobalNextPiece)
    #time.sleep(2)

    #randCol = random_color()
    next_surf = BASICFONT.render('Next Tetromino:', True, TEXTCOLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOWWIDTH - 180, 160)
    DISPLAYSURF.blit(next_surf, next_rect)

    pygame.draw.rect(DISPLAYSURF, TEXTCOLOR,(485, 195, (4.2 * BOXSIZE) + 8,(4.2 * BOXSIZE) + 8), 5)

    # draw the "next" piece
    draw_piece(piece, pixelx=WINDOWWIDTH - 150, pixely=200)



def make_text_objs(text, font, color):
    ### Crea un oggetto testo definendone il colore e il font    
    surf = font.render(text, True, color)
    return surf, surf.get_rect()