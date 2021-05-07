#!/usr/bin/env python3

#
# @Programmer Dominik Sysojew - Osinski
# @Graphics Joseph Illingworth
# Space Invaders
# V 1.2.1
#
# See changelog.txt for list of changes made in this version
#

import tkinter
import random
import math

#
# Try to import windows sounds, and define functions for music playback
#
try:

	import winsound
	
	def AudioPlay(path):
		winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
		
	def AudioStop():
		winsound.PlaySound(None, winsound.SND_PURGE)
	
except:
	
	def AudioPlay(path):
		pass
		
	def AudioStop():
		pass
	
lastx = 0
lasty = 0

window = tkinter.Tk()
window.title("Space Invaders")
window.overrideredirect(True)
window.geometry(str(window.winfo_screenwidth())+"x"+str(window.winfo_screenheight()))
window.config(bg="black")
window.config(cursor="none")

#
# This class defines 'static' weapon presets, they should not be changed during runtime
# Additional weapons may be added.
# Structure for the weapons
#
#	'image' : tkinter.PhotoImage - This stores the image which is drawn on screen if the game is used. This field is required, even if no missiles would be fired
#	'level' : list [] - This list contains lists which define how the bullets should be shot, example
#		[[(10, 0, -10, 0, 10, 1)]] - this would shoot one bullet at level 1.
#						Each tuple () defines a singular bullet. List containing tuples is defining set of bullets at specific level (identified by index).
#						The weapon level is counted from 0, therefore weapon at "level 1" as shown in GUI, will be accessed as index 0.
#						The values are storred as following:
#		(Offset_y, Offset_x, velocity_y, velocity_x, damage, piercing)
#			Offset_y - defines what is the Y offset on the screen from the player
#			Offset_x - defines what is the X offset on the screen from the player
#			velocity_y - defines what is the velocity of the missile in Y direction
#			velocity_x - defines what is the velocity of the missile in X direction
#			damage - defines how much damage the weapon deals at hit
#			piercing - defines how much times the missile can hit a obsticle before discarding
#	'bpl' : list of integers [] - This list defines how many missiles may be there on screen at a given time.
#	'cooldown' : list of integers [] - This defines how many frames the player must wait before next missile can be shot, this can be changed at different levels
#	'soundfile' : string - This defines which sound file should be played once weapon is fired
#

