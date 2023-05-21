import pygame

class CSteering:
    def __init__(self, enemy_steering_info:dict) -> None:
        self.follow_vector:pygame.Vector2 = pygame.Vector2(0, 0)
        self.gravity_vector:pygame.Vector2 = pygame.Vector2(0,enemy_steering_info["gravity"])
        self.current_time=0
        self.time_to_recalcule=enemy_steering_info["time_to_recalcule"]
 