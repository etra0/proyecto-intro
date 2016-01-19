import pygame, sys, os, time
from pygame.locals import *
import serial
from time import sleep, time
import threading as t
from random import randint

FLAG = True

def controlArduino():

	global FLAG

	try:
		AR = serial.Serial('/dev/ttyACM0',9600)
	except:
		FLAG = False

	while FLAG:
		indicador = AR.readline().strip()
		if '1' in indicador:
			jugador['salto']=1

		elif '2' in indicador:
			jugador['salto']=0

		if '3' in indicador:
			# golpe(jugador, time())
			tiempo = time()
			jugador['arduino']=1

		elif '4' in indicador:
			jugador['arduino'] = 0
	

def golpe(jugador, tiempo):
	if jugador['golpe']:
		tiempo2 = time()
		if tiempo2-tiempo < 0.1:
			jugador['sprite'] = 6
		elif tiempo2-tiempo < 0.2:
			jugador['sprite'] = 7
		elif tiempo2-tiempo < 0.3:
			jugador['sprite'] = 8
		if jugador['sprite'] == 8:
			jugador['golpe'] = 0

def resize(image, size):

	image=(pygame.image.load(os.path.join('data', image)))
	return pygame.transform.scale(image, size)

def animacion(jugador, unidad, timeguide, sprites):
	global anim
	if timeguide%3==0:
		bloques['fire']=resize('fire2.png', (16, 16))

	elif timeguide%3==1:
		bloques['fire']=resize('fire3.png', (16, 16))

	elif timeguide%3==2:
		bloques['fire']=resize('fire1.png', (16, 16))

	if timeguide%4==0:
		bloques['brick']=resize('brick1.png', (64, 64))
		bloques['banana']=resize('banana1.png', (48, 48))
		bloques['bird']=resize('bird2.png',(63,63))
		if not jugador['golpe']:
			if anim:
				jugador["sprite"]=2
			else:
				jugador["sprite"]=5
	elif timeguide%4==1:
		bloques['brick']=resize('brick2.png', (64, 64))
		bloques['banana']=resize('banana2.png', (48, 48))
		bloques['bird']=resize('bird3.png',(63,63))
		if not jugador['golpe']:
			if anim:
				jugador["sprite"]=1
			else:
				jugador["sprite"]=5
	elif timeguide%4==2:
		bloques['brick']=resize('brick3.png', (64, 64))
		bloques['banana']=resize('banana1.png', (48, 48))
		bloques['bird']=resize('bird2.png',(63,63))
		if not jugador['golpe']:
			if anim:
				jugador["sprite"]=3
			else:
				jugador["sprite"]=5
	elif timeguide%4==3:
		bloques['brick']=resize('brick4.png', (64, 64))
		bloques['banana']=resize('banana3.png', (48, 48))
		bloques['bird']=resize('bird1.png',(63,63))
		if not jugador['golpe']:
			if anim:
				jugador["sprite"]=4
			else:
				jugador["sprite"]=5


def randblock(diccBloques, bAcum,velHor):
	if not bAcum:
		cont = 0
		for i in xrange(15):
			if randint(0,10) in range(0,6) or cont >= 2:
				diccBloques['grass'].append([64*i,544])
				cont = 0
			else:
				cont += 1
	else:
		cont = 0
		coordLastBrick = diccBloques['grass'][-1]
		if bAcum%64 in range(velHor%64):
			listaTemporal = []
			for i in xrange(4):
				listaTemporal.append(randint(0,11) in range(0,6))
			if True in listaTemporal:
				listaTemporal = listaTemporal.index(True)
			else:
				listaTemporal = 0
			listaTemporal += 1
			diccBloques['grass'].append([coordLastBrick[0]+64*listaTemporal,544])

	if bAcum%800 in range(velHor%64):
		for i in xrange(15):
			diccBloques['rock'].append([bAcum/64*64+832+64*i*3,544-randint(1,5)*64])
		for i in xrange(5):
			diccBloques['banana'].append([bAcum/64*64+832+64*i*3,544-randint(1,5)*64])
		for i in xrange(2):
			coords = [bAcum/64*64+832+64*i*3,544-randint(1,5)*64]
			if coords not in diccBloques['banana']:
				diccBloques['bird'].append(coords)

	

		# Esto se utiliza para limpiar las banans superpuestas

		
	diccBloques['grass'] = diccBloques['grass'][:20]
	diccBloques['rock'] = diccBloques['rock'][:20]
	diccBloques['banana'] = diccBloques['banana'][:5]

	for i in xrange(len(diccBloques['rock'])):
		indiceAcumulado = 0
		for j in xrange(len(diccBloques['banana'])):
			j -= indiceAcumulado
			if diccBloques['rock'][i] == diccBloques['banana'][j]:
				del diccBloques['banana'][j]
				indiceAcumulado += 1

		indiceAcumulado = 0
		for j in xrange(len(diccBloques['bird'])):
			j -= indiceAcumulado
			if diccBloques['rock'][i] == diccBloques['bird'][j]:
				del diccBloques['bird'][j]
				indiceAcumulado += 1

	# Eliminar bloques fuera de pantalla
	for tipo in diccBloques:
		indiceAcumulado = 0
		for i in range(len(diccBloques[tipo])):
			i = i-indiceAcumulado
			if diccBloques[tipo][i][0] < bAcum-64:
				del diccBloques[tipo][i]
				indiceAcumulado += 1




