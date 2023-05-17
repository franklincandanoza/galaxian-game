
class CTagPauseMessage:
    def __init__(self,pause_conf:dict) -> None:
        self.time_show = pause_conf["time_show"]
        self.time_hide =pause_conf["time_hide"]
        self.current_time=0
        self.is_showing = False
        
        
        
        
