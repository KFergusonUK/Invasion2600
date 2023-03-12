import pygame
import os.path
import time
from os import stat_result

previous_bullet_time = pygame.time.get_ticks()
width = 600
height = 400
display = pygame.display.set_mode((width, height)) #Width, Height
pygame.display.set_caption('INVASION 2600') #Window title
#pygame.display.set_icon(Icon_name) #Change Icon
fps = 60
clock = pygame.time.Clock()
startTime = time.time()
speed = 5
mobwidth = 6
mobheight = 3
distdiff = 50
offsetx = 400
offsety = 40
walls = []
win = False
lose = False
game1 = False
win_img = 'win.jpg'
loading = True
die_sound = False
win_sound = False
win_time = 0
score_count = 0


# Level 2 map:
level = [
  "WWWWWWWWWWWWWEWWWWWWWWWWWW",
  "W                        W",
  "W      WWWWWWWWWWWW      W",
  "W                        W",
  "W         W    W         W",
  "WWWWWWWWWWW    WWWWWWWWWWW",
  "W                        W",
  "W      W          W      W",
  "W      W          W      W",
  "WWWW   WWWWWWWWWWWW   WWWW",
  "W  W                  W  W",
  "W  W                  W  W",
  "W  WWWWWWWWW  WWWWWWWWW  W",
  "W          W  W          W",
  "WWWWWWWWWWWW  WWWWWWWWWWWW",
  "W                        W",
  "W                        W",
  "WWWWWWWWWWWWWWWWWWWWWWWWWW",
]

#Define Player:
class player(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('player1.png').convert_alpha()

    #Set position of Player:
    self.rect = self.image.get_rect() #Get image size and coord
    self.rect.x = 600 // 2
    self.rect.y = 400 - self.rect.height - 10

    #Movement set to 0
    self.velx = 0
    self.vely = 0
    self.speed = speed
    self.speedy = speed
    
  def update(self):
    self.speed = 0
    self.speedy = 0
    self.rect.x += self.velx
    self.rect.y += self.vely
    
    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_LEFT]:
      self.speed = -5
    if pressed_key[pygame.K_RIGHT]:
      self.speed = 5
    self.rect.x += self.speed

    #IF INVADERS IS WON, CHANGE MOVEMENT FOR TRON-ADVENTURE:
    if len(mobs) == 0:
      if pressed_key[pygame.K_UP]:
        if pressed_key[pygame.K_UP] and pressed_key[pygame.K_RIGHT]:
          self.speedy = 0
        elif pressed_key[pygame.K_UP] and pressed_key[pygame.K_LEFT]:
          self.speedy = 0
        else:
          self.speedy = -5
      if pressed_key[pygame.K_DOWN]:
        if pressed_key[pygame.K_DOWN] and pressed_key[pygame.K_RIGHT]:
          self.speedy = 0
        elif pressed_key[pygame.K_DOWN] and pressed_key[pygame.K_LEFT]:
          self.speedy = 0
        else:
          self.speedy = 5
      plyr.rect.y += self.speedy

      #STOP PLAYER MOVING THROUGH TRON-ADVENTURE/MAZE WALLS     
      for wall in walls:
        if plyr.rect.colliderect(wall.rect):
          if self.speed > 0:
            plyr.rect.right = wall.rect.left
          if self.speed < 0:
            plyr.rect.left = wall.rect.right
          if self.speedy > 0:
            plyr.rect.bottom = wall.rect.top
          if self.speedy < 0:
            plyr.rect.top = wall.rect.bottom
    
      #WIN CONDITION:
      if plyr.rect.colliderect(end_rect):
          global win
          win = True
          recog.kill(self)
          sprite_group.remove(rec)
          plyr.kill()
          wallbuild.kill()
          Wall.remove(self)
          wall=[]
          wallb.kill(self)


  def displaytext(self, text):
    pygame.font.init()
    font = pygame.font.SysFont('Terminal', 70)
    textsurface = font.render(text, False, (255, 255, 255))             #Font colour
    display.blit(textsurface, (150, 150))
        
    #Stop player moving out of screen BOTH GAMES:
    if self.rect.right > 590:
        self.rect.right = 590
    if self.rect.left < 10:
        self.rect.left = 10
    if self.rect.top < 10:
        self.rect.top = 10
    if self.rect.bottom > 390:
        self.rect.bottom = 390

