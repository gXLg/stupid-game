import pygame
from time import sleep
from random import choice, randrange
from sys import argv

pygame.init ( )
window = pygame.display.set_mode ( ( 512, 512 ))

font = pygame.font.SysFont ( None, 24 )

colors = { }
try :
  for i in open ( "map/colorscheme" ).readlines ( ) : exec ( i )
except :
  colors [ 0 ] = ( 28, 37, 65, 0 )
  colors [ 1 ] = ( 58, 80, 107, 0 )
  colors [ 2 ] = ( 113, 128, 172, 0 )

  colors [ "air" ] = ( 232, 241, 242, 0 )
  colors [ "air_tired" ] = ( 51, 51, 51, 0 )
  colors [ "fire" ] = ( 215, 38, 61, 0 )
  colors [ "fire_tired" ] = ( 193, 102, 107, 0 )
  colors [ "water" ] = ( 68, 207, 108, 0 )
  colors [ "water_tired" ] = ( 86, 130, 89, 0 )

  colors [ "earth" ] = ( 26, 16, 9, 0 )
  colors [ "earth_tired" ] = ( 61, 59, 48, 0 )

game = [ ]
try :
  gamestr = open ( "map/game" ).read ( )
except :
  gamestr = """0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 2 1 2 1 2 1 2 1 2 1 2 1 2 0
0 2 1 1 1 1 1 2 1 2 1 1 1 2 1 0
0 1 2 2 2 1 2 1 2 1 1 1 2 1 2 0
0 2 1 2 2 2 1 2 1 2 1 1 1 2 1 0
0 1 2 1 2 1 2 1 2 1 2 1 1 1 2 0
0 2 1 1 2 1 1 2 1 2 1 1 1 2 1 0
0 1 2 1 2 1 1 1 2 1 2 1 2 1 2 0
0 2 1 2 1 1 1 1 1 2 1 2 1 2 1 0
0 1 2 1 1 1 2 1 2 1 2 1 2 1 2 0
0 2 1 2 1 2 1 1 1 1 1 1 1 2 1 0
0 2 2 1 2 1 2 1 2 1 1 1 2 1 2 0
0 2 2 2 1 2 1 1 1 2 1 2 1 2 1 0
0 2 2 2 2 1 2 1 2 1 2 1 2 1 2 0
0 2 2 2 2 2 2 2 1 2 1 2 1 2 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"""

for i in gamestr.split ( "\n" ) : game += eval ( "[[" + i.replace ( " ", "," ) + "]]" )

physics = { }
try :
  for i in open ( "map/physics" ).readlines ( ) : exec ( i )
except :
  solid = [ 0 ]
  air = [ 1, 2 ]

def draw_game ( ) :
  for y, i in enumerate ( game ) :
    for x, j in enumerate ( i ) :
      cords = ( x * 32, y * 32 )
      f = pygame.Rect ( cords [ 0 ], cords [ 1 ], 32, 32 )
      pygame.draw.rect ( window, colors [ j ], f )

clock = pygame.time.Clock ( )
pygame.display.set_caption ( "Stupid Game" )

try :
  single = ( argv [ 1 ] == "single" )
  host = ( argv [ 1 ] == "host" )
  join = ( argv [ 1 ] == "join" )
  if single :
    try : bots = int ( argv [ 2 ])
    except : bots = 3
  elif host :
    try : port = int ( argv [ 2 ])
    except : port = 2281
    try : bots = int ( argv [ 3 ])
    except : bots = 3
  elif join :
    server = argv [ 2 ]
    try : port = int ( argv [ 3 ])
    except : port = 2281
  else :
    error