#--------------------------------------------------
pygame.init() 								#Inicializar pygame
personaje 		= [] 						# Lista de sprites del personaje
bloques 		= dict() 					# Lista de sprites de los bloques
os.environ["SDL_VIDEO_CENTERED"] = "1"		# Se centra la pantalla.
momentAcum=0
def iniciar():
	global diccBloques, anim, clock, bAcum, Partida, unidad, acelHor, velHor, Juego, jugador, font
	diccBloques		= {'rock':[],'fire':[],'grass':[],'banana':[],'bird':[]}
	anim 			= True
	clock       	= pygame.time.Clock()
	bAcum			= 0							# Posicion acumulada del movimiento horizontal
	Partida			= 1 						# Variable booleana que determina si el bucle sigue
	unidad 			= 4 						# Velocidad de movimiento
	acelHor			= 0							# Aceleracion Horizontal
	velHor			= 3							# Velocidad Horizontal
	Juego			= True
	jugador			= {
						"posicion":[400, 0],	# Posicion inicial del jugador
						"gravedad":0,			# Indicador de rgravedad ***
						"vidas":3,				# WIP
						"direccion":'N', 		# N=neutro, L=left, R=right
						"salto":0,				# Indicador de salto
						"golpe":0,
						"sprite":0, 				# Indice del sprite en la lista de los sprites del personaje
						"cayendo":False,
						"bananas":0,
						"score":0,
						"arduino":0
						}
	global tiempo
	tiempo = 0
	font 			= pygame.font.Font(None, 60)


# Inicio de identificacion del control de Arduino
iniciar()

try:
	arch = open("score","r")
	for linea in arch:
		linea = linea.strip()
	record = int(linea)
	arch.close()
except:
	record = 0
#--------------------------------------------------------------------------------------
# Carga de sprites
startingbackground = resize("sbg.png", (800,600))
background = resize('bg.jpg', (800, 600))
												# Texturas del background
personaje.append (resize('monkey1.png', (64, 64)))  										# Texturas hacia la derecha
personaje.append (resize('monkey2.png', (64, 64)))										# """"
personaje.append (resize('monkey3.png', (64, 64)))
personaje.append (resize('monkey4.png', (64, 64)))
personaje.append (resize('monkey5.png', (64, 64)))
personaje.append (resize('monkey6.png', (64, 64)))
personaje.append(resize('hit1.png', (64, 64)))
personaje.append(resize('hit2.png', (84, 82)))
personaje.append(resize('hit3.png', (88,64)))

bloques['rock']=resize('rock.png', (64, 64))											# Texturas del bloque 1 (solido, no dano)
bloques['fire']=resize('fire1.png', (16, 16))
bloques['brick']=resize('brick1.png', (64, 64))
bloques['grass']=resize('grass.png',(64,64))
bloques['banana']=resize('banana3.png',(48,48))
bloques['bird']=resize('bird2.png',(63,63))
#
#--------------------------------------------------------------------------------------

window=pygame.display.set_mode((800, 600))	#Crea ventana 800x576
pygame.mixer.music.load("data/mainloop.mp3")
pygame.mixer.music.set_volume(0.50)
jump=pygame.mixer.Sound("data/jump.ogg")
bite=pygame.mixer.Sound("data/bite.ogg")
bite.set_volume(0.2)
death=pygame.mixer.Sound("data/death.ogg")
hit=pygame.mixer.Sound("data/hit.ogg")
pygame.mixer.music.play(-1)