class weapon:
	NONE = {
				"image":tkinter.PhotoImage(file="data/images/upgrades/laser.gif"),
				"level":[[]],
				"bpl":[0],
				"cooldown":[0],
				'soundfile':''
			}
	LASER = {
				"image":tkinter.PhotoImage(file="data/images/weapons/laser.gif"),
				"level":[
							[
								(10, 0, -10, 0, 10, 1)
							],
							[
								(10, 0, -15, 0, 10, 1)
							],
							[
								(10, 0, -10, 0, 10, 1),
								(10, 0, -9, 1, 10, 1),
								(10, 0, -9, -1, 10, 1)
							],
							[
								(10, 0, -15, 0, 10, 1),
								(10, 0, -14, 1, 10, 1),
								(10, 0, -14, -1, 10, 1)
							],
							[
								(10, 0, -10, 0, 10, 1),
								(10, 0, -9, 1, 10, 1),
								(10, 0, -9, -1, 10, 1),
								(10, 0, -8, 2, 10, 1),
								(10, 0, -8, -2, 10, 1)
							],
							[
								(10, 0, -15, 0, 10, 1),
								(10, 0, -14, 1, 10, 1),
								(10, 0, -14, -1, 10, 1),
								(10, 0, -13, 2, 10, 1),
								(10, 0, -13, -2, 10, 1)
							]
						],
				"bpl":[5, 7, 15, 21, 25, 35],
				"cooldown":[5, 5, 5, 5, 5, 5],
				'soundfile':'data/sounds/laser.wav'
			}
	PLAZMA = {
				"image":tkinter.PhotoImage(file="data/images/weapons/plazma.gif"),
				"level":[
							[
								(10, 0, -10, 0, 50, 1)
							],
							[
								(10, 0, -15, 0, 50, 1)
							],
							[
								(10, 0, -10, 0, 50, 1),
								(15, 15, -10, 0, 50, 1),
								(15, -15, -10, 0, 50, 1)
							],
							[
								(10, 0, -15, 0, 50, 1),
								(15, 15, -15, 0, 50, 1),
								(15, -15, -15, 0, 50, 1)
							]
						],
				"bpl":[3, 5, 15, 25],
				"cooldown":[5, 5, 5, 5],
				'soundfile':'data/sounds/plazma_v3.wav'
			}
	HULLBREAKER = {
				"image":tkinter.PhotoImage(file="data/images/weapons/hullbreaker.gif"),
				"level":[
							[
								(10, 0, -10, 0, 10, 2)
							],
							[
								(10, 0, -10, 0, 20, 3)
							],
							[
								(10, 0, -13, 0, 20, 3)
							],
							[
								(10, 0, -13, 0, 30, 4)
							]
						],
				"bpl":[5, 5, 5, 5],
				"cooldown":[3, 3, 3, 3],
				'soundfile':'data/sounds/hullbreaker.wav'
			}
	DEVASTATOR = {
				"image":tkinter.PhotoImage(file="data/images/weapons/devastator.gif"),
				"level":[
							[
								(-0,0,-2000,0,10,1),
								(-25,0,-2000,0,10,1),
								(-50,0,-2000,0,10,1),
								(-75,0,-2000,0,10,1),
								(-100,0,-2000,0,10,1),
								(-125,0,-2000,0,10,1),
								(-150,0,-2000,0,10,1),
								(-175,0,-2000,0,10,1),
								(-200,0,-2000,0,10,1),
								(-225,0,-2000,0,10,1),
								(-250,0,-2000,0,10,1),
								(-275,0,-2000,0,10,1),
								(-300,0,-2000,0,10,1),
								(-325,0,-2000,0,10,1),
								(-350,0,-2000,0,10,1),
								(-375,0,-2000,0,10,1),
								(-400,0,-2000,0,10,1),
								(-425,0,-2000,0,10,1),
								(-450,0,-2000,0,10,1),
								(-475,0,-2000,0,10,1),
								(-500,0,-2000,0,10,1),
								(-525,0,-2000,0,10,1),
								(-550,0,-2000,0,10,1),
								(-575,0,-2000,0,10,1),
								(-600,0,-2000,0,10,1),
								(-625,0,-2000,0,10,1),
								(-650,0,-2000,0,10,1),
								(-675,0,-2000,0,10,1),
								(-700,0,-2000,0,10,1),
								(-725,0,-2000,0,10,1),
								(-750,0,-2000,0,10,1),
								(-775,0,-2000,0,10,1),
								(-800,0,-2000,0,10,1),
								(-825,0,-2000,0,10,1),
								(-850,0,-2000,0,10,1),
								(-875,0,-2000,0,10,1),
								(-900,0,-2000,0,10,1),
								(-925,0,-2000,0,10,1),
								(-950,0,-2000,0,10,1),
								(-975,0,-2000,0,10,1),
								(-1000,0,-2000,0,10,1),
								(-1025,0,-2000,0,10,1),
								(-1050,0,-2000,0,10,1),
								(-1075,0,-2000,0,10,1)
							],
							[
								(-0,0,-2000,0,10,1),
								(-25,0,-2000,0,10,1),
								(-50,0,-2000,0,10,1),
								(-75,0,-2000,0,10,1),
								(-100,0,-2000,0,10,1),
								(-125,0,-2000,0,10,1),
								(-150,0,-2000,0,10,1),
								(-175,0,-2000,0,10,1),
								(-200,0,-2000,0,10,1),
								(-225,0,-2000,0,10,1),
								(-250,0,-2000,0,10,1),
								(-275,0,-2000,0,10,1),
								(-300,0,-2000,0,10,1),
								(-325,0,-2000,0,10,1),
								(-350,0,-2000,0,10,1),
								(-375,0,-2000,0,10,1),
								(-400,0,-2000,0,10,1),
								(-425,0,-2000,0,10,1),
								(-450,0,-2000,0,10,1),
								(-475,0,-2000,0,10,1),
								(-500,0,-2000,0,10,1),
								(-525,0,-2000,0,10,1),
								(-550,0,-2000,0,10,1),
								(-575,0,-2000,0,10,1),
								(-600,0,-2000,0,10,1),
								(-625,0,-2000,0,10,1),
								(-650,0,-2000,0,10,1),
								(-675,0,-2000,0,10,1),
								(-700,0,-2000,0,10,1),
								(-725,0,-2000,0,10,1),
								(-750,0,-2000,0,10,1),
								(-775,0,-2000,0,10,1),
								(-800,0,-2000,0,10,1),
								(-825,0,-2000,0,10,1),
								(-850,0,-2000,0,10,1),
								(-875,0,-2000,0,10,1),
								(-900,0,-2000,0,10,1),
								(-925,0,-2000,0,10,1),
								(-950,0,-2000,0,10,1),
								(-975,0,-2000,0,10,1),
								(-1000,0,-2000,0,10,1),
								(-1025,0,-2000,0,10,1),
								(-1050,0,-2000,0,10,1),
								(-1075,0,-2000,0,10,1)
							],
							[
								(-0,0,-2000,0,10,1),
								(-25,0,-2000,0,10,1),
								(-50,0,-2000,0,10,1),
								(-75,0,-2000,0,10,1),
								(-100,0,-2000,0,10,1),
								(-125,0,-2000,0,10,1),
								(-150,0,-2000,0,10,1),
								(-175,0,-2000,0,10,1),
								(-200,0,-2000,0,10,1),
								(-225,0,-2000,0,10,1),
								(-250,0,-2000,0,10,1),
								(-275,0,-2000,0,10,1),
								(-300,0,-2000,0,10,1),
								(-325,0,-2000,0,10,1),
								(-350,0,-2000,0,10,1),
								(-375,0,-2000,0,10,1),
								(-400,0,-2000,0,10,1),
								(-425,0,-2000,0,10,1),
								(-450,0,-2000,0,10,1),
								(-475,0,-2000,0,10,1),
								(-500,0,-2000,0,10,1),
								(-525,0,-2000,0,10,1),
								(-550,0,-2000,0,10,1),
								(-575,0,-2000,0,10,1),
								(-600,0,-2000,0,10,1),
								(-625,0,-2000,0,10,1),
								(-650,0,-2000,0,10,1),
								(-675,0,-2000,0,10,1),
								(-700,0,-2000,0,10,1),
								(-725,0,-2000,0,10,1),
								(-750,0,-2000,0,10,1),
								(-775,0,-2000,0,10,1),
								(-800,0,-2000,0,10,1),
								(-825,0,-2000,0,10,1),
								(-850,0,-2000,0,10,1),
								(-875,0,-2000,0,10,1),
								(-900,0,-2000,0,10,1),
								(-925,0,-2000,0,10,1),
								(-950,0,-2000,0,10,1),
								(-975,0,-2000,0,10,1),
								(-1000,0,-2000,0,10,1),
								(-1025,0,-2000,0,10,1),
								(-1050,0,-2000,0,10,1),
								(-1075,0,-2000,0,10,1)
							]
						],
				"bpl":[44, 44, 44],
				"cooldown":[20, 15, 10],
				'soundfile':'data/sounds/fire.wav'
			}
	