# Import MOB(Alien):
class mob(pygame.sprite.Sprite):

  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    super(mob, self).__init__()
    #x = 36
    #y = 36
    
    self.image = pygame.image.load('mob1edit2.png').convert_alpha()
    #self.image = pygame.transform.scale(self.image, 25, 25)

    self.rect = self.image.get_rect()
    self.rect.centerx = x
    self.rect.bottom = y
    self.speed = 2
    self.counter = 0

  def update(self):

    if self.rect.bottom >= height-25:
      print("YOU. LOSE")
      self.displaytext("YOU LOSE")
      
    if self.rect.y < height/4:
      if self.counter % 20 == 0:
        self.rect.y += self.speed
      if self.counter == 0:
        self.rect.x += 50
      if self.counter == 100:
        self.rect.x -= 50
      self.counter += 1
      if self.counter == 200:
        self.counter = 0
    elif self.rect.y >= height/4:
      if self.counter % 40 == 0:
        self.rect.y += self.speed * 3
      if self.counter == 0:
        self.rect.x += 50
      if self.counter == 100:
        self.rect.x -= 50
      self.counter += 1
      if self.counter == 200:
        self.counter = 0

  def displaytext(self, text):
    pygame.font.init()
    font = pygame.font.SysFont('Terminal', 70)
    textsurface = font.render(text, False, (255, 255, 255)) #Font colour
    display.blit(textsurface, (150, 150))

