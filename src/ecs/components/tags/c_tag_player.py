class CTagPlayer:
    def __init__(self, dead_enemies: int =0, lifes: int = 0) -> None:
        self.dead_enemies = dead_enemies
        self.level = 1
        self.original_lifes = lifes
        self.current_lifes = lifes
        self.score = 0