class entity():


	def __init__(self, loc_x, loc_y, imagefile=None, image=None, vel_x=2, vel_y=0, health=10):
	
		if imagefile == None and image == None:
			return
			
		if imagefile == None:
			self.image = image
			
		if image == None:
			self.image = tkinter.PhotoImage(file=imagefile)
			
		self.loc_x = loc_x
		self.loc_y = loc_y
		self.imgID = canvas.create_image((self.loc_x, self.loc_y), image=self.image)
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.health = health
		
	def changeImage(self, imagefile=None, image=None):
		
		if imagefile == None and image == None:
			return False
			
		if imagefile == None:
			self.image = image
			
		if image == None:
			self.image = tkinter.PhotoImage(file=imagefile)
			
		canvas.delete(self.imgID)
		self.imgID = canvas.create_image((self.loc_x, self.loc_y), image=self.image)
		return True
		
	def addLocation(self, x, y):
	
		if self.loc_x + x <= 25 and x < 0:
			return False
			
		if self.loc_x + x >= window.winfo_screenwidth()-25 and x > 0:
			return False
			
		if self.loc_y + y <= 25 and y < 0:
			return False
			
		if self.loc_y + y >= window.winfo_screenheight()-25 and y > 0:
			return False
			
		self.loc_x += x
		self.loc_y += y
		canvas.move(self.imgID, x, y)
		return True
		
		
	def autoLocate(self):
	
		if not self.addLocation(self.vel_x, 0):
			self.vel_x = -self.vel_x
			self.addLocation(self.vel_x, 0)
			
		if not self.addLocation(0, self.vel_y):
			self.vel_y = -self.vel_y
			self.addLocation(0, self.vel_y)
			
			
	def preremove(self):
	
		canvas.delete(self.imgID)

class MenuEntity(entity):
	
	def __init__(self, loc_x, loc_y, action, imagefile=None, image=None, vel_x=0, vel_y=0, health=1):
		super().__init__(loc_x, loc_y, imagefile, image, vel_x, vel_y, health)
		self.action = action
		
		
	def preremove(self):
		canvas.delete(self.imgID)
		self.action()
		
		
	def justRemove(self):
		canvas.delete(self.imgID)
		
class Player:
	
	def __init__(self, loc_x, loc_y, imagefile=None, image:tkinter.PhotoImage=None, health=3, invincible=False, weaponType=weapon.LASER, weaponLevel = 0):
	
		if imagefile == None and image == None:
			print("WARNING: trying to create player object without any image or imagefile")
			return
			
		if imagefile == None:
			self.image = image
			
		if image == None:
			self.image = tkinter.PhotoImage(file=imagefile)
			
		self.loc_x = loc_x
		self.loc_y = loc_y
		self.health = health
		self.invincible = invincible
		self.weaponType = weaponType
		self.weaponLevel = weaponLevel
		self.weaponCooldown = 0
		self.imgID = canvas.create_image((self.loc_x, self.loc_y), image=self.image)
		self.updateMoveLeft = False
		self.updateMoveUp = False
		self.updateMoveDown = False
		self.updateMoveRight = False
		self.updateShoot = False
		self.speedLeft = 0
		self.speedUp = 0
		self.speedDown = 0
		self.speedRight = 0
		self.score = 0
		self.playerShots = []
		
	def changeImage(self, imagefile=None, image:tkinter.PhotoImage=None):
		
		if imagefile == None and image == None:
			return False
			
		if imagefile == None:
			self.image = image
			
		if image == None:
			self.image = tkinter.PhotoImage(file=imagefile)
			
		canvas.delete(self.imgID)
		self.imgID = canvas.create_image((self.loc_x, self.loc_y), image=self.image)
		return True
		
	def addLocation(self, x, y):
	
		if self.loc_x + x <= 25 and x < 0:
			return False
			
		if self.loc_x + x >= window.winfo_screenwidth()-25 and x > 0:
			return False
			
		if self.loc_y + y <= 25 and y < 0:
			return False
			
		if self.loc_y + y >= window.winfo_screenheight()-25 and y > 0:
			return False
			
		self.loc_x += x
		self.loc_y += y
		canvas.move(self.imgID, x, y)
		return True
		
	def update(self):
		
		x = 0
		y = 0
		
		if self.updateMoveLeft:
			if self.speedLeft < 15:
				self.speedLeft += 1
			
			if self.loc_x - self.speedLeft > 25:
				self.loc_x -= self.speedLeft
				x -= self.speedLeft
			
		if self.updateMoveUp:
			if self.speedUp < 15:
				self.speedUp += 1
				
			if self.loc_y - self.speedUp > 25:
				self.loc_y -= self.speedUp
				y -= self.speedUp
			
		if self.updateMoveDown:
			if self.speedDown < 15:
				self.speedDown += 1
				
			if self.loc_y + self.speedDown < window.winfo_screenheight()-25:
				self.loc_y += self.speedDown
				y += self.speedDown
			
		if self.updateMoveRight:
			if self.speedRight < 15:
				self.speedRight += 1
			
			if self.loc_x + self.speedRight < window.winfo_screenwidth()-25:
				self.loc_x += self.speedRight
				x += self.speedRight
			
		if self.updateShoot:
			if len(self.playerShots) < self.weaponType["bpl"][self.weaponLevel]:
				if self.weaponCooldown == 0:
					self.weaponCooldown = self.weaponType["cooldown"][self.weaponLevel]
					AudioPlay(self.weaponType['soundfile'])
					for z in self.weaponType["level"][self.weaponLevel]:
						self.playerShots.append(shot(self.loc_x + z[1], self.loc_y + z[0], image=self.weaponType["image"], vel_y=z[2], vel_x=z[3], damage=z[4], piercing=z[5]))
		
	
		if self.weaponCooldown != 0:
			self.weaponCooldown -= 1
		
		canvas.move(self.imgID, x, y)

	def preremove(self):
		canvas.delete(self.imgID)
		

class shot(entity):


	def __init__(self, loc_x, loc_y, imagefile=None, image=None, vel_x=0, vel_y=-10, damage=10, piercing=1):
	
		super(shot, self).__init__(loc_x, loc_y, imagefile, image, vel_x, vel_y)
		self.piercing = piercing
		self.damage = damage
		
		
	def update(self):
	
		self.loc_x += self.vel_x
		self.loc_y += self.vel_y
		canvas.move(self.imgID, self.vel_x, self.vel_y)
		
class upgrade(entity):


	def __init__(self, loc_x, loc_y, type, imagefile=None, image=None, vel_x=0, vel_y=5):
	
		super(upgrade, self).__init__(loc_x, loc_y, imagefile, image, vel_x, vel_y)
		self.type = type
		
		
	def update(self):
	
		self.loc_x += self.vel_x
		self.loc_y += self.vel_y
		canvas.move(self.imgID, self.vel_x, self.vel_y)

