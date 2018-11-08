import pygame

class Sprites():
	def __init__( self, cols, rows ):
		self.megaman = pygame.image.load( "megaman.png" ).convert_alpha()
		self.megaman = pygame.transform.scale( self.megaman, ( 1200, 1000 ) )
		self.megaman_flipped = pygame.image.load( "megaman_flipped.png" ).convert_alpha()
		self.megaman_flipped = pygame.transform.scale( self.megaman_flipped, ( 1200, 1000 ) )
		self.index = 0
		self.orientation = "r"	

		self.cols = cols
		self.rows = rows
		self.total_cells = cols * rows
		
		self.rect = self.megaman.get_rect()
		w = self.cellwidth = int(self.rect.width / cols)
		h = self.cellheight = int(self.rect.height / rows)
		
		self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.total_cells)])
		
	def draw( self, surface, index, x, y, orientation, row = 0 ):
		if orientation == "l":
			surface.blit( self.megaman_flipped, ( x - self.cellwidth / 2, y ), self.cells[ 9 - index ] )
			#print(index)
			#print(( 9 + 10 * row ) - ( index ))
		if orientation == "r":
			surface.blit( self.megaman, ( x, y ), self.cells[index] )
	def get_index( self ):
		return self.index

	def set_index( self, index ):
		self.index = index

	def set_orientation( self, orientation ):
		self.orientation = orientation	

	def get_orientation( self ):
		return self.orientation

	def get_row( self, index ):
		return index // 9

class Player():
	def __init__( self ):
		self.x = 0
		self.y = 400
		self.speed = 8
		self.jump_speed = 7
		self.mass = 1
		self.states = {
			"run": False,
			"jump": False,
			"stop": False,
			"shoot": False,
			"on_air": False
		}

	def set_states( self, states ):
		self.states = states

	def get_states( self ):
		return self.states	
		
class Movement():
	def __init__( self ):
		self.jumping = False

	def check_keys( self, key ):
		states = player.get_states()	
		if key[pygame.K_w]:
			states["jump"] = True
			states["stop"] = False
			states["shoot"] = False
			states["run"] = False
			if key[pygame.K_d] or key[pygame.K_a]:
				states["run"] = True
				if key[pygame.K_SPACE]:
					states["shoot"] = True
			elif key[pygame.K_SPACE]:
				states["shoot"] = True
		elif key[pygame.K_d] or key[pygame.K_a] and not key[pygame.K_w]:
			states["run"] = True
			states["stop"] = False
			states["jump"] = False
			states["shoot"] = False
			if key[pygame.K_SPACE]:
				states["shoot"] = True
		else:
			states["stop"] = True
			states["run"] = False
			states["jump"] = False
			states["shoot"] = False
			if key[pygame.K_SPACE]:
				states["shoot"] = True
		player.set_states( states )

	def move_left( self ):
		player.x += player.speed

	def move_right( self ):
		player.x -= player.speed	

	def stop( self, state ):
		if not state["jump"]:
			sprites.draw( screen, 0, player.x, player.y, sprites.get_orientation() )

	def run( self, orientation, state ):
		if not state["jump"] and not state["shoot"]:
			sprites.set_orientation( orientation )
			list_sprites = [ 3, 4, 5 ]
			self.index = sprites.get_index()
			
			if self.index > 2:
				sprites.set_index( 0 )
				self.index = 0
			
			sprites.draw( screen, list_sprites[self.index], player.x, player.y, orientation, sprites.get_row( list_sprites[self.index] ) )	
			sprites.set_index( self.index + 1 )
		sprites.set_orientation( orientation )

	def shoot( self, state ):
		if state["stop"] and state["shoot"]:
			sprites.draw( screen, 12, player.x, player.y, sprites.get_orientation() )
		elif state["run"] and state["shoot"] and not state["jump"]:
			list_sprites = [ 13, 14, 15 ]
			self.index = sprites.get_index()
			print(self.index)
			if self.index > 2:
				sprites.set_index( 0 )
				self.index = 0

			sprites.draw( screen, self.index, player.x, player.y, sprites.get_orientation() )
			sprites.set_index( self.index + 1 )


	def jump( self ):	
		self.jumping = True

	def update( self ):
		state = player.get_states()
		if self.jumping:
			if player.jump_speed > 0:
				f = ( 0.5 * player.mass * ( player.jump_speed * player.jump_speed ) )
			else:
				f = -( 0.5 * player.mass * ( player.jump_speed * player.jump_speed ) )

			player.y = player.y - f
			player.jump_speed = player.jump_speed - 0.5
			if player.y >= 400:
				player.y = 400
				self.jumping = False
				player.jump_speed = 7
			sprites.draw( screen, 6, player.x, player.y, sprites.get_orientation() )
			state = player.get_states()
			state["on_air"] = True
		else:
			state["on_air"] = False	




pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode( ( width, height ) )
player = Player()
sprites = Sprites( 10, 7 )
movement = Movement()
clock = pygame.time.Clock()

while True:
	clock.tick( 30 )
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	screen.fill( ( 0, 0, 0 ) )		

	key = pygame.key.get_pressed()
	if key[pygame.K_d]:
		movement.run( "r", player.get_states() )
		movement.move_left()
		if key[pygame.K_w]:
			movement.jump()
		elif key[pygame.K_SPACE]:
			movement.shoot( player.get_states() )

	elif key[pygame.K_a]:
		movement.run( "l", player.get_states() )
		movement.move_right()
		if key[pygame.K_w]:
			movement.jump()
		elif key[pygame.K_SPACE]:
			movement.shoot( player.get_states() )

	elif key[pygame.K_w]:
		movement.jump()
		if key[pygame.K_d]:
			movement.run( "r", player.get_states() )
			movement.move_left()
		if key[pygame.K_a]:
			movement.run( "l", player.get_states() )
			movement.move_right()

	elif key[pygame.K_SPACE]:
		movement.shoot( player.get_states() )

	else:
		movement.stop( player.get_states() )
	
	movement.check_keys( key )
	movement.update()	
	pygame.display.flip()