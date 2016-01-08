import pygame, sys, os, time
from pygame.locals import *
#import serial
import threading as t
from random import randint

FLAG = True
diccBloques={'rock':[],'fire':[],'brick':[]}
cont=0

for i in xrange(1000):
	if cont%2==0:
		if randint(0,1):
			diccBloques['brick'].append([32*i,544])
		cont+=1
	else:
		diccBloques['brick'].append([32*i,544])
		cont+=1

for k in xrange(25):
	diccBloques['rock'].append([32*k*3,544-randint(1,3)*32])

# for k in xrange(25):
# 	diccBloques['fire'].append([32*k*3,544-randint(1,3)*32])

# def controlArduino(jugador):

# 	global FLAG

# 	try:
# 		AR = serial.Serial('/dev/ttyACM0',9600)
# 	except:
# 		FLAG = False

# 	while FLAG:
# 		indicador = AR.readline().strip()
# 		if '1' in indicador:
# 			jugador['salto']=1

# 		elif '2' in indicador:
# 			jugador['salto']=0

# 		if '3' in indicador:
# 			jugador['direccion'] = 'R'

# 		elif '4' in indicador:
# 			jugador['direccion'] = 'N'


def resize(image, size):

	image=(pygame.image.load(os.path.join('data', image)))
	return pygame.transform.scale(image, size)

def mover(jugador, unidad, moment, sprites):	# WIP

	# if jugador["direccion"] == 'R':
	# 	if noAvanzar!='R':
	# 		jugador["posicion"][0] += unidad

	if (moment/100)%2 == 0:
		jugador["sprite"] = 0
	else:
		jugador["sprite"] = 1

	# if jugador["direccion"] == 'L':
	# 	if noAvanzar!='L':
	# 		jugador["posicion"][0] -= unidad
	#if (moment/100)%2 == 0:
	#	jugador["sprite"] = 2
	#else:
	#	jugador["sprite"] = 3


#--------------------------------------------------
pygame.init() 								#Inicializar pygame

clock       	= pygame.time.Clock()
bAcum			= 0							# Posicion acumulada del movimiento horizontal
Juego 			= 1 						# Variable booleana que determina si el bucle sigue
unidad 			= 4 						# Velocidad de movimiento
personaje 		= [] 						# Lista de sprites del personaje
bloques 		= dict() 					# Lista de sprites de los bloques
acelHor			= 0							# Aceleracion Horizontal
velHor			= 5							# Velocidad Horizontal
jugador			= {
					"posicion":[400, 0],	# Posicion inicial del jugador
					"gravedad":0,			# Indicador de gravedad ***
					"vidas":3,				# WIP
					"direccion":'N', 		# N=neutro, L=left, R=right
					"salto":0,				# Indicador de salto
					"sprite":0 				# Indice del sprite en la lista de los sprites del personaje
					}
font 			= pygame.font.Font(None, 80)

# Inicio de identificacion del control de Arduino
#arduinoProcess	= t.Thread(target=controlArduino,args=(jugador,))
#arduinoProcess.start()

#--------------------------------------------------------------------------------------
# Carga de sprites
background = resize('bg.png', (800, 600))												# Texturas del background
personaje.append (resize('koopa1.png', (32, 64)))  										# Texturas hacia la derecha
personaje.append (resize('koopa2.png', (32, 64)))										# """"
personaje.append (pygame.transform.flip(resize('koopa1.png', (32, 64)), True, False)) 	# Texturas hacia la izquierda (derecha con flip)
personaje.append(pygame.transform.flip(resize('koopa2.png', (32, 64)), True, False))	# """"
bloques['rock']=resize('rock.png', (32, 32))											# Texturas del bloque 1 (solido, no dano)
bloques['fire']=resize('fire1.png', (16, 16))
bloques['brick']=resize('brick1.png', (32, 32))

#
#--------------------------------------------------------------------------------------

window=pygame.display.set_mode((800, 576))	#Crea ventana 800x576
pygame.mixer.music.load("data/loop.mp3")
pygame.mixer.music.set_volume(0.15)
jump=pygame.mixer.Sound("data/jump.wav")
pygame.mixer.music.play(-1)
TEST = True