def controllerDown(event):
	if event.char == event.keysym:
		if event.char.lower() == "w":
			playerOne.updateMoveUp = True
			
		if event.char.lower() == "a":
			playerOne.updateMoveLeft = True
			
		if event.char.lower() == "s":
			playerOne.updateMoveDown = True
			
		if event.char.lower() == "d":
		 	playerOne.updateMoveRight = True
			
		if event.char.lower() == "i" and playerTwo != None:
			playerTwo.updateMoveUp = True
			
		if event.char.lower() == "j" and playerTwo != None:
			playerTwo.updateMoveLeft = True
			
		if event.char.lower() == "k" and playerTwo != None:
			playerTwo.updateMoveDown = True
			
		if event.char.lower() == "l" and playerTwo != None:
		 	playerTwo.updateMoveRight = True
			
def controllerUp(event):
	if event.char == event.keysym:
		if event.char.lower() == "w":
			playerOne.updateMoveUp = False
			playerOne.speedUp = 0
			
		if event.char.lower() == "a":
			playerOne.updateMoveLeft = False
			playerOne.speedLeft = 0
			
		if event.char.lower() == "s":
			playerOne.updateMoveDown = False
			playerOne.speedDown = 0
			
		if event.char.lower() == "d":
			playerOne.updateMoveRight = False
			playerOne.speedRight = 0
		
		if event.char.lower() == "i" and playerTwo != None:
			playerTwo.updateMoveUp = False
			playerTwo.speedUp = 0
			
		if event.char.lower() == "j" and playerTwo != None:
			playerTwo.updateMoveLeft = False
			playerTwo.speedLeft = 0
			
		if event.char.lower() == "k" and playerTwo != None:
			playerTwo.updateMoveDown = False
			playerTwo.speedDown = 0
			
		if event.char.lower() == "l" and playerTwo != None:
			playerTwo.updateMoveRight = False
			playerTwo.speedRight = 0
			



def controllerMouse(event):

	global playerOne, lastx, lasty
	
	if(event.x == playerOne.loc_x and event.y == playerOne.loc_y):
		lastx = event.x
		lasty = event.y
		return
		
	#move player	
	playerOne.addLocation(event.x-lastx, 0)
	playerOne.addLocation(0, event.y-lasty)
	lastx = event.x
	lasty = event.y
	
			
