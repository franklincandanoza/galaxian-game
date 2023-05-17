
class CEnemyBasicFire:
    def __init__(self, enemy_basic_fire:dict) -> None:
        
        self.frequency_fire:int = enemy_basic_fire["frequency"]
        self.bullets = enemy_basic_fire["bullets"]["min"],enemy_basic_fire["bullets"]["max"]
        self.time=0