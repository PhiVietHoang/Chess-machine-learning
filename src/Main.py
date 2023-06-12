from turtle import width
import pygame as p
from sys import exit

from pyparsing import col
import ChessEngine
import SmartMove

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 120
IMAGES = {}

def loadImages():
	pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE));

def main():
	p.init()
	screen = p.display.set_mode((WIDTH, HEIGHT))
	p.display.set_caption('Chess')
	clock = p.time.Clock()
	screen.fill(p.Color('white'))
	gs = ChessEngine.GameState()
	validMoves = gs.getValidMoves()
	moveMade = False #flag variable for when a move is made
	animate = False
	loadImages() #only do this once, before the while loop
	sqSelected = () #keep track of the last click of the user (row, column)
	playerClicks = [] #keep track of player click [sqSelected, sqSelected]
	gameOver = False
	player1 = True
	player2 = False
	while True:
		humanTurn = (gs.whiteToMove and player1) or (not gs.whiteToMove and player2)
		for e in p.event.get():
			if e.type == p.QUIT:
				p.quit()
				exit()
			#mouse handler
			elif e.type == p.MOUSEBUTTONDOWN:
				if not gameOver and humanTurn:
					location = p.mouse.get_pos()
					col = location[0]//SQ_SIZE
					row = location[1]//SQ_SIZE
					if sqSelected == (row, col): #user clicked the same square
						sqSelected = () #deselect
						playerClicks = [] #clear player clicks
					else:
						sqSelected = (row, col)
						playerClicks.append(sqSelected)
					if len(playerClicks) == 2: #after 2nd click
						move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
						for i in range(len(validMoves)):
							if move == validMoves[i]:
								gs.makeMove(validMoves[i])
								print('Move made: ' + move.getChessNotation())
								print('Enpassant possible square: ' + str(gs.enpassantPossible))
								moveMade = True
								animate = True
								sqSelected = ()
								playerClicks = []
						if not moveMade:
							playerClicks = [sqSelected]
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z: #when 'z' is pressed
					gs.undoMove() 
					gs.undoMove() 
					moveMade = True
					animate = False
				if e.key == p.K_r:
					gs=ChessEngine.GameState()
					validMoves = gs.getValidMoves()
					sqSelected=()
					playerClicks=[]
					moveMade = False
					animate = False

		if not gameOver and not humanTurn:
			AIMove = SmartMove.findBestMoveAlphaBetaPrunning(gs,validMoves)
			"""
      		Choose algorithm:
			SmartMove.findBestMoveGreedy(gs,validMoves) 				#Greedy algorithm
			SmartMove.findBestMoveMinMax(gs,validMoves) 				#Minimax Algorithm
			SmartMove.findBestMoveNegaMax(gs,validMoves) 				#Negamax Algorithm
			SmartMove.findBestMoveAlphaBetaPrunning(gs,validMoves) 		#AlphaBeta prunning algorithm
			"""
			if AIMove is None:
				AIMove = SmartMove.findRandomMove(validMoves)
			gs.makeMove (AIMove)
			moveMade = True
			animate = True
     
     
		if moveMade: 
			if animate:
				animateMove (gs.moveLog[-1], screen, gs.board, clock)
			validMoves = gs.getValidMoves()
			moveMade = False
			animate = False
		drawGameState(screen, gs, validMoves, sqSelected)
		if gs.checkMate:
			gameOver=True
			if gs.whiteToMove:
				drawText(screen, 'Black is winner!')
			else:
				drawText(screen, 'White is winner!')
		elif gs.staleMate:
			gameOver=True
			drawText(screen, 'Stalemate')
		clock.tick(MAX_FPS)
		p.display.flip()
  
def highLightSquare(screen, gs, validMoves, sqSelected):
	if sqSelected != ():
		r,c = sqSelected
		if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqselected is a piece than can be move
			s = p.Surface((SQ_SIZE,SQ_SIZE))
			s.set_alpha(100)
			s.fill(p.Color('aqua'))
			screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
			s.fill(p.Color('yellow'))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))
      


def drawGameState(screen, gs, validMoves, sqSelected):
	drawBoard(screen) #draw squares on the board, top left square is always light
	drawPieces(screen, gs.board)	#draw pieces on top of those squares
	highLightSquare(screen, gs, validMoves, sqSelected)

def drawBoard(screen):
    global colors 
    colors = [p.Color('light gray'), p.Color('dark green')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if piece != '--':
				screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def drawText(screen,text):
    font=p.font.SysFont("cambria",60,True,False)
    textObject=font.render(text,0,p.Color('Gray'))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject=font.render(text,0,p.Color('dark red'))
    screen.blit(textObject,textLocation.move(2,2))
    
def animateMove (move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 
    frameCount = (abs(dR)+ abs(dC))*framesPerSquare
    for frame in range (frameCount+1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)



if __name__ == '__main__':
	main()