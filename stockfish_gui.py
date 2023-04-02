from stockfish import Stockfish
from chessboard import display
import pygame
import math

stockfish = Stockfish('stockfish-windows-2022-x86-64-avx2.exe')
stockfish.set_elo_rating(1350)

#add custom event for fingers open and fingers closed (PYGAME USEREVENT=24/32)
closed = pygame.USEREVENT+0
open = pygame.USEREVENT+1
ascii_to_num = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6, 'h' : 7}
all_squares = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 
'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 
'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'
'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 
'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 
'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 
'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8']


#initialise display
X = 800
Y = 800
scrn = pygame.display.set_mode((X, Y))
pygame.init()

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)
GREEN = (79, 121, 66) # foresty

#load piece images
pieces = {'BLACK_PAWN': pygame.image.load('b_pawn.png').convert(),
          'BLACK_KNIGHT': pygame.image.load('b_knight.png').convert(),
          'BLACK_BISHOP': pygame.image.load('b_bishop.png').convert(),
          'BLACK_ROOK': pygame.image.load('b_rook.png').convert(),
          'BLACK_QUEEN': pygame.image.load('b_queen.png').convert(),
          'BLACK_KING': pygame.image.load('b_king.png').convert(),
          'WHITE_PAWN': pygame.image.load('w_pawn.png').convert(),
          'WHITE_KNIGHT': pygame.image.load('w_knight.png').convert(),
          'WHITE_BISHOP': pygame.image.load('w_bishop.png').convert(),
          'WHITE_ROOK': pygame.image.load('w_rook.png').convert(),
          'WHITE_QUEEN': pygame.image.load('w_queen.png').convert(),
          'WHITE_KING': pygame.image.load('w_king.png').convert(),
          }

def update(scrn, stockfish):
    '''
    updates the screen based on Stockfish class
    ''' 
    for s in all_squares:
        # piece = board.piece_at(i)
        piece = stockfish.get_what_is_on_square(s).name
        if piece == None:
            pass
        else:
            scrn.blit(pieces[str(piece)], 100* ascii_to_num.get(s[0:1]), 100*(8-s[1:2]))
    
    for i in range(7):
        i=i+1
        pygame.draw.line(scrn,WHITE,(0,i*100),(800,i*100))
        pygame.draw.line(scrn,WHITE,(i*100,0),(i*100,800))

    pygame.display.flip()

def gui(stockfish, fingerState1, fingerState2, index):

    #make background Green
    scrn.fill(GREEN)
    #name window
    pygame.display.set_caption('Chess')

    status = True
    while (status):
        #update screen
        update(scrn,stockfish)
        if(fingerState1):
            pygame.event.post(closed)
        if(fingerState2):
            pygame.event.post(open)

        for event in pygame.event.get():
     
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                status = False

            # if piece picked up
            if event.type == pygame.closed:
                #remove previous highlights
                scrn.fill(GREEN)
                # get index of piece being picked up from other code
                # show possible moves
                #check the square that is clicked
                piece = stockfish.get_what_is_on_square(index).name
                #can say stuff here
                pieceX = 100*(ascii_to_num.get(index[0:1]))
                pieceY = 100*(8-index[1:2])
                pygame.draw.rect(scrn,BLUE,pygame.Rect(pieceX,pieceY,100,100),5)
                #if empty pass
                if piece == None:
                    pass
                else:
                    #figure out valid moves this piece can make
                    # all_squares = list of strings of all squares
                    all_squares = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 
                    'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 
                    'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'
                    'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 
                    'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 
                    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 
                    'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8']
                    for m in all_squares:
                        if(stockfish.is_move_correct(index + m)):
                            TX1 = 100*(ascii_to_num.get(index[0:1])) # a = 0, h = 7, so first coordinate = ascii conversion from
                            TY1 = 100*(8-index[1:2]) # 8 = 0, 1 = 7, so second coordinate = 8-y
                            #highlight squares it can move to
                            pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
            # if we are moving a piece
            if event.type == pygame.open:
                newIndex = 'a1'
                stockfish.make_moves_from_current_position(index + newIndex)
            index = None
    pygame.quit()

gui(stockfish, closed, open)
