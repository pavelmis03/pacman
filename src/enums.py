from enum import Enum


# Types of food in game
class FoodType(Enum):  # Class - enum. Need to recognize type of food object
    DOT = 1
    ENERGIZER = 2
    FRUIT = 3


# Types of behavior of ghosts
class GhostType:
    BLINKY = 'BLINKY'
    PINKY = 'PINKY'
    INKY = 'INKY'
    CLYDE = 'CLYDE'


# Types of behavior of ghosts
class GhostState(Enum):
    chase = 0
    scatter = 1
    eaten = 2
    frightened = 3
