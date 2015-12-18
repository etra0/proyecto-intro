import pygame,sys
from pygame.locals import *

def resize(image,size):
	image=(pygame.image.load(os.path.join('data',image)))
	return pygame.transform.scale(image,size)

sprites=[]
sprites.append(resize('koopa1.png',(32,32)))
sprites.append(resize('koopa2.png',(32,32)))
pygame.init()
window=pygame.display.set_mode((512,434))
while True:
	#pygame.display.update()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
