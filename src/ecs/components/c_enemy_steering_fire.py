import random

class CEnemySteeringFire:
    def __init__(self,enemy_steering_fire_dict:dict) -> None:
        self.bullets = random.randrange(enemy_steering_fire_dict["bullets"]["min"],enemy_steering_fire_dict["bullets"]["max"]) 
        self.current_bullets = self.bullets
        self.time_to_fire = random.uniform(enemy_steering_fire_dict["time_to_fire"]["min"], enemy_steering_fire_dict["time_to_fire"]["max"])
        self.time_between_bullets = enemy_steering_fire_dict["time_between_bullets"]
        self.current_time = 0
        self.bullet_current_time = 0
        
    