#Bullet:
class bullet(pygame.sprite.Sprite):

  def __init__(self, x ,y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('bullet.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.bottom = y
    self.rect.centerx = x
    self.speedy = -7
    self.dir = os.path.dirname(__file__)

# Import sounds
  def sound(self, sound_name):
    #sound_dir = os.path.join(self.dir, 'sounds')
    pygame.mixer.init()
    return pygame.mixer.Sound(sound_name)

  def update(self):
    #Shoot bullet:
    self.rect.y += self.speedy
        
    if self.rect.bottom < 0:
      self.kill()

    #Check for collission Alien Vs Bullet:
    for each_alien in aliens:
      bullet_hits = each_alien.rect.colliderect(bullt.rect)
      if bullet_hits == True:
        #Play alien die sound:
        self.alien_die_sound = self.sound('fail.wav')
        self.alien_die_sound.play()
        #Kill the mob
        mobs.remove(each_alien)
        each_alien.kill()
        bullt.kill()


#TRON-ADVENTURE STYLE GAME IN THIS SECTION:
class Wall(pygame.sprite.Sprite):

  def __init__(self,pos):
    walls.append(self)
    self.rect = pygame.Rect(pos[0], pos[1], 23, 23)



# Import Recog(Tron):
class recog(pygame.sprite.Sprite):

  def __init__(self, x=450, y=100):
    pygame.sprite.Sprite.__init__(self)
    super(recog, self).__init__()
    
    self.image = pygame.image.load('recog.png').convert_alpha()

    self.rect = self.image.get_rect()
    self.rect.centerx = x
    self.rect.bottom = y
    self.speed = 2
    self.counter = 0

  def update(self):
    
    #Recog move towards player:
    dirvect = pygame.math.Vector2(plyr.rect.x - self.rect.x,
                                 plyr.rect.y - self.rect.y)
    try:
      dirvect.normalize()
      dirvect.scale_to_length(self.speed)
      self.rect.move_ip(dirvect)
      
    except:
      global lose
      lose = True
      #print("YOU. LOSE")
      rec.kill()
      plyr.kill()
      display.fill((0,0,0))
      self.displaytext("YOU LOSE")

  def displaytext(self, text):
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 70)
    textsurface = font.render(text, False, (255, 255, 255)) #Font colour
    display.blit(textsurface, (150, 150))


# Wall Builder:
class wallb(pygame.sprite.Sprite):

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    super(wallb, self).__init__()

    #Draw the walls etc
    for wall in walls:
      pygame.draw.rect(display, (255, 255, 255), wall.rect)
      pygame.draw.rect(display, (255, 0, 0), end_rect)

         
#LOADING SCREEN:
if loading == True:
  bg = pygame.image.load("loadings.png")
  display.blit(bg, (0, 0))
  pygame.display.flip()
  time.sleep(5)
  loading = False

#Run all the things (INVADERS):
plyr = player()
aliens=[]
aliens.append(mob(71,36)) #Width of mob: 73
aliens.append(mob(198, 36))
aliens.append(mob(325, 36))
aliens.append(mob(452, 36))
#Second Row:
aliens.append(mob(134,90))
aliens.append(mob(261, 90))
aliens.append(mob(388, 90))
mobs = aliens
sprite_group = pygame.sprite.Group()
sprite_group.add(plyr)
sprite_group.add(mobs)

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
  for col in row:
      if col == "W":
          Wall((x, y))
      if col == "E":
          end_rect = pygame.Rect(x, y, 25, 25)
      x += 23
  y += 23
  x = 0


Active = True
while Active:
    clock.tick(fps)
    
    for event in pygame.event.get():  # Wait for user.
        if event.type == pygame.QUIT:
            pygame.quit
            quit()
            #Shoot the bullets:
        elif event.type == pygame.KEYDOWN and len(mobs) != 0:
            if event.key == pygame.K_SPACE:
              current_bullet_time = pygame.time.get_ticks()
              if current_bullet_time  - previous_bullet_time > 500:
                previous_bullet_time = current_bullet_time
                bullt = bullet(plyr.rect.centerx, plyr.rect.top)
                sprite_group.add(bullt)
                #Play bullet sound:
                pygame.mixer.init()
                laser_sound = pygame.mixer.Sound('laser.wav')
                pygame.mixer.Sound.play(laser_sound)
        else:
            pass

  #Score / Timer:
    score_count = str(time.time() - startTime)
    
    #Update all the sprites:
    sprite_group.update()

    #Render to screen:
    sprite_group.draw(display)
    pygame.display.flip()

    #Update the background so we dont get ghost images:
    display.fill((0,0,0))

    if len(mobs) == 0 and win == False and lose == False:
      #RUN TRON-ADVENTURE:
      
      wallbuild = wallb()

      if game1 == False:
        #Stage 2 Load:
        bg = pygame.image.load("stage2.png")
        display.blit(bg, (0, 0))
        pygame.display.flip()
        time.sleep(2)
      
        rec = recog()
        sprite_group.add(rec)
        game1 = True
        
    if win == True:
        pygame.font.init()
        font = pygame.font.SysFont('Fixedsys Regular', 70)
        textsurface = font.render("YOU WIN", False, (255, 255, 255))             #Font colour
        display.blit(textsurface, (200, 150))
        
        #Play player win sound:
        if win_sound == False:
          pygame.mixer.init()
          player_win_sound = pygame.mixer.Sound('game_win.wav')
          pygame.mixer.Sound.play(player_win_sound)
          wintime = score_count
          #Record win time:
          win_sound = True
        pygame.font.init()
        font = pygame.font.SysFont('Terminal', 15)
        textsurface = font.render("Complete Time: " + str(round(float(wintime),2)) + " seconds", False, (255, 255, 255))             #Font colour
        display.blit(textsurface, (230, 220))
        pygame.display.flip()

    if lose == True:
        bg = pygame.image.load("lose.png")
        display.blit(bg, (0, 0))
        pygame.display.flip()
        #Play player died sound:
        if die_sound == False:
          pygame.mixer.init()
          player_die_sound = pygame.mixer.Sound('desc.wav')
          pygame.mixer.Sound.play(player_die_sound)
          die_sound = True


