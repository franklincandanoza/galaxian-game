import pygame
class CTagEnemyNew:
    def __init__(self, enemy_type: str, original_position : pygame.Vector2) -> None:
        self.enemy_type = enemy_type
        self.original_position = original_position
