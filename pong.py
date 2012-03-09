import pygame, sys, os


def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer:
		return NoneSound()
	fullname = os.path.join('grenade.wav', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print "Cannot load sound: ", wav
		raise SystemExit, message
	return sound

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE1_START_X = 10
PADDLE1_START_Y = 20
PADDLE2_START_X = 780
PADDLE2_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle1_rect = pygame.Rect((PADDLE1_START_X, PADDLE1_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2_rect = pygame.Rect((PADDLE2_START_X, PADDLE2_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score1 = 0
score2 = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

running = True
rematch = False
winner = "anyone"
r_for_rematch = "Press 'R' for a rematch!"

paddle_sound = load_sound("grenade.wav")

# Game loop
while running == True:

	while rematch == True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
		if pygame.key.get_pressed()[pygame.K_r]:
			score1 = 0
			score2 = 0
			rematch = False
		winning_text = font.render(str(winner), True, (255, 0, 0))
		rematch_text = font.render(str(r_for_rematch), True, (255, 0, 0))
		screen.blit(winning_text, (340, 200))
		screen.blit(rematch_text, (340, 230))
		pygame.display.flip()
		pygame.time.delay(20)


	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle1_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle1_rect.top < 0:
				paddle1_rect.top = 0
			elif paddle1_rect.bottom >= SCREEN_HEIGHT:
				paddle1_rect.bottom = SCREEN_HEIGHT

	# This test if w/up or s/down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_w] and paddle1_rect.top > 0:
		paddle1_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_s] and paddle1_rect.bottom < SCREEN_HEIGHT:
		paddle1_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_UP] and paddle2_rect.top > 0:
		paddle2_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle2_rect.bottom < SCREEN_HEIGHT:
		paddle2_rect.bottom += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	#if ball_rect.right >= SCREEN_WIDTH or ball_rect.left <= 0:
		#ball_speed[0] = -ball_speed[0]
		#ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))
		
	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle1_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		paddle_sound.play()
		#score1 += 1
	if paddle2_rect.colliderect(ball_rect):
		ball_speed[0] = -ball_speed[0]
		paddle_sound.play()


	if ball_rect.right >= SCREEN_WIDTH:
		score1 += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

	if ball_rect.left <= 0:
		score2 += 1
		ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))




	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle1_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), paddle2_rect)
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	score_text_1 = font.render(str(score1), True, (0, 0, 0))
	score_text_2 = font.render(str(score2), True, (0, 0, 0))
	screen.blit(score_text_1, (((SCREEN_WIDTH / 2) - 10) - font.size(str(score1))[0] / 2, 5))
	screen.blit(score_text_2, (((SCREEN_WIDTH / 2) + 10) - font.size(str(score2))[0] / 2, 5))
	pygame.draw.line(screen, (0, 0, 255), (400, 0), (400, 800))

	if score1 == 11:
		winner = "Player 1 wins!"
		rematch = True
		#print "rematch"
	if score2 == 11:
		winner = "Player 2 wins!"
		rematch = True

	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
