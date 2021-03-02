# stupid-game
A little pygame based game

# usage


_GUI (without arguments)_:
- Windows : download "game.exe" and just open it
- Unix and Windows : start game.py with python3


_conole (with arguments)_:
- $`python game.py single [bots]`
  - play in single mode with `[bots]` amount of bots to play with (default 3)

- $`python game.py host [port] [bots]`
  - to host your game on `[port]` (default 2281) with `[bots]` amount of bots (default 3)

- $`python game.py join [server] [port]`
  - to join a hosted game on `[server]` (default kemuri.ddns.net) on `[port]` (default 2281)

Under _default_ I mean if the argument is not given or is not in allowed range

# control

_gui control_:
- at the beginning :
  - K - download newest game repository
  - J - download latest executable release
- AD - left/right in switchers
- H - submit selection
- Q or close-Button - exit
- port selcetion : numbers allowed from numpad and keypad
- server selection : printable characters allowed, submission via enter-Button 

_game control_:
- WASD - typical movement
- LSHIFT ( left shift ) - run
- H - hit
- J - barrier
- K - magic
- Q or close-Button - exit
- after death : R - restart game with current options

# requirements for python script
- python 3.7 or higher
- newest pygame module

# installing executable
- go to releases
- download the desired version
  - if you want to run game.exe, all you need is Windows 7+