except :
  print ( "Wrong args, trying GUI" )

  join = False
  host = False
  single = True

  menu_mode = "Singleplayer >"
  menu = True
  leave = False
  while menu :
    clock.tick ( 60 )
    for event in pygame.event.get ( ) :
      if event.type == pygame.QUIT :
        menu = False
        leave = True
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_a :
          menu_mode = "Singleplayer >"
          single = True
        elif event.key == pygame.K_d :
          menu_mode = "< Multiplayer"
          single = False
        elif event.key == pygame.K_h :
          menu = False
        elif event.key == pygame.K_q :
          menu = False
          leave = True
    draw_game ( )
    splash = font.render ( menu_mode, True, colors [ 0 ] )
    window.blit ( splash, ( 40, 40 ))
    pygame.display.flip ( )

  if leave :
    pygame.quit ( )
    quit ( )

  if not single :

    join = True
    host = False

    menu_mode = "Join >"
    menu = True
    leave = False
    while menu :
      clock.tick ( 60 )
      for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT :
          menu = False
          leave = True
        if event.type == pygame.KEYDOWN :
          if event.key == pygame.K_a :
            menu_mode = "Join >"
            join = True
            host = False
          elif event.key == pygame.K_d :
            menu_mode = "< Host"
            join = False
            host = True
          elif event.key == pygame.K_h :
            menu = False
          elif event.key == pygame.K_q :
            menu = False
            leave = True
      draw_game ( )
      splash = font.render ( menu_mode, True, colors [ 0 ] )
      window.blit ( splash, ( 40, 40 ))
      pygame.display.flip ( )
    if leave :
      pygame.quit ( )
      quit ( )
    if host :
      prompt = "Port to host your game (default 2281): "
      port = ""
      menu = True
      leave = False
      while menu :
        clock.tick ( 60 )
        for event in pygame.event.get ( ) :
          if event.type == pygame.QUIT :
            menu = False
            leave = True
          if event.type == pygame.KEYDOWN :
            if event.unicode.isdigit ( ) :
              port += event.unicode
            elif event.key == pygame.K_BACKSPACE :
              port = port [ : -1 ]
            elif event.key == pygame.K_h :
              menu = False
            elif event.key == pygame.K_q :
              menu = False
              leave = True
        draw_game ( )
        splash = font.render ( prompt + port, True, colors [ 0 ] )
        window.blit ( splash, ( 40, 40 ))
        pygame.display.flip ( )
      if port : port = int ( port )
      else : port = 2281
    else :
      prompt = "Server to connect to (default kemuri.ddns.net): "
      server = ""
      menu = True
      leave = False
      while menu :
        clock.tick ( 60 )
        for event in pygame.event.get ( ) :
          if event.type == pygame.QUIT :
            menu = False
            leave = True
          if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_BACKSPACE :
              server = server [ : -1 ]
            elif event.key == pygame.K_RETURN :
              menu = False
            elif event.unicode :
              server += event.unicode
        draw_game ( )
        splash = font.render ( prompt + server, True, colors [ 0 ] )
        window.blit ( splash, ( 40, 40 ))
        pygame.display.flip ( )
      if not server : server = "kemuri.ddns.net"
      if leave :
        pygame.quit ( )
        quit ( )
      prompt = "Port to connect your game (default 2281): "
      port = ""
      menu = True
      leave = False
      while menu :
        clock.tick ( 60 )
        for event in pygame.event.get ( ) :
          if event.type == pygame.QUIT :
            menu = False
            leave = True
          if event.type == pygame.KEYDOWN :
            if event.unicode.isdigit ( ) :
              port += event.unicode
            if event.key == pygame.K_BACKSPACE :
              port = port [ : -1 ]
            if event.key == pygame.K_h :
              menu = False
            if event.key == pygame.K_q :
              menu = False
              leave = True
        draw_game ( )
        splash = font.render ( prompt + port, True, colors [ 0 ] )
        window.blit ( splash, ( 40, 40 ))
        pygame.display.flip ( )
      if port : port = int ( port )
      else : port = 2281

  if leave :
    pygame.quit ( )
    quit ( )

  if not join :
    bots = 3
    menu = True
    while menu :
      clock.tick ( 60 )
      for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT :
          menu = False
          leave = True
        if event.type == pygame.KEYDOWN :
          if event.key == pygame.K_a :
            if bots > 0 : bots -= 1
          if event.key == pygame.K_d :
            if bots < 20 : bots += 1
          if event.key == pygame.K_h :
            menu = False
      draw_game ( )
      splash = font.render ( "Number of bots in the game: - " + str ( bots ) + " +", True, colors [ 0 ] )
      window.blit ( splash, ( 40, 40 ))
      pygame.display.flip ( )

  if leave :
    pygame.quit ( )
    quit ( )

if host : from multiprocessing.connection import Listener
elif join : from multiprocessing.connection import Client

pygame.display.set_caption ( "Stupid Game" + ( " (Multiplayer)" if not single else "" ))

