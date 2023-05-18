import pygame
class CTagEnemyNew:
    def __init__(self, enemy_type: str, original_position : pygame.Vector2, enemy_score: int) -> None:
        self.enemy_type = enemy_type
        self.enemy_score = enemy_score
        self.original_position = original_position
