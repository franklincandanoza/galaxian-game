class CTagPlayer:
    def __init__(self, dead_enemies: int =0, lifes: int = 0) -> None:
        self.dead_enemies = dead_enemies
        self.level = 1
        self.original_lifes = lifes
        self.current_lifes = lifes
        self.score = 0
        
    def restart_score(self)->None:
        self.score = 0
        
    def discount_life(self)->None:
        self.current_lifes -=1
        if self.current_lifes == 0:
            self.level = 1
            self.score = 0
            self.current_lifes = self.original_lifes