def update():

	global bg1pos, bg2pos, score, scoreID1, scoreID2, wave, waveID, healthID1, healthID2, playerOne, playerTwo
	
	scbu1 = int(playerOne.score/10000)
	scbu2 = 0
	if playerTwo != None:
		scbu2 = int(playerTwo.score/10000)
	
	# This line works outside virtualbox, but doesn't work inside
	# This line should be commented out for running inside virtualbox
	window.event_generate("<Motion>", warp=True, x=playerOne.loc_x, y=playerOne.loc_y)				#<==========================================================================================================
	
	
	#Check whatever the background is still on the screen
	#If the background is below the screen teleport it above the screen
	if bg1pos >= backgroundImage.height():
		bg1pos = -backgroundImage.height()
		canvas.move(bg1, 0, -backgroundImage.height()*2)
		
	if bg2pos >= backgroundImage1.height():
		bg2pos = -backgroundImage1.height()
		canvas.move(bg2, 0, -backgroundImage1.height()*2)
		
	#move the background down by 1 pixel to give the feeling of movement
	canvas.move(bg1, 0, 1)
	canvas.move(bg2, 0, 1)
	bg1pos += 1
	bg2pos += 1
	
	#Update the scoring on the bottom left side of screen
	canvas.delete(scoreID1)
	if playerOne.health > 0:
		scoreID1 = canvas.create_text((10, 50), text="Weapon level: " + str(playerOne.weaponLevel + 1) + "\nScore: "+str(playerOne.score), fill="white", anchor=tkinter.NW, font=("System 20 bold"))
	else:
		scoreID1 = canvas.create_text((10, 50), text="GAME OVER\nScore: " + str(playerOne.score), fill="white", anchor=tkinter.NW, font=("System 20 bold"))
	
	
	if playerTwo != None:
		canvas.delete(scoreID2)
		if playerTwo.health > 0:
			scoreID2 = canvas.create_text((window.winfo_screenwidth()-10, 50), text="Weapon level: " + str(playerTwo.weaponLevel + 1) + "\nScore: "+str(playerTwo.score), fill="white", anchor=tkinter.NE, font=("System 20 bold"), justify=tkinter.RIGHT)
		else:
			scoreID2 = canvas.create_text((window.winfo_screenwidth()-10, 50), text="GAME OVER\nScore: " + str(playerTwo.score), fill="white", anchor=tkinter.NE, font=("System 20 bold"), justify=tkinter.RIGHT)

	canvas.delete(waveID)
	waveID = canvas.create_text((10, window.winfo_screenheight()-40), text="Wave: " + str(wave), fill="white", anchor=tkinter.NW, font=("System 20 bold"))
	
	canvas.delete(healthID1)
	if playerOne.health == 1:
		healthID1 = canvas.create_image((10, 10), image=life1, anchor=tkinter.NW)
	elif playerOne.health == 2:
		healthID1 = canvas.create_image((10, 10), image=life2, anchor=tkinter.NW)
	elif playerOne.health == 3:
		healthID1 = canvas.create_image((10, 10), image=life3, anchor=tkinter.NW)
	elif playerOne.health == 4:
		healthID1 = canvas.create_image((10, 10), image=life4, anchor=tkinter.NW)
	elif playerOne.health == 5:
		healthID1 = canvas.create_image((10, 10), image=life5, anchor=tkinter.NW)
	elif playerOne.health == 6:
		healthID1 = canvas.create_image((10, 10), image=life6, anchor=tkinter.NW)
	
	
	if playerTwo != None:
		canvas.delete(healthID2)
		if playerTwo.health == 1:
			healthID2 = canvas.create_image((window.winfo_screenwidth()-10, 10), image=life1, anchor=tkinter.NE)
		elif playerTwo.health == 2:
			healthID2 = canvas.create_image((window.winfo_screenwidth()-10, 10), image=life2, anchor=tkinter.NE)
		elif playerTwo.health == 3:
			healthID2 = canvas.create_image((window.winfo_screenwidth()-10, 10), image=life3, anchor=tkinter.NE)
		elif playerTwo.health == 4:
			healthID2 = canvas.create_image((window.winfo_screenwidth()-10, 10), image=life4, anchor=tkinter.NE)
		elif playerTwo.health == 5:
			healthID2 = canvas.create_image((window.winfo_screenwidth()-10, 10), image=life5, anchor=tkinter.NE)
		elif playerTwo.health == 6:
			healthID2 = canvas.create_image((window.winfo_screenwidth()-10, 10), image=life6, anchor=tkinter.NE)
	
	todelPlayerOneShots = []
	todelPlayerTwoShots = []
	todelenemyshots = []
	todelenemies = []
	todelupgrades = []
	for x in enemies:
	
		for y in playerOne.playerShots:
		
			#calculate enemy > shot collisions
			
			if x.health <=0:
				continue
				
			gapX = x.loc_x - y.loc_x
			gapY = x.loc_y - y.loc_y
			gap = math.sqrt(gapX**2+gapY**2)
			
			if gap <= 25:
				if y.piercing == 1:
					y.preremove()
					todelPlayerOneShots.append(y)
					
				else:
					y.piercing -= 1
					
				#random reward
				x.health -= y.damage
				
				if x.health <= 0:
					x.preremove()
					
					if wave != 0:
						rand = random.randint(1,100)
						playerOne.score += 10
						
						if (rand == 42 or rand == 7):
							randw = random.randint(1,100)
							
							if randw < 50:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.LASER, image=laserUpgradeImage))
								
							elif randw < 75:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.PLAZMA, image=plazmaUpgradeImage))
								
							elif randw < 99:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.HULLBREAKER, image=hullbreakerUpgradeImage))
								
							elif randw == 100:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.DEVASTATOR, image=devastatorUpgradeImage))
							
					todelenemies.append(x)
		
		if playerTwo != None:	
			for y in playerTwo.playerShots:
			
				#calculate enemy > shot collisions
				
				if x.health <=0:
					continue
					
				gapX = x.loc_x - y.loc_x
				gapY = x.loc_y - y.loc_y
				gap = math.sqrt(gapX**2+gapY**2)
				
				if gap <= 25:
					if y.piercing == 1:
						y.preremove()
						todelPlayerTwoShots.append(y)
						
					else:
						y.piercing -= 1
						
					#random reward
					rand = random.randint(1,100)
					x.health -= y.damage
					
					if x.health <= 0:
						x.preremove()
						playerTwo.score += 10
						
						if (rand == 42 or rand == 7):
							randw = random.randint(1,100)
							
							if randw < 50:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.LASER, image=laserUpgradeImage))
								
							elif randw < 75:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.PLAZMA, image=plazmaUpgradeImage))
								
							elif randw < 99:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.HULLBREAKER, image=hullbreakerUpgradeImage))
								
							elif randw == 100:
								upgrades.append(upgrade(x.loc_x, x.loc_y, weapon.DEVASTATOR, image=devastatorUpgradeImage))
								
						todelenemies.append(x)


		#calculate enemy > player collisions
		gapX1 = x.loc_x - playerOne.loc_x
		gapY1 = x.loc_y - playerOne.loc_y
		gap1 = math.sqrt(gapX1**2+gapY1**2)
		
		
		if playerTwo != None:
			gapX2 = x.loc_x - playerTwo.loc_x
			gapY2 = x.loc_y - playerTwo.loc_y
			gap2 = math.sqrt(gapX2**2+gapY2**2)
		
		if gap1 <= 25 and not playerOne.invincible:
			x.preremove()
			todelenemies.append(x)
			playerOne.health -= 1
			if playerOne.health > 0:
				playerOne.changeImage(imagefile="data/images/player1-inv.gif")
				window.after(3000, lambda: removeInvinsibility(playerOne, "data/images/player1.gif"))
			playerOne.addLocation(-playerOne.loc_x+window.winfo_screenwidth()/2-25, -playerOne.loc_y+window.winfo_screenheight()-(window.winfo_screenheight()/8))
			playerOne.weaponLevel = max(0, playerOne.weaponLevel-2)
			playerOne.invincible = True
			
			if playerOne.health == 0:
				#gameover
				playerOne.weaponType = weapon.NONE
				playerOne.preremove()
				#canvas.create_text((window.winfo_screenwidth()/2, window.winfo_screenheight()/2), text="Game Over\nYou have scored "+str(score)+" points", fill="white", font=("System 24 bold"))
		
		
		if playerTwo != None and gap2 <= 25 and not playerTwo.invincible:
			x.preremove()
			todelenemies.append(x)
			playerTwo.health -= 1
			if playerTwo.health > 0:
				playerTwo.changeImage(imagefile="data/images/player2-inv.gif")
				window.after(3000, lambda: removeInvinsibility(playerTwo, "data/images/player2.gif"))
			playerTwo.addLocation(-playerTwo.loc_x+window.winfo_screenwidth()/2-25, -playerTwo.loc_y+window.winfo_screenheight()-(window.winfo_screenheight()/8))
			playerTwo.weaponLevel = max(0, playerTwo.weaponLevel-2)
			playerTwo.invincible = True
			
			if playerTwo.health == 0:
				#gameover
				playerTwo.weaponType = weapon.NONE
				playerTwo.preremove()
				#canvas.create_text((window.winfo_screenwidth()/2, window.winfo_screenheight()/2), text="Game Over\nYou have scored "+str(score)+" points", fill="white", font=("System 24 bold"))
		
		#move the enemy
		x.autoLocate()
		#randomly shoot the player
		
		if ((random.randint(1,1000) <= 3) or (random.randint(1,1000) <= 7 and bullethellMode)) and wave != 0:
			enemyshots.append(shot(x.loc_x, x.loc_y, image=eggWeaponImage, vel_y=random.randint(5,15)))
			if bullethellMode:
				enemyshots.append(shot(x.loc_x, x.loc_y, image=eggWeaponImage, vel_y=random.randint(5,15), vel_x=random.randint(1,5)))
				enemyshots.append(shot(x.loc_x, x.loc_y, image=eggWeaponImage, vel_y=random.randint(5,15), vel_x=-random.randint(1,5)))
			
	#calculate enemyshots > player collisions
	for x in enemyshots:
	
		gapX1 = x.loc_x - playerOne.loc_x
		gapY1 = x.loc_y - playerOne.loc_y
		gap1 = math.sqrt(gapX1**2+gapY1**2)
		
		if playerTwo != None:
			gapX2 = x.loc_x - playerTwo.loc_x
			gapY2 = x.loc_y - playerTwo.loc_y
			gap2 = math.sqrt(gapX2**2+gapY2**2)
		
		if gap1 <= 25 and not playerOne.invincible:
			x.preremove()
			todelenemyshots.append(x)
			playerOne.health -= 1
			if playerOne.health > 0:
				playerOne.changeImage(imagefile="data/images/player1-inv.gif")
				window.after(3000, lambda: removeInvinsibility(playerOne, "data/images/player1.gif"))
			playerOne.addLocation(-playerOne.loc_x+window.winfo_screenwidth()/2-25, -playerOne.loc_y+window.winfo_screenheight()-(window.winfo_screenheight()/8))
			playerOne.weaponLevel = max(0, playerOne.weaponLevel-2)
			playerOne.invincible = True
			
			if playerOne.health == 0:
				#gameover
				playerOne.weaponType = weapon.NONE
				playerOne.preremove()
				#canvas.create_text((window.winfo_screenwidth()/2, window.winfo_screenheight()/2), text="Game Over\nYou have scored "+str(score)+" points", fill="white", font=("System 24 bold"))
		
		if playerTwo != None and gap2 <= 25 and not playerTwo.invincible:
			x.preremove()
			todelenemyshots.append(x)
			playerTwo.health -= 1
			if playerTwo.health > 0:
				playerTwo.changeImage(imagefile="data/images/player2-inv.gif")
				window.after(3000, lambda: removeInvinsibility(playerTwo, "data/images/player2.gif"))
			playerTwo.addLocation(-playerTwo.loc_x+window.winfo_screenwidth()/2-25, -playerTwo.loc_y+window.winfo_screenheight()-(window.winfo_screenheight()/8))
			playerTwo.weaponLevel = max(0, playerTwo.weaponLevel-2)
			playerTwo.invincible = True
			
			if playerTwo.health == 0:
				#gameover
				playerTwo.weaponType = weapon.NONE
				playerTwo.preremove()
				#canvas.create_text((window.winfo_screenwidth()/2, window.winfo_screenheight()/2), text="Game Over\nYou have scored "+str(score)+" points", fill="white", font=("System 24 bold"))	
		x.update()
		
		if x.loc_x >= window.winfo_screenwidth() or x.loc_y >= window.winfo_screenheight()+15 or x.loc_x < 0:
			if (x.loc_x >= window.winfo_screenwidth() or x.loc_x <= 0) and bullethellMode:
				x.vel_x = -x.vel_x
			else:
				x.preremove()
				todelenemyshots.append(x)
	
	#calculate upgrades > player collisions
	for x in upgrades:
		gapX1 = x.loc_x - playerOne.loc_x
		gapY1 = x.loc_y - playerOne.loc_y
		gap1 = math.sqrt(gapX1**2+gapY1**2)
		
		if playerTwo != None:
			gapX2 = x.loc_x - playerTwo.loc_x
			gapY2 = x.loc_y - playerTwo.loc_y
			gap2 = math.sqrt(gapX2**2+gapY2**2)
		
		if gap1 <= 25 and playerOne.health > 0:
			x.preremove()
			todelupgrades.append(x)
			playerOne.score += 100
			if playerOne.weaponType == x.type and playerOne.weaponLevel < len(playerOne.weaponType["level"])-1:
				playerOne.weaponLevel += 1
			if playerOne.weaponType != x.type:
				playerOne.weaponType = x.type
				playerOne.weaponLevel = 0
				
		
		if playerTwo != None and gap2 <= 25 and playerTwo.health > 0:
			x.preremove()
			todelupgrades.append(x)
			playerTwo.score += 100
			if playerTwo.weaponType == x.type and playerTwo.weaponLevel < len(playerTwo.weaponType["level"])-1:
				playerTwo.weaponLevel += 1
			if playerTwo.weaponType != x.type:
				playerTwo.weaponType = x.type
				playerTwo.weaponLevel = 0
				
		x.update()
		
		if x.loc_x >= window.winfo_screenwidth() or x.loc_y >= window.winfo_screenheight()+15:
			x.preremove()
			todelupgrades.append(x)

	for x in playerOne.playerShots:
		#move players shots
		x.update()
		if x.loc_x <= 0 or x.loc_y <= 0 or x.loc_x > window.winfo_screenwidth():
			#if the shot is outside the screen delete it
			x.preremove()
			todelPlayerOneShots.append(x)
	
	if playerTwo != None:
		for x in playerTwo.playerShots:
			#move players shots
			x.update()
			if x.loc_x <= 0 or x.loc_y <= 0 or x.loc_x > window.winfo_screenwidth():
				#if the shot is outside the screen delete it
				x.preremove()
				todelPlayerTwoShots.append(x)
	
	for x in todelenemies:
		try:
			enemies.remove(x)
		except:
			pass #if the enemy was already deleted ignore exception
		
	for x in todelPlayerOneShots:
		try:
			playerOne.playerShots.remove(x)
		except:
			pass
	
	if playerTwo != None:
		for x in todelPlayerTwoShots:
			try:
				playerTwo.playerShots.remove(x)
			except:
				pass
	
	for x in todelenemyshots:
		try:
			enemyshots.remove(x)
		except:
			pass
			
	for x in todelupgrades:
		try:
			upgrades.remove(x)
		except:
			pass
			
	if len(enemies) == 0 and len(todelenemies) != 0:
		prespawnNextWave()
		
		
	if scbu1 < int(playerOne.score/10000) and playerOne.health < 6:
		playerOne.health += 1
	
	if playerTwo != None and scbu2 < int(playerTwo.score/10000) and playerTwo.health < 6:
		playerTwo.health += 1
	
	#
	# Update player new controller source code
	#
	
	playerOne.update()
	
	if playerTwo != None:
		playerTwo.update()
		
	window.after(32, update)
	
