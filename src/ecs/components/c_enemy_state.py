from enum import Enum
import pygame


class CEnemyState:
    def __init__(self, start_pos: pygame.Vector2):
        self.state = EnemyState.IDLE
        self.start_pos = pygame.Vector2(start_pos.x, start_pos.y)
        self.chase_sound_channel = None


class EnemyState(Enum):
    IDLE = 0
    ATTACKING = 1
