import pygame,sys,os
from pygame.locals import *

dicc={'a':(0,576-32)}

def resize(image,size):
	image=(pygame.image.load(os.path.join('data',image)))
	return pygame.transform.scale(image,size)

def mover(jugador,unidad,moment,sprites):
	if jugador["direccion"] == 'R':
		jugador["posicion"][0]+=unidad
		if (moment/100)%2==0:
			jugador["sprite"] = 0
		else:
			jugador["sprite"] = 1
	if jugador["direccion"] == 'L':
		jugador["posicion"][0]-=unidad
		if (moment/100)%2==0:
			jugador["sprite"] = 2
		else:
			jugador["sprite"] = 3


#--------------------------------------------------
clock       =  						pygame.time.Clock()
Juego 		=						1 #Variable booleana que determina si el bucle sigue
unidad 		=						4 # Velocidad de movimiento
personaje 	=						[] # Lista de sprites del personaje
bloques 	= 						[] # Lista de sprites de los bloques
jugador		=						{
										"posicion":[0,0],
										"gravedad":0,
										"vidas":3,
										"direccion":'N',	#N=neutro, L=left, R=right
										"salto":0,
										"sprite":0
									}

#Carga de sprites
background=resize('bg.png',(800,600))
personaje.append(resize('koopa1.png',(32,64)))
personaje.append(resize('koopa2.png',(32,64)))
personaje.append(pygame.transform.flip(resize('koopa1.png',(32,64)),True,False))
personaje.append(pygame.transform.flip(resize('koopa2.png',(32,64)),True,False))
bloques.append(resize('fg.png',(32,32)))

pygame.init() #Inicializar pygame
window=pygame.display.set_mode((800,576)) #Crea ventana 800x600
collisiones=[]	#Rects de los bloques


while Juego:		#Mainloop
	clock.tick(60)
	pygame.display.set_caption("NN | FPS: "+str(round(clock.get_fps(),2)))
	window.blit(background,(0,0))
	personajeRect=window.blit(personaje[jugador["sprite"]],jugador["posicion"])
	for i in xrange(25):		#anadir Bloques a la ventana principal
		x,y=dicc['a']
		collisiones.append(window.blit(bloques[0],(x+i*32,y)))
	collisiones.append(window.blit(bloques[0],(600,512)))
	#print collisiones
	pygame.display.update()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
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
	moment=pygame.time.get_ticks()
	mover(jugador,unidad,moment,personaje)

	listacollisiones=personajeRect.collidelistall(collisiones)
	if listacollisiones==[]:
		jugador['gravedad'] += 1
		jugador["posicion"][1]+= jugador['gravedad']
	else:
		jugador['gravedad'] = 0
		jugador['posicion'][1] = (jugador["posicion"][1])/32*32+1
		if jugador['salto']==1:
			jugador['gravedad'] = -12
			jugador['posicion'][1] += jugador["gravedad"]
			jugador['salto'] = 0