arduinoProcess	= t.Thread(target=controlArduino)
arduinoProcess.start()
while Juego:
	window.blit(background, (0-bAcum%800, 0))
	window.blit(background, (800-bAcum%800, 0))
	window.blit(startingbackground, (0,0))
	textRecord = font.render("Record: {0}".format(record), 1, (255, 255, 255))
	#window.blit(textRecord, (400, 400))
	bAcum += 1
	Partida = False
	pygame.display.set_caption("SMASH YOUR BRO")
	pygame.display.update()

	for event in pygame.event.get():										# Reconocimiento de eventos
		if event.type==pygame.QUIT:
			FLAG = False
			sys.exit()
		if event.type==KEYDOWN:
			if event.key== K_RETURN:
				iniciar()

		 		Partida = True
		 		bAcum = 0

	
	while Partida:																# Mainloop

		if jugador['bananas'] >= 20:
			jugador['vidas'] += 1
			jugador['bananas'] = 0
			jugador['score'] += 100

		if jugador['vidas'] <= 0:
			break

		randblock(diccBloques, bAcum, velHor)
		colisiones=[]															# Lista de colisiones
		clock.tick(60) 															# Se setea el maximo fps
		pygame.display.set_caption("SMASH YOUR BRO | FPS: "+str(round(clock.get_fps(), 2))) # Con esto se imprime los fps en el nombre del archivo

		window.blit(background, (0-bAcum%800, 0))
		window.blit(background, (800-bAcum%800, 0))

		for i in diccBloques:													# Dibujo de bloques y anadido para comprobar colisiones
			for bloque in diccBloques[i]:
				colisiones.append(window.blit(bloques[i],(bloque[0]-bAcum,bloque[1])))

		textVidas = font.render("Vidas: {0}".format(jugador["vidas"]), 1, (255, 255, 255))
		window.blit(textVidas, (0, 0))
		textBananas = font.render("Bananas: {0}".format(jugador["bananas"]), 1, (255, 255, 255))
		window.blit(textBananas, (0, 40))
		textScore = font.render("Score: {0}".format(jugador["score"]), 1, (255, 255, 255))
		window.blit(textScore, (0, 80))

		jugRect=window.blit(personaje[jugador["sprite"]], jugador["posicion"])	# Rect del jugador, sirve para comparar colisiones
		pygame.display.update()													# Actualizar la pantalla


		for event in pygame.event.get():										# Reconocimiento de eventos
			if event.type==pygame.QUIT:
				FLAG = False
				sys.exit()

			elif event.type==KEYDOWN:
			 	if event.key==K_SPACE:
			 		jugador['salto'] = 1
			 	if event.key== K_w:
			 		tiempo = time()
			 		jugador['golpe'] = 1
			 	if event.key== K_RETURN:
			 		pausa = True
			 		pygame.mixer.music.pause()
			 		while pausa:
			 			for event in pygame.event.get():
			 				if event.type==KEYDOWN:
			 					pausa = False
			 					pygame.mixer.music.unpause()

			 		
		if jugador['arduino']:
			tiempo = time()
	 		jugador['golpe'] = 1
		moment = pygame.time.get_ticks() - momentAcum									# Variable independiente para dibujar la animacion del jugador
		listaColisiones = jugRect.collidelistall(colisiones) 					# Lista con las colisiones que tiene el personaje
		timeguide=moment/100

		if listaColisiones != []:
			for i in listaColisiones:
				if colisiones[i][2:]==[48,48]:
					jugador['bananas']+=1
					del diccBloques['banana'][diccBloques['banana'].index([colisiones[i][0]+bAcum,colisiones[i][1]])]
					jugador['score'] += 20
					bite.play()
				elif colisiones[i][2:]==[63,63]:
					if not jugador["golpe"]:
						jugador['posicion']=[400,0]
						jugador['vidas']-= 1
						jugador['cayendo'] = True
						death.play()
					else:
						jugador['score'] += 50
						del diccBloques['bird'][diccBloques['bird'].index([colisiones[i][0]+bAcum,colisiones[i][1]])]
						hit.play()
					break
					
				else:
					x, y = colisiones[i][:2]
					x1, y1 = jugador['posicion']

					if max(y1+64,y+64) - min(y1,y) < 126 and x < x1+64 < x+64:				# Comparacion de posicion por la derecha
						jugador['posicion'][0] -=velHor

					if max(x1+64,x+64) - min(x1,x) < 120 and y < y1+64 < y+64:
						jugador['posicion'][1] 	= (jugador["posicion"][1])/64*64+33 			# Se le sumo uno porque antes rebotaba infinitamente
						jugador['gravedad'] 	= 0
						jugador["cayendo"] 		= False

					if max(x1+64,x+64) - min(x1,x) < 120 and y < y1 < y+64:
						jugador['gravedad']=0
						jugador['posicion'][1] = (jugador["posicion"][1])/64*64+33
						pass
					if jugador['salto'] == 1:											# Definicion de salto
						jugador['gravedad'] 	= -24
						jugador['posicion'][1] 	+= jugador["gravedad"]					# ***
						jugador['salto'] 		= 0
						jump.play()

					else: 
						jugador["cayendo"] 	= True
						jugador['sprite']	= 5

			anim=True

		if listaColisiones == [] or jugador["cayendo"]:
			jugador["gravedad"] += 1
			jugador["posicion"][1]	+= jugador["gravedad"]/2

			if listaColisiones==[]:
				anim=False

		if jugador['posicion'][0] < -64 or jugador ['posicion'][1] > 600:		# Definicion de perder
			jugador['posicion'] = [400,0]
			jugador['gravedad'] =0
			jugador['vidas']-=1
			death.play()

		animacion(jugador, unidad, timeguide, personaje)								# Animacion general
		try:
			golpe(jugador, tiempo)
		except:
			pass

		print jugador['golpe']
		if jugador['golpe']:
			if time() - tiempo > 0.3:
				jugador['golpe'] = 0

		if moment%500 == 0:
			acelHor += 1
			velHor+=1

		if moment%100 == 0:
			jugador['score'] +=1
		bAcum+=velHor
		acelHor=0
	if jugador['score'] > record:
		record = jugador['score']
		arch = open("score","w")
		arch.write(str(jugador['score'])+"\n")
		arch.close()
	momentAcum = pygame.time.get_ticks()
	
		