def removeInvinsibility(pl:Player, imagefile):
	pl.invincible = False
	if pl.health > 0:
		pl.changeImage(imagefile=imagefile)
	
def prespawnNextWave():

	global wave
	
	wave += 1
	v = wave % 10
	
	if v == 4:
		id1 = canvas.create_image((200,window.winfo_screenheight()-200), image=dangerImage)
		id2 = canvas.create_image((window.winfo_screenwidth()-200,window.winfo_screenheight()-200), image=dangerImage)
		window.after(5000, lambda canvas=canvas, id1=id1: canvas.delete(id1))
		window.after(5000, lambda canvas=canvas, id2=id2: canvas.delete(id2))
		
	elif v == 6:
		id = canvas.create_image((window.winfo_screenwidth()/2,window.winfo_screenheight()-200), image=dangerImage)
		window.after(5000, lambda canvas=canvas, id=id: canvas.delete(id))
		
	elif v == 9:
		id = canvas.create_text((window.winfo_screenwidth()/2, 100), text="Bonus level", fill="white", font=("System 32 bold"))
		window.after(5000, lambda canvas=canvas, id=id: canvas.delete(id))
		
	window.after(3000, lambda: spawnNextWave(None))
	
	
def spawnNextWave(e):

	v = wave % 10
	
	if v == 1:
		for y in range(0,6):
			for x in range(0,6):
				if y % 2 == 0:
					enemies.append(entity(-60*x, 50+60*y, image=enemyImage, health=wave))
					
				else:
					enemies.append(entity(window.winfo_screenwidth()+60*x, 50+60*y, image=enemyImage, vel_x=-2, health=wave))
					
	elif v == 2:
		for y in range(0,6):
			for x in range(0,12):
				enemies.append(entity(-60*x, 50+60*y, image=enemyImage, health=wave))
				
	elif v == 3:
		enemies.append(entity(0, window.winfo_screenheight()/4, image=enemyImage, vel_x=random.randint(3,5), vel_y=random.randint(-5,5), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*2, image=enemyImage, vel_x=random.randint(3,5), vel_y=random.randint(-5,5), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*3, image=enemyImage, vel_x=random.randint(3,5), vel_y=random.randint(-5,5), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4, image=enemyImage, vel_x=random.randint(3,5), vel_y=random.randint(-5,5), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*2, image=enemyImage, vel_x=random.randint(3,5), vel_y=random.randint(-5,5), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*3, image=enemyImage, vel_x=random.randint(3,5), vel_y=random.randint(-5,5), health=wave))
		
	elif v == 4:
		for x in range(0,36):
			enemies.append(entity(x*-60, window.winfo_screenheight()+x*60, image=enemyImage, vel_x=5, vel_y=-5, health=wave))
		for x in range(0,36):
			enemies.append(entity(window.winfo_screenwidth()+x*60, window.winfo_screenheight()+x*60, image=enemyImage, vel_x=5, vel_y=-5, health=wave))
			
	elif v == 5:
		for y in range(0,6):
			for x in range(0,20):
				if y % 2 == 0:
					enemies.append(entity(-60*x, 50+60*y, image=enemyImage, health=wave))
					
				else:
					enemies.append(entity(window.winfo_screenwidth()+60*x, 50+60*y, image=enemyImage, vel_x=-2, health=wave))
					
	elif v == 6:
		for x in range(0,36):
			enemies.append(entity(x*-60, x*-60, image=enemyImage, vel_x=5, vel_y=-5, health=wave))
			
		for x in range(0,36):
			enemies.append(entity(window.winfo_screenwidth()+x*60, x*-60, image=enemyImage, vel_x=5, vel_y=-5, health=wave))
			
	elif v == 7:
		enemies.append(entity(0, window.winfo_screenheight()/4, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*2, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*3, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6*2, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6*4, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*2, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*3, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6*2, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6*4, image=enemyImage, vel_x=random.randint(3,10), vel_y=random.randint(-10,10), health=wave))
		
	elif v == 8:
		for y in range(0,6):
			for x in range(0,24):
				if y % 2 == 0:
					enemies.append(entity(-60*x, 50+60*y, image=enemyImage, health=wave))
					
				else:
					enemies.append(entity(window.winfo_screenwidth()+60*x, 50+60*y, image=enemyImage, vel_x=-2, health=wave))
					
	elif v == 9:
		#bonus
		randw = random.randint(1,4)
		if randw == 1:
			upgrades.append(upgrade(window.winfo_screenwidth()/2, 0, weapon.LASER, image=laserUpgradeImage))
			
		elif randw == 2:
			upgrades.append(upgrade(window.winfo_screenwidth()/2, 0, weapon.PLAZMA, image=plazmaUpgradeImage))
			
		elif randw == 3:
			upgrades.append(upgrade(window.winfo_screenwidth()/2, 0, weapon.HULLBREAKER, image=hullbreakerUpgradeImage))
			
		elif randw == 4:
			upgrades.append(upgrade(window.winfo_screenwidth()/2, 0, weapon.DEVASTATOR, image=devastatorUpgradeImage))
			
		window.after(2000, lambda: prespawnNextWave())
		
	elif v == 0:
		enemies.append(entity(0, window.winfo_screenheight()/4, image=enemyImage, vel_x=3, vel_y=-2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*2, image=enemyImage, vel_x=3, vel_y=3, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*3, image=enemyImage, vel_x=3, vel_y=2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6, image=enemyImage, vel_x=5, vel_y=-2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6*2, image=enemyImage, vel_x=5, vel_y=-3, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6*4, image=enemyImage, vel_x=5, vel_y=2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4, image=enemyImage, vel_x=7, vel_y=-2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*2, image=enemyImage, vel_x=7, vel_y=3, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/4*3, image=enemyImage, vel_x=7, vel_y=2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6, image=enemyImage, vel_x=7, vel_y=2, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6*2, image=enemyImage, vel_x=7, vel_y=3, health=wave))
		enemies.append(entity(0, window.winfo_screenheight()/6*4, image=enemyImage, vel_x=7, vel_y=-2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4, image=enemyImage, vel_x=3, vel_y=-2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*2, image=enemyImage, vel_x=3, vel_y=3, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*3, image=enemyImage, vel_x=3, vel_y=2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6, image=enemyImage, vel_x=5, vel_y=-2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6*2, image=enemyImage, vel_x=5, vel_y=-3, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6*4, image=enemyImage, vel_x=5, vel_y=2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4, image=enemyImage, vel_x=7, vel_y=2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*2, image=enemyImage, vel_x=7, vel_y=-3, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/4*3, image=enemyImage, vel_x=7, vel_y=-2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6, image=enemyImage, vel_x=7, vel_y=2, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6*2, image=enemyImage, vel_x=7, vel_y=3, health=wave))
		enemies.append(entity(window.winfo_screenwidth(), window.winfo_screenheight()/6*4, image=enemyImage, vel_x=7, vel_y=-2, health=wave))
		
		