class Entity :

  def __init__ ( self, element = "air", x = 256, y = 256, type = "bot" ) :
    self.element = element
    self.body = pygame.Rect ( x, y, 32, 32 )
    self.energy = pygame.Rect ( x, y, 32, 32 )
    self.cooldown = 300
    self.type = type

  def move ( self, player_ = None, knockback = 1, controller = False ) :

    if self.type == "player" and controller :
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
      if single :
        player_ = player
      elif player_ :
        pass
      elif ( player.body.x - self.body.x ) ** 2 + ( player.body.y - self.body.y ) ** 2 < ( player2.body.x - self.body.x ) ** 2 + ( player2.body.y - self.body.y ) ** 2 :
        player_ = player
      else :
        player_ = player2
      rx = player_.body.x - self.body.x
      ry = player_.body.y - self.body.y
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
    for i in entities + [ player ] + ( [ player2 ] if not single else [ ]) :
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
    for i in entities + [ player ] + ( [ player2 ] if not single else [ ]) :
      if i == self : continue
      if ( ( ( self.body.x - i.body.x ) ** 2 + ( self.body.y - i.body.y ) ** 2 ) ** 0.5 ) < 80 :
        i.move ( player_ = self, knockback = -32 )

  def hit ( self ) :
    self.cooldown -= 10
    for i in entities + [ player ] + ( [ player2 ] if not single else [ ]) :
      if i == self : continue
      if ( ( ( self.body.x - i.body.x ) ** 2 + ( self.body.y - i.body.y ) ** 2 ) ** 0.5 ) < 44.8 :
        i.move ( player_ = self, knockback = -16 )
        i.cooldown -= 10

  def magic ( self ) :
    self.cooldown -= 80
    low_objects.append ( Object ( self.body.center, radius = 64, color = colors [ self.element ], type = "filled_circle", cooldown = 240, maxcooldown = 120 ))

  def attack ( self ) :
    for player_ in [ player ] + ( [ player2 ] if not single else [ ]) :
      if ( ( ( self.body.x - player_.body.x ) ** 2 + ( self.body.y - player_.body.y ) ** 2 ) ** 0.5 ) < 38.4 :
        e = self.element
        p = player_.element
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
        player_.cooldown -= dmg

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

  def draw ( self, nor = True ) :
    percentage = int ( 32 * self.cooldown / 300 )
    self.energy.height = 32 - percentage
    pygame.draw.rect ( window, colors [ self.element ], self.body )
    pygame.draw.rect ( window, colors [ self.element + "_tired" ], self.energy )
    pygame.draw.rect ( window, colors [ self.element + "_tired" ], self.body, 3 )
    small = ( self.body.x + 8, self.body.y + 8, 16, 16 )
    if self.type == "player" : pygame.draw.rect ( window, colors [ self.element + "_tired" ], small, 3 if nor else 0 )

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
    #s.set_alpha ( 255 )
    if "circle" in self.type :
      pygame.draw.circle ( s, self.color, self.cords, self.radius, 0 if self.type == "filled_circle" else 2 )
    elif "text" in self.type :
      num = font.render ( self.value, True, self.color )
      s.blit ( num, self.cords )
    window.blit ( s, ( 0, 0 ))
    self.cooldown -= 1

def new ( ) :
  random = randrange ( 100 )
  entities.append ( Entity ( x = randrange ( 32, 480 ), y = randrange ( 32, 480 ),
                             element = choice ( [ "fire", "air", "earth", "water" ])))

if host :
  try :
    server_sock = Listener ( ( "localhost", port ))
  except :
    print ( "Could not host game" )
    pygame.quit ( )
    quit ( )

