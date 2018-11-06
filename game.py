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
		
	def draw( self, surface, index, x, y, orientation ):
		if orientation == "l":
			surface.blit( self.megaman_flipped, ( x - self.cellwidth / 2, y ), self.cells[9 - index] )
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

class Player():
	def __init__( self ):
		self.x = 0
		self.y = 400
		self.speed = 8
		self.jump_speed = 8
		self.mass = 2
		
class Movement():
	def __init__( self ):
		self.jumping = False

	def move_left( self ):
		player.x += player.speed

	def move_right( self ):
		player.x -= player.speed	

	def stop( self ):
		if not self.jumping:
			sprites.draw( screen, 0, player.x, player.y, sprites.get_orientation() )

	def run( self, orientation ):
		if not self.jumping:
			sprites.set_orientation( orientation )
			list_sprites = [ 3, 4, 5 ]
			self.index = sprites.get_index()
			
			if self.index > 2:
				sprites.set_index( 0 )
				self.index = 0
			
			sprites.draw( screen, list_sprites[self.index], player.x, player.y, orientation )	
			sprites.set_index( self.index + 1 )
		sprites.set_orientation( orientation )

	def jump( self ):	
		self.jumping = True

	def update( self ):
		if self.jumping:
			if player.jump_speed > 0:
				F = ( 0.5 * player.mass * ( player.jump_speed * player.jump_speed ) )
			else:
				F = -( 0.5 * player.mass * ( player.jump_speed * player.jump_speed ) )

			player.y = player.y - F
			player.jump_speed = player.jump_speed - 1
			if player.y >= 400:
				player.y = 400
				self.jumping = False
				player.jump_speed = 8
			sprites.draw( screen, 6, player.x, player.y, sprites.get_orientation() )


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
		movement.run( "r" )
		movement.move_left()
	elif key[pygame.K_a]:
		movement.run( "l" )
		movement.move_right()
	elif key[pygame.K_w]:
		movement.jump()
	else:
		movement.stop()
	
	movement.update()	
	pygame.display.flip()