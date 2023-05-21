import pygame

import enum
class State(enum.Enum):
    STEERING="STEERING",
    RETURNING="RETURNING"

class CSteeringState:
    def __init__(self,original_pos:pygame.Vector2) -> None:
        self.state = State.STEERING
        self.original_pos = original_pos 