play = True
while play :
  draw_game ( )
  waiting = font.render ( "Waiting for connection..", True, colors [ 0 ] )
  window.blit ( waiting, ( 160, 250 ))
  pygame.display.flip ( )
  if host :
    conn = server_sock.accept ( )
  if join :
    try :
      client = Client ( ( server, port ))
    except :
      print ( "Could not connect" )
      pygame.quit ( )
      quit ( )
  run = True
  kills = 0
  kills2 = 0
  if single : player = Entity ( type = "player", element = choice ( [ "fire", "air", "earth", "water" ]))
  else :
    player = Entity ( x = 40, y = 40, type = "player", element = choice ( [ "fire", "air", "earth", "water" ]))
    random = randrange ( 100 )
    player2 = Entity ( y = 420, x = 420, type = "player", element = choice ( [ "fire", "air", "earth", "water" ]))
  entities = [ ]
  low_objects = [ ]
  top_objects = [ ]
  if not join : [ new ( ) for i in range ( bots )]
  frame = 0
  while run :
    pygame.display.set_icon ( window )

    if join :
      var = client.recv ( )
      player = var [ "player" ]
      player2 = var [ "player2" ]
      entities = var [ "entities" ]
      low_objects = var [ "low_objects" ]
      top_objects = var [ "top_objects" ]
      run = var [ "run" ]
      kills = var [ "kills" ]
      kills2 = var [ "kills2" ]


    if not join :
      frame = ( frame + 1 ) % 60
      clock.tick ( 60 )

    health = { }
    for i in entities + [ player ] + ( [ player2 ] if not single else [ ]) :
      health [ i ] = i.cooldown

    for event in pygame.event.get ( ) :
      if event.type == pygame.QUIT :
        run = False
      if join : player_ = player2
      else : player_ = player
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_h :
          player_.hit ( )
        if event.key == pygame.K_j :
          player_.push ( )
        if event.key == pygame.K_k :
          player_.magic ( )

    keys = pygame.key.get_pressed ( )
    if not join and player.cooldown <= 0 : run = False
    if host and player2.cooldown <= 0 : run = False
    if not join and keys [ pygame.K_q ] : run = False

    if not frame % 4 and not join :
      for i in entities + [ player ] + ( [ player2 ] if not single else [ ]) : i.dmg ( )
      for i in entities : i.attack ( )

    if not join : player.move ( controller = True )
    else : player2.move ( controller = True )
    if not frame % 2 and not join:
      for i in entities : i.move ( )

    for i in health :
      value = i.cooldown - health [ i ]
      if value < 0 : top_objects.append ( Object ( i.body.center, color = colors [ i.element ], cooldown = 30, type = "text", value = str ( round ( value ))))

    if not join :
      removed = [ ]
      for i in entities :
        if i.cooldown <= 0 : removed.append ( i )
      for i in removed :
        entities.remove ( i )
        if single :
          player_ = player
          kills += 1
        elif ( player.body.x - i.body.x ) ** 2 + ( player.body.y - i.body.y ) ** 2 < ( player2.body.x - i.body.x ) ** 2 + ( player2.body.y - i.body.y ) ** 2 :
          player_ = player
          kills += 1
        else :
          player_ = player2
          kills2 += 1
        player_.element = i.element
        player_.cooldown = 300
        new ( )

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

    if join :
      var = { "player" : player, "player2" : player2, "entities" : entities, "low_objects" : low_objects, "top_objects" : top_objects }
      client.send ( var )

    window.fill ( 0 )
    draw_game ( )
    for i in low_objects : i.draw ( )
    for i in entities : i.draw ( )
    if host :
      player.draw ( )
      player2.draw ( nor = False )
    elif join :
      player2.draw ( )
      player.draw ( nor = False )
    else :
      player.draw ( )
    for i in top_objects : i.draw ( )
    pygame.display.flip ( )

    if host :
      var = { "player" : player, "player2" : player2, "entities" : entities, "low_objects" : low_objects,
              "top_objects" : top_objects, "run" : run, "kills" : kills, "kills2" : kills2 }
      conn.send ( var )
      var = conn.recv ( )
      player = var [ "player" ]
      player2 = var [ "player2" ]
      entities = var [ "entities" ]
      low_objects = var [ "low_objects" ]
      top_objects = var [ "top_objects" ]

  if host : conn.close ( )
  if join : client.close ( )
  draw_game ( )
  if host :
    gg = font.render ( "You - Health: " + str ( player.cooldown ) + " Kills: " + str ( kills ), True, colors [ 0 ] )
    window.blit ( gg, ( 40, 430 ))
    gg = font.render ( "Opponent - Health: " + str ( player2.cooldown ) + " Kills: " + str ( kills2 ), True, colors [ 0 ] )
    window.blit ( gg, ( 40, 450 ))
  elif join :
    gg = font.render ( "You - Health: " + str ( player2.cooldown ) + " Kills: " + str ( kills2 ), True, colors [ 0 ] )
    window.blit ( gg, ( 40, 430 ))
    gg = font.render ( "Opponent - Health: " + str ( player.cooldown ) + " Kills: " + str ( kills ), True, colors [ 0 ] )
    window.blit ( gg, ( 40, 450 ))
  else :
    gg = font.render ( "Health: " + str ( player.cooldown ) + " Kills: " + str ( kills ), True, colors [ 0 ] )
    window.blit ( gg, ( 40, 430 ))
  pygame.display.flip ( )
  x = True
  while x :
    for event in pygame.event.get ( ) :
        if event.type == pygame.QUIT :
          x = False
          play = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q :
            play = False
            x = False
          if event.key == pygame.K_r :
            run = True
            x = False
pygame.quit ( )
quit ( )
