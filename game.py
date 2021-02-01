import pygame
from time import sleep
from random import choice, randrange

pygame.init ( )

window = pygame.display.set_mode ( ( 512, 512 ))
pygame.display.set_caption ( "Stupid Game" )

clock = pygame.time.Clock ( )

font = pygame.font.SysFont ( None, 24 )

colors = { }
for i in open ( "map/colorscheme" ).readlines ( ) : exec ( i )

game = [ ]
for i in open ( "map/game" ).readlines ( ) : game += eval ( "[[" + i.replace ( " ", "," ) + "]]" )

physics = { }
for i in open ( "map/physics" ).readlines ( ) : exec ( i )

class Entity :

  def __init__ ( self, element = "air", x = 256, y = 256, type = "bot" ) :
    self.element = element
    self.body = pygame.Rect ( x, y, 32, 32 )
    self.energy = pygame.Rect ( x, y, 32, 32 )
    self.cooldown = 300
    self.type = type

  def move ( self, player, knockback = 1 ) :

    if self.type == "player" :
      keys = pygame.key.get_pressed ( )

      dx = ( keys [ pygame.K_d ] - keys [ pygame.K_a ])
      dy = ( keys [ pygame.K_s ] - keys [ pygame.K_w ])

      if keys [ pygame.K_LSHIFT ] and self.cooldown > 0 and ( dx or dy ) :
        dx *= 2
        dy *= 2
        self.cooldown -= 1
      else :
        if self.cooldown < 300 : self.cooldown += 0.25
        else : self.cooldown = 300

    else :
      rx = player.body.x - self.body.x
      ry = player.body.y - self.body.y
      dx = 0 if not rx else int ( abs ( rx ) / rx )
      dy = 0 if not ry else int ( abs ( ry ) / ry )

    dx *= knockback
    dy *= knockback

    rx = ( self.body.centerx + dx ) // 32
    ry = ( self.body.centery + dy ) // 32

    if not 0 < rx < 16 : rx = dx = 0
    if not 0 < ry < 16 : ry = dy = 0

    if game [ self.body.centery // 32 ] [ int ( rx )] in solid : dx = 0
    if game [ int ( ry )] [ self.body.centerx // 32 ] in solid : dy = 0

    cx = cy = False
    for i in entities + [ player ] * ( self.type != "player" ) :
      if i == self : continue
      if ( ( ( self.body.x + dx - i.body.x ) ** 2 + ( self.body.y - i.body.y ) ** 2 ) ** 0.5 ) < 32 : cx = True
      if ( ( ( self.body.x - i.body.x ) ** 2 + ( self.body.y + dy - i.body.y ) ** 2 ) ** 0.5 ) < 32 : cy = True
    if cx : dx = 0
    if cy : dy = 0

    self.body.x += dx
    self.body.y += dy
    self.energy.x += dx
    self.energy.y += dy

  def push ( self ) :
    self.cooldown -= 20
    low_objects.append ( Object ( self.body.center, radius = 64 ))
    for i in entities + [ player ] * ( self.type != "player" ) :
      if i == self : continue
      if ( ( ( self.body.x - i.body.x ) ** 2 + ( self.body.y - i.body.y ) ** 2 ) ** 0.5 ) < 80 :
        i.move ( player, knockback = -32 )

  def hit ( self ) :
    self.cooldown -= 10
    for i in entities + [ player ] * ( self.type != "player" ) :
      if i == self : continue
      if ( ( ( self.body.x - i.body.x ) ** 2 + ( self.body.y - i.body.y ) ** 2 ) ** 0.5 ) < 44.8 :
        i.move ( player, knockback = -16 )
        i.cooldown -= 10

  def magic ( self ) :
    self.cooldown -= 80
    low_objects.append ( Object ( self.body.center, radius = 64, color = colors [ self.element ], type = "filled_circle", cooldown = 240, maxcooldown = 120 ))

  def attack ( self ) :
    if ( ( ( self.body.x - player.body.x ) ** 2 + ( self.body.y - player.body.y ) ** 2 ) ** 0.5 ) < 38.4 :
      e = self.element
      p = player.element
      if p == e : dmg = 1
      if p == "fire" :
        if e == "water" : dmg = 4
        else : dmg = 2
      if p == "air" :
        if e == "fire" : dmg = 4
        else : dmg = 2
      if p == "earth" :
        if e == "air" : dmg = 4
        else : dmg = 2
      if p == "water" :
        if e == "earth" : dmg = 4
        else : dmg = 2
      player.cooldown -= dmg

  def dmg ( self ) :
    for i in low_objects :
      if ( ( ( self.body.centerx - i.cords [ 0 ]) ** 2 + ( self.body.centery - i.cords [ 1 ]) ** 2 ) ** 0.5 ) <= 64 :
        c = i.color
        e = self.element
        if c == colors [ 0 ] : dmg = 0
        if c == colors [ e ] : dmg = 0
        if e == "fire" :
          if c == colors [ "water" ] : dmg = 4
          if c == colors [ "air" ] : dmg = -1
          if c == colors [ "earth" ] : dmg = 2
        if e == "air" :
          if c == colors [ "fire" ] : dmg = 4
          if c == colors [ "earth" ] : dmg = -1
          if c == colors [ "water" ] : dmg = 2
        if e == "earth" :
          if c == colors [ "air" ] : dmg = 4
          if c == colors [ "water" ] : dmg = -1
          if c == colors [ "fire" ] : dmg = 2
        if e == "water" :
          if c == colors [ "earth" ] : dmg = 4
          if c == colors [ "fire" ] : dmg = -1
          if c == colors [ "air" ] : dmg = 2
        self.cooldown -= dmg

  def draw ( self ) :
    percentage = int ( 32 * self.cooldown / 300 )
    self.energy.height = 32 - percentage
    pygame.draw.rect ( window, colors [ self.element ], self.body )
    pygame.draw.rect ( window, colors [ self.element + "_tired" ], self.energy )
    #pygame.draw.rect ( window, colors [ self.element + "_tired" ], self.body, width = 3 )
    pygame.draw.rect ( window, colors [ self.element + "_tired" ], self.body, 3 )
    small = ( self.body.x + 8, self.body.y + 8, 16, 16 )
    #if self.type == "player" : pygame.draw.rect ( window, colors [ self.element + "_tired" ], small, width = 3 )
    if self.type == "player" : pygame.draw.rect ( window, colors [ self.element + "_tired" ], small, 3 )

class Object :

  def __init__ ( self, cords, radius = None, color = colors [ 0 ], cooldown = 30, maxcooldown = None, type = "circle", value = None ) :
    self.cooldown = cooldown
    self.cords = cords
    self.radius = radius
    self.color = color
    self.type = type
    self.value = value
    self.maxcooldown = maxcooldown if maxcooldown else cooldown

  def draw ( self ) :
    s = pygame.Surface ( ( 512, 512 ))
    s.set_colorkey ( 0 )
    s.set_alpha ( 255 * min ( 1, self.cooldown / self.maxcooldown ))
    if "circle" in self.type :
      #pygame.draw.circle ( s, self.color, self.cords, self.radius, width = 0 if self.type == "filled_circle" else 2 )
      pygame.draw.circle ( s, self.color, self.cords, self.radius, 0 if self.type == "filled_circle" else 2 )
    elif "text" in self.type :
      num = font.render ( self.value, True, self.color )
      s.blit ( num, self.cords )
    window.blit ( s, ( 0, 0 ))
    self.cooldown -= 1

def draw_game ( ) :
  for y, i in enumerate ( game ) :
    for x, j in enumerate ( i ) :
      cords = ( x * 32, y * 32 )
      f =  pygame.Rect ( cords [ 0 ], cords [ 1 ], 32, 32 )
      pygame.draw.rect ( window, colors [ j ], f )

def new ( ) :
  random = randrange ( 100 )
  entities.append ( Entity ( x = randrange ( 32, 480 ), y = randrange ( 32, 480 ),
                             element = choice ( [ "fire", "air", "earth", "water" ])))

play = True
while play :
  run = True
  kills = 0
  player = Entity ( type = "player", element = choice ( [ "fire", "air", "earth", "water" ]))
  entities = [ ]
  low_objects = [ ]
  top_objects = [ ]
  new ( )
  new ( )
  new ( )
  frame = 0
  while run :
    pygame.display.set_icon ( window )
    frame = ( frame + 1 ) % 60
    clock.tick ( 60 )

    health = { }
    for i in entities + [ player ] :
      health [ i ] = i.cooldown

    for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT :
          run = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_h :
            player.hit ( )
          if event.key == pygame.K_j :
            player.push ( )
          if event.key == pygame.K_k :
            player.magic ( )
    keys = pygame.key.get_pressed ( )
    if player.cooldown <= 0 : run = False
    if keys [ pygame.K_q ] : run = False

    if not frame % 4 :
      for i in entities + [ player ] : i.dmg ( )
      for i in entities : i.attack ( )

    player.move ( None )
    if not frame % 2 :
      for i in entities : i.move ( player )

    for i in health :
      value = i.cooldown - health [ i ]
      if value < 0 : top_objects.append ( Object ( i.body.center, color = colors [ i.element ], cooldown = 30, type = "text", value = str ( round ( value ))))

    removed = [ ]
    for i in entities :
      if i.cooldown <= 0 : removed.append ( i )
    for i in removed :
      entities.remove ( i )
      player.element = i.element
      player.cooldown = 300
      new ( )
      kills += 1

    removed = [ ]
    for i in low_objects :
      if i.cooldown <= 0 : removed.append ( i )
    for i in removed :
      low_objects.remove ( i )

    removed = [ ]
    for i in top_objects :
      if i.cooldown <= 0 : removed.append ( i )
    for i in removed :
      top_objects.remove ( i )

    window.fill ( 0 )
    draw_game ( )
    for i in low_objects : i.draw ( )
    for i in entities : i.draw ( )
    player.draw ( )
    for i in top_objects : i.draw ( )
    pygame.display.flip ( )

  draw_game ( )
  pygame.display.flip ( )
  print ( kills )
  x = True
  while x :
    for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT : x = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q :
            play = False
            x = False
          if event.key == pygame.K_r :
            run = True
            x = False
pygame.quit ( )
exit ( )