while Juego:																# Mainloop




	colisiones=[]															# Lista de colisiones
	clock.tick(60) 															# Se setea el maximo fps
	pygame.display.set_caption("NN | FPS: "+str(round(clock.get_fps(), 2))) # Con esto se imprime los fps en el nombre del archivo

	window.blit(background, (0-bAcum%800, 0))
	window.blit(background, (800-bAcum%800, 0))
	# for i in xrange(10):													# Dibujo de background
	# 	window.blit(background, (800*i-bAcum, 0))							# """"

	jugRect=window.blit(personaje[jugador["sprite"]], jugador["posicion"])	# Rect del jugador, sirve para comparar colisiones

	for i in diccBloques:													# Dibujo de bloques y anadido para comprobar colisiones
		for bloque in diccBloques[i]:
			colisiones.append(window.blit(bloques[i],(bloque[0]-bAcum,bloque[1])))

	textVidas = font.render("Vidas: {0}".format(jugador["vidas"]), 1, (255, 255, 255))
	window.blit(textVidas, (0, 0))

	pygame.display.update()													# Actualizar la pantalla


	for event in pygame.event.get():										# Reconocimiento de eventos
		if event.type==pygame.QUIT:
			FLAG = False
			sys.exit()

		elif event.type==KEYDOWN:
		 	if event.key==K_SPACE:
		 		jugador['salto'] = 1

	moment = pygame.time.get_ticks()										# Variable independiente para dibujar la animacion del jugador
	listaColisiones = jugRect.collidelistall(colisiones) 					# Lista con las colisiones que tiene el personaje
	timeguide=moment/100

	if timeguide%3==0:
		bloques['fire']=resize('fire2.png', (16, 16))
	elif timeguide%3==1:
		bloques['fire']=resize('fire3.png', (16, 16))
	elif timeguide%3==2:
		bloques['fire']=resize('fire1.png', (16, 16))
	if timeguide%4==0:
		bloques['brick']=resize('brick1.png', (32, 32))
	elif timeguide%4==1:
		bloques['brick']=resize('brick2.png', (32, 32))
	elif timeguide%4==2:
		bloques['brick']=resize('brick3.png', (32, 32))
	elif timeguide%4==3:
		bloques['brick']=resize('brick4.png', (32, 32))

	for tipo in diccBloques.values():
		for k in tipo:
			x1, y1 = jugador['posicion']									# Coordenada x1, y1 del jugador
			x, y = k

			if (max(x1+bAcum+32,x+32)-min(x1+bAcum,x))<63 and (max(y1+64,y+32) - min(y1,y)) < 94:				# Comparacion de posicion por la derecha
				#if [x,y] in diccBloques['fire']:
				#	jugador['vidas']-=1
				#	jugador['posicion']=[400,0]
				#else:
				# jugador['posicion'][0] -= velHor						# Debe retroceder (<-)

				jugador['posicion'][0] = x-33-bAcum
			
			if listaColisiones != []:							# No tiene gravedad debido a que colisiona
				if y+64 > colisiones[listaColisiones[0]][1] and x+20 < colisiones[listaColisiones[0]][0]:
					jugador['posicion'][1] 	= (jugador["posicion"][1])/32*32+1 			# Se le sumo uno porque antes rebotaba infinitamente

	print listaColisiones, jugador["gravedad"]
	if listaColisiones == []:
		if jugador['salto'] == 1:											# Definicion de salto
			jugador['gravedad'] 	= -12
			jugador['posicion'][1] 	+= jugador["gravedad"]					# ***
			jugador['salto'] 		= 0
			jump.play()
		else:
			jugador["gravedad"] 	+= 1										
			jugador["posicion"][1]	+= jugador["gravedad"]

	if jugador['posicion'][0] > 800 or jugador ['posicion'][1] > 600:		# Definicion de perder (WIP)
		jugador['posicion'] = [400,0]
		jugador['gravedad'] = 0

	mover(jugador, unidad, moment, personaje)								# Animacion del jugador (WIP)

	#if moment%100 == 0:
	#	acelHor += 1

	# moverPantalla(diccBloques)												# Mover bloques
	bAcum+=velHor															# 
	#acelHor=0
	

