

class CReadyLevel:
    def __init__(self, level_info:dict) -> None:
        
        self.player_showed = False
        self.level_info = level_info
        self.start_config()
        
    def start_config(self)->None:
        self.time_to_ready:int = self.level_info["time_to_ready"]
        self.time=0
        self.ready = False
        self.level = 1
        