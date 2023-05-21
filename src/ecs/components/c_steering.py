import pygame

import enum
class State(enum.Enum):
    STEERING="STEERING",
    RETURNING="RETURNING"

class CSteering:
    def __init__(self) -> None:
        self.follow_vector:pygame.Vector2 = pygame.Vector2(0, 0)
        self.gravity_vector:pygame.Vector2 = pygame.Vector2(0,100)
        self.current_time=0
        self.time_to_recalcule=0.8
