import pygame
import random
import math

class obstacle():
	
	def __init__(self, Screen, Width, Height, Speed ):
		self.Screen = Screen
		self.Width = Width
		self.Height = Height
		self.Obstacles = list()
		self.Score = 0
		self.IsNewObstacles = False
		self.CountCollision = 0
		self.PlayerRect = None
		self.IsCollision = None
		self.speed = Speed
		self.isStoping = False
		self.frame = 1
		self.xTopTube = 0
		self.yTopTube = 0
		self.xButtonTube = 0
		self.yButtonTube = 0
		
	
	def Create(self, Distance, Scale):
		
			self.Distance = Distance
			self.Scale = Scale
			
			Distortion = round(random.random() * 600)
			
			
			#вверхняя труба
			a1 = self.Width
			b1 = -100
			x1 = (self.Height - Distance) // 2 + Distortion
			y1  = Scale
			
			r1 = pygame.Rect((a1, b1, y1, x1))
			
			#нижняя труба
			a2 = self.Width
			b2 = x1 + Distance - 100
			x2 = self.Height // 2 - Distortion
			y2 = Scale
			
			r2 = pygame.Rect((a2, b2, y2, x2))
			
			#пространство между трубами
			a = self.Width - 10
			b = (self.Height - Distance) // 2 - 100 + Distortion 
			x = Distance 
			y = Scale + 20
			
			r = pygame.Rect((a, b, y, x))
			
			self.Obstacles.append([r1, r2, r, True, False])
			
	
	def Moving(self):
		
		
		for ob in self.Obstacles:
			

			pygame.draw.rect(self.Screen, (255, 0, 0), ob[0])
			pygame.draw.rect(self.Screen, (255, 0, 0), ob[1])
			pygame.draw.rect(self.Screen, (0, 0, 255), ob[2], 3)			
			
			if self.isStoping == True:
				self.StopingMoving()
			
			if ob[3] == False: #or self.Score==0:
				self.xTopTube = ob[2].x + ob[2].width / 2
				self.yTopTube = ob[2].y
				self.xButtonTube = ob[2].x + ob[2].width / 2
				self.yButtonTube = ob[2].y + ob[2].height
			
			ob[0].x -= self.speed
			ob[1].x -= self.speed 
			ob[2].x -= self.speed 
			
			if self.Score < 10:
				self.DistanceOfNewObstacles = self.Width / 2
			

			if ob[0].x < self.DistanceOfNewObstacles:
				if ob[3] == True:
					self.Create(self.Distance, self.Scale)
					ob[3] = False
							
			self.Collision(ob[0])	
			self.Collision(ob[1])
			ob[4] = self.OutOfCollision(ob[2], ob[4])
			
			if ob[0].x < -self.Scale :
				#self.Score += 1
				self.Obstacles.remove(ob)
				
				
	def DoCollision(self):
			for ob in self.Obstacles:
				self.Collision(ob[0])	
				self.Collision(ob[1])
			
	
	def StopingMoving(self):
		
		self.speed = self.function(self.speed)
		
	def Stop(self):
		self.isStoping = True
		self.speed_0 = self.speed
		self.StopingMoving()
			
					
	def Get_score(self):
			return str(self.Score)
			
	
	def Set_score(self, score):
			self.Score = score
			
	def Collision(self, RectOfObstacle):
		if RectOfObstacle.colliderect(self.PlayerRect):
			self.CountCollision += 1
	
	def OutOfCollision(self, RectOfCollision, IsCollision):
		if RectOfCollision.colliderect(self.PlayerRect):
			if IsCollision == False:
				IsCollision = True
		
		if IsCollision == True:
			if not RectOfCollision.colliderect(self.PlayerRect):
				self.Score += 1
				IsCollision = False
		return IsCollision
				
	
	def SetPlayerRect(self, PlayerRect):
		self.PlayerRect = PlayerRect
	
	def GetCountCollision(self):
		return self.CountCollision
	
	def SetCountCollision(self, CountCollision):
		self.CountCollision = CountCollision
		
	def GetSpeed(self):
		return self.speed
		
	def SetFrame(self, frame):
		if frame <= 30:
			self.frame = frame
		
	def GetFrame(self):
		return self.frame
		
	def GetIsStoping(self):
		return self.isStoping
		
	def function(self, speed):
		x = self.frame / 30
		return round(-math.log10(x) * self.speed_0)
		
	def GetScale(self):
		return self.Scale
		
	def GetXTopTube(self):		
		return self.xTopTube
		
	def GetYTopTube(self):		
		return self.yTopTube
		
	def GetXButtomTube(self):		
		return self.xButtonTube 
		
	def GetYButtomTube(self):		
		return self.yButtonTube