import pygame

class CEnemySpawnerNew:
    def __init__(self, enemies:dict) -> None:
        self.current_time:float = 0
        self.spawn_event_data:list[SpawnEventDataNew] = []
        for single_enemy_configuration in enemies:
            self.spawn_event_data.append(SpawnEventDataNew(single_enemy_configuration))

class SpawnEventDataNew:
    def __init__(self, event_data:dict) -> None:
        self.type:str = event_data["enemy_type"]
        self.quantity:str =  event_data["quantity"]
        self.quantity_by_line:str =  event_data["quantity_by_line"]
        self.triggered = False