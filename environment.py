from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random
import pygame

metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

class FlippyEnv(Env):
	def __init__(self):
		super(FlippyEnv, self).__init__()
		self.len_goal = 100
		self.action_space = Discrete(2)
		self.observation_space = Box(low=-1280, high=1280, shape=(3, ), dtype=np.float32)
		#self.state = 38 + random.randint(-3, 3)

		self.width = 1280
		self.height = 720
		self.screen = None
		self.clock = None
		self.isopen = True

		self.g = 6
		self.a = 40
		self.done = False
		self.x = 0

	def step(self, action):

		self.reward = 0
		if action == 1:

			self.countOfActions += 1
			self.a = 40

			if self.prefReward == 10:
				self.reward = 2
			self.reward = 10

		noise = abs(10 * random.uniform(-1, 1))
		self.a -= self.g
		self.positionY -= self.a + noise



		if self.positionY <= self.topY and self.positionY  >= self.buttomY:
			self.done = False
			# self.reward += 2
		else:

			self.done = True
			self.reward -= 30

		# if self.countOfActions > self.len_goal:
		# 	print(self.countOfActions)
		# 	self.done = True

		self.bird = pygame.Rect(self.positionX - self.scaleX // 2, self.positionY - self.scaleY // 2,
								self.scaleX, self.scaleY)

		self.tubes.SetPlayerRect(self.bird)
		self.tubes.Moving()


		if self.tubes.GetScore() != self.prefScore:
			self.reward += 100
			self.prefScore = self.tubes.GetScore()


		if self.tubes.GetCountCollision() != 0:
			self.reward = -20
			self.tubes.SetCountCollision(0)
			self.done = True


		# self.x += 1
		# if self.x % 2 == 0:
		# 	if self.topY > self.height // 4:
		# 		self.topY -= 1
		# 	if self.buttomY < self.height - self.height // 4:
		# 		self.buttomY += 1
		#
		# 	self.x = 0

		self.prefReward = self.reward


			
		info = {"score": self.countOfActions}

		x, y = self.tubes.GetPositionsCentrOfTubes()

		self.deltaX = round(x - self.positionX)
		self.deltaY = round(y - self.positionY)

		observation = [ self.deltaX, self.deltaY, self.positionY]
		# observation = [self.positionY]
		observation = np.array(observation, dtype=np.float32)

		return observation, self.reward, self.done, info
		
	def render(self, mode="human"):
		import pygame
		from pygame import gfxdraw

		if self.screen is None:
			pygame.init()
			pygame.display.init()
			self.screen = pygame.display.set_mode((self.width, self.height))

		if self.clock is None:
			self.clock = pygame.time.Clock()

		self.surf = pygame.Surface((self.width, self.height))
		self.surf.fill((255, 255, 255))



		# topTube = [(0, self.height),
		# 		   (self.width, self.height),
		# 		   (self.width, self.topY),
		# 		   (0, self.topY)]
		#
		# buttomTube = [(0, 0),
		# 		  (self.width, 0),
		# 		  (self.width, self.buttomY),
		# 		  (0, self.buttomY)]
		#
		# gfxdraw.filled_polygon(self.surf, buttomTube, (202, 152, 101))
		# gfxdraw.filled_polygon(self.surf, topTube, (202, 152, 101))

		for tube in self.tubes.Tubes:
			pygame.draw.rect(self.surf, (255, 0, 0), tube[0])
			pygame.draw.rect(self.surf, (255, 0, 0), tube[1])
			pygame.draw.rect(self.surf, (0, 0, 255), tube[2], 3)

		self.bird = pygame.Rect(self.positionX - self.scaleX // 2, self.positionY - self.scaleY // 2,
						   self.scaleX, self.scaleY)

		# bird = [(self.positionX, self.positionY),
		# 		(self.positionX, self.positionY + self.scaleY),
		# 		(self.positionX + self.scaleX, self.positionY + self.scaleY),
		# 		(self.positionX + self.scaleX, self.positionY)]
		#
		# gfxdraw.filled_polygon(self.surf, bird, (202, 152, 101))

		# pygame.draw.circle(self.surf, (0, 0, 0), self.tubes.GetPositionsCentrOfTubes(), 50, 5)

		pygame.draw.rect(self.surf, (0, 0, 0), self.bird)

		font = pygame.font.Font(pygame.font.get_default_font(), 36)
		text_surface = font.render(f'deltaX: {self.deltaX} deltaY: {self.deltaY} Score:{self.tubes.GetScore()}]', True, (0, 0, 0))
		self.surf.blit(text_surface, dest=(0, 0))

		# self.surf = pygame.transform.flip(self.surf, False, True)
		self.screen.blit(self.surf, (0, 0))


		if mode == "human":
			pygame.event.pump()
			self.clock.tick(30)
			pygame.display.flip()
		if mode == "rgb_array":
			return np.transpose(
				np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
			)
		else:
			return self.isopen
		
	def reset(self, seed=None):
		# super().reset(seed=seed)
		self.reward = 0
		self.prefReward = 0
		self.countOfActions = 0
		self.a = 40
		self.prefScore = 0

		self.tubes = Tubes(self.width, self.height)
		self.tubes.Create()

		self.positionX = 300
		self.positionY = 300
		
		self.scaleX = 30
		self.scaleY = 20
		
		self.topY = self.height 
		self.buttomY = 0
		
		self.done = False

		self.bird = pygame.Rect(self.positionX - self.scaleX // 2, self.positionY - self.scaleY // 2,
								self.scaleX, self.scaleY)

		self.tubes.SetPlayerRect(self.bird)
		x, y = self.tubes.GetPositionsCentrOfTubes()

		self.deltaX = round(x - self.positionX)
		self.deltaY = round(y - self.positionY)

		# observation = [self.positionY]
		observation = [ self.deltaX, self.deltaY, self.positionY]
		observation = np.array(observation, dtype=np.float32)
		
		return observation
		

	def close(self):
		print(self.countOfActions)
		if self.screen is not None:
			import pygame

			pygame.display.quit()
			pygame.quit()
			self.isopen = False