def quit(event):
	window.destroy()

def setFire(player, value):
	if player != None:
		player.updateShoot = value

def menuBullethellMode():
	global bullethellMode
	for x in enemies:
		x.justRemove()
	enemies.clear()
	bullethellMode = True
	
	enemies.append(MenuEntity(int(window.winfo_screenwidth()/4), 100, menuOnePlayerMode, imagefile="data/images/temp/opm.gif"))
	enemies.append(MenuEntity(int(window.winfo_screenwidth()/4*3), 100, menuTwoPlayerMode, imagefile="data/images/temp/tpm.gif"))
	
def menuNormalMode():
	global bullethellMode
	for x in enemies:
		x.justRemove()
	enemies.clear()
	bullethellMode = False
	
	enemies.append(MenuEntity(int(window.winfo_screenwidth()/4), 100, menuOnePlayerMode, imagefile="data/images/temp/opm.gif"))
	enemies.append(MenuEntity(int(window.winfo_screenwidth()/4*3), 100, menuTwoPlayerMode, imagefile="data/images/temp/tpm.gif"))
	
def menuOnePlayerMode():
	for x in enemies:
		x.justRemove()
	enemies.clear()
	
	playerOne.invincible = False
	
	#window.after(30, lambda: prespawnNextWave())
	
