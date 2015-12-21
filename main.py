import pygame, sys, os
from pygame.locals import *
import serial
import threading as t

FLAG = True
dicc={'a':(0, 576-32)}

def controlArduino(jugador):
	try:
		AR = serial.Serial('/dev/ttyACM0',9600)
	except:
		FLAG = False
	while FLAG:
		indicador = AR.readline().strip()
		if '1' in indicador:
			print '!',
			jugador['salto']=1
		else:
			jugador['salto']=0

def resize(image, size):
	image=(pygame.image.load(os.path.join('data', image)))
	return pygame.transform.scale(image, size)

def mover(jugador, unidad, moment, sprites,noAvanzar):
	if jugador["direccion"] == 'R':
		if noAvanzar!='R':
			jugador["posicion"][0] += unidad
		if (moment/100)%2 == 0:
			jugador["sprite"] = 0
		else:
			jugador["sprite"] = 1
	if jugador["direccion"] == 'L':
		if noAvanzar!='L':
			jugador["posicion"][0] -= unidad
		if (moment/100)%2 == 0:
			jugador["sprite"] = 2
		else: 
			jugador["sprite"] = 3


#--------------------------------------------------

clock       	= pygame.time.Clock()
Juego 			= 1 	#Variable booleana que determina si el bucle sigue
unidad 			= 4 	# Velocidad de movimiento
personaje 		= [] 	# Lista de sprites del personaje
bloques 		= [] 	# Lista de sprites de los bloques
jugador			= {
					"posicion":[0, 0], 
					"gravedad":0, 
					"vidas":3, 
					"direccion":'N', 	#N=neutro, L=left, R=right
					"salto":0, 
					"sprite":0 			#Indice del sprite en la lista de los sprites del personaje
					}
arduinoProcess	= t.Thread(target=controlArduino,args=(jugador,))
#Carga de sprites
background=resize('bg.png', (800, 600))
personaje.append(resize('koopa1.png', (32, 64)))  # Texturas hacia la derecha
personaje.append(resize('koopa2.png', (32, 64)))
personaje.append(pygame.transform.flip(resize('koopa1.png', (32, 64)), True, False)) #Texturas hacia la izquierda (derecha con flip)
personaje.append(pygame.transform.flip(resize('koopa2.png', (32, 64)), True, False))
bloques.append(resize('fg.png', (32, 32)))

pygame.init() #Inicializar pygame
window=pygame.display.set_mode((800, 576)) #Crea ventana 800x600
arduinoProcess.start()

while Juego:		#Mainloop
	colisiones=[]
	clock.tick(30) #Se setea el maximo fps
	pygame.display.set_caption("NN | FPS: "+str(round(clock.get_fps(), 2))) # Con esto se imprime los fps en el nombre del archivo
	window.blit(background, (0, 0)) 													# Fondo del juego
	personajeRect=window.blit(personaje[jugador["sprite"]], jugador["posicion"])		# Texturas del jugador
	for i in xrange(25):		#anadir Bloques a la ventana principal
		x, y=dicc['a']
		colisiones.append(window.blit(bloques[0], (x+i*32, y)))

	colisiones.append(window.blit(bloques[0], (600, 512)))
	pygame.display.update()
	
	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			FLAG = False
			sys.exit()

		elif event.type==KEYDOWN:
			if event.key==K_RIGHT:
				jugador["direccion"] = "R"

			if event.key==K_LEFT:
				jugador["direccion"] = "L"

			if event.key==K_SPACE:
				jugador['salto'] = 1
				
		elif event.type==KEYUP:
			if event.key==K_RIGHT:
				jugador["direccion"] = "N"

			if event.key==K_LEFT:
				jugador["direccion"] = "N"

	noAvanzar=0
	moment=pygame.time.get_ticks()
	listacolisiones = personajeRect.collidelistall(colisiones) #Lista con las colisiones que tiene el personaje

	if listacolisiones==[]:
		jugador['gravedad'] 	+= 1
		jugador["posicion"][1]	+= jugador['gravedad']

	else:
		for i in colisiones:
			x1,y1=jugador['posicion']
			x,y,l,a=i
			if x1+a==x and (y<=y1<=y1+a or y<=y1+a<=y1+a):
				noAvanzar='R'
			if x1==x+a and (y<=y1<=y1+a or y<=y1+a<=y1+a):
				noAvanzar='L'

		jugador['gravedad'] 	= 0
		jugador['posicion'][1] 	= (jugador["posicion"][1])/32*32+1 #Se le sumo uno porque antes rebotaba infinitamente

		if jugador['salto']==1:
			jugador['gravedad'] 	= -12
			jugador['posicion'][1] 	+= jugador["gravedad"]
			jugador['salto'] 		= 0
	mover(jugador, unidad, moment, personaje, noAvanzar)