class Tubes():

	def __init__(self, width, height):
		self.Tubes = []
		self.speed = 10
		self.width = width
		self.height = height
		self.CountCollision = 0
		self.Score = 0

	def Create(self, ):


		self.Distance = 400
		self.Scale = 50

		Distortion = round(random.random() * 150)

		# нижняя труба
		a1 = self.width
		b1 = 0
		x1 = (self.height - self.Distance) // 2 + Distortion
		y1 = self.Scale

		r1 = pygame.Rect((a1, b1, y1, x1))

		# вверхняя труба
		a2 = self.width
		b2 = x1 + self.Distance
		x2 = self.height // 2 - Distortion
		y2 = self.Scale

		r2 = pygame.Rect((a2, b2, y2, x2))

		# пространство между трубами
		a = self.width
		b = (self.height - self.Distance) // 2 + Distortion
		x = self.Distance
		y = self.Scale

		r = pygame.Rect((a, b, y, x))

		self.Tubes.append([r1, r2, r, True, False])

	def Moving(self):

		for tube in self.Tubes:

			tube[0].x -= self.speed
			tube[1].x -= self.speed
			tube[2].x -= self.speed

			self.DistanceOfNewObstacles = self.width / 2

			if tube[0].x < self.DistanceOfNewObstacles:
				if tube[3] == True:
					self.Create()
					tube[3] = False

			self.Collision(tube[0])
			self.Collision(tube[1])
			tube[4] = self.OutOfCollision(tube[2], tube[4])

			if tube[0].x < -self.Scale:
				#self.Score += 1
				self.Tubes.remove(tube)

	def Collision(self, RectOfObstacle):
		if RectOfObstacle.colliderect(self.PlayerRect):
			self.CountCollision += 1

	def SetPlayerRect(self, PlayerRect):
		self.PlayerRect = PlayerRect

	def GetPositionsCentrOfTubes(self):
		if self.Tubes[0][2].x > self.PlayerRect.x - self.Scale // 2:
			x = self.Tubes[0][2].x + self.Tubes[0][2].width
			y = self.Tubes[0][2].y + self.Tubes[0][2].height // 2
		else:
			x = self.Tubes[1][2].x + self.Tubes[1][2].width
			y = self.Tubes[1][2].y + self.Tubes[1][2].height // 2
		return x, y

	def GetCountCollision(self):
		return self.CountCollision

	def SetCountCollision(self, CountCollision):
		self.CountCollision = CountCollision


	def OutOfCollision(self, RectOfCollision, IsCollision):
		if RectOfCollision.colliderect(self.PlayerRect):
			if IsCollision == False:
				IsCollision = True

		if IsCollision == True:
			if not RectOfCollision.colliderect(self.PlayerRect):
				self.Score += 1
				IsCollision = False
		return IsCollision

	def GetScore(self):
		return self.Score

	def SetScore(self, score):
		self.Score = score