def menuTwoPlayerMode():
	global playerTwo
	for x in enemies:
		x.justRemove()
	enemies.clear()
	
	playerTwo = Player(window.winfo_screenwidth()/2+75, window.winfo_screenheight()-(window.winfo_screenheight()/8), imagefile="data/images/player2.gif")

	playerOne.invincible = False
	playerTwo.invincible = False
	
	#window.after(30, lambda: prespawnNextWave())
	
canvas = tkinter.Canvas(window, bg="black", width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack()

canvas.bind_all("<KeyPress>", controllerDown)
canvas.bind_all("<KeyRelease>", controllerUp)
canvas.bind_all("<KeyPress-space>", lambda e: setFire(playerOne, True))
canvas.bind_all("<KeyRelease-space>", lambda e: setFire(playerOne, False))
canvas.bind_all("<KeyPress-Return>", lambda e: setFire(playerTwo, True))
canvas.bind_all("<KeyRelease-Return>", lambda e: setFire(playerTwo, False))
canvas.bind_all("<End>", quit)
canvas.bind_all("<Escape>", quit)
canvas.bind_all("<Motion>", controllerMouse)
canvas.bind_all("<ButtonPress-1>", lambda e: setFire(playerOne, True))
canvas.bind_all("<ButtonRelease-1>", lambda e: setFire(playerOne, False))

dangerImage = tkinter.PhotoImage(file="data/images/danger.gif")
eggWeaponImage = tkinter.PhotoImage(file="data/images/weapons/egg.gif")
laserUpgradeImage = tkinter.PhotoImage(file="data/images/upgrades/laser.gif")
plazmaUpgradeImage = tkinter.PhotoImage(file="data/images/upgrades/plazma.gif")
hullbreakerUpgradeImage = tkinter.PhotoImage(file="data/images/upgrades/hullbreaker.gif")
devastatorUpgradeImage = tkinter.PhotoImage(file="data/images/upgrades/devastator.gif")
enemyImage = tkinter.PhotoImage(file="data/images/enemy.gif")
backgroundImage = tkinter.PhotoImage(file="data/images/background.gif")
backgroundImage1 = tkinter.PhotoImage(file="data/images/background1.gif")

life1 = tkinter.PhotoImage(file="data/images/Life Bar/Life-1.gif")
life2 = tkinter.PhotoImage(file="data/images/Life Bar/Life-2.gif")
life3 = tkinter.PhotoImage(file="data/images/Life Bar/Life-3.gif")
life4 = tkinter.PhotoImage(file="data/images/Life Bar/Life-4.gif")
life5 = tkinter.PhotoImage(file="data/images/Life Bar/Life-5.gif")
life6 = tkinter.PhotoImage(file="data/images/Life Bar/Life-6.gif")

bg1 = canvas.create_image((0,backgroundImage.height()/2), image=backgroundImage, anchor=tkinter.NW)
bg2 = canvas.create_image((0,-(backgroundImage1.height()/2)), image=backgroundImage1, anchor=tkinter.NW)
bg1pos = backgroundImage.height()/2
bg2pos = -(backgroundImage.height()/2)

enemyshots = []
enemies = []
upgrades = []

playerOne = Player(window.winfo_screenwidth()/2-75, window.winfo_screenheight()-(window.winfo_screenheight()/8), imagefile="data/images/player1.gif")
playerTwo = None

playerOne.invincible = True

canvas.create_text(window.winfo_screenwidth()-10, window.winfo_screenheight()-40, text="V1.2.1", fill="white", anchor=tkinter.NE, font=("System 20 bold"))

scoreID1 = 0
scoreID2 = 0
healthID1 = 0
healthID2 = 0
waveID = 0
wave = 0

bullethellMode = False

enemies.append(MenuEntity(int(window.winfo_screenwidth()/4), 100, menuBullethellMode, imagefile="data/images/temp/bhm.gif"))
enemies.append(MenuEntity(int(window.winfo_screenwidth()/4*3), 100, menuNormalMode, imagefile="data/images/temp/nm.gif"))

update()
window.mainloop()