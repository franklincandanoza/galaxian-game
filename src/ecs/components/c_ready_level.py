

class CReadyLevel:
    def __init__(self, level_info:dict) -> None:
        
        self.time_to_ready:int = level_info["time_to_ready"]
        self.time=0
        self.ready = False