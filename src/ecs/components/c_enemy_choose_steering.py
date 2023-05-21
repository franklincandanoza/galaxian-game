

class CEnemyChooseSteering:
    def __init__(self,enemy_steering_dict:dict) -> None:
 
        self.time_steering = enemy_steering_dict["enemy_steering"]["time_steering"]
        self.enemies_to_steering_min = enemy_steering_dict["enemy_steering"]["enemies_to_steering"]["min"]
        self.enemies_to_steering_max = enemy_steering_dict["enemy_steering"]["enemies_to_steering"]["max"]
        self.current_time = 0 