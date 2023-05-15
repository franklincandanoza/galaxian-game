import pygame

class SoundsService:
    def __init__(self) -> None:
        self._sounds : dict[str, pygame.mixer.Sound]= {}
        
    def play(self, path: str)-> None:
        # Carga perezosa (En caso de no encontrarlo la carga y la retorna, de lo contrario la retorna de una vez)
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        self._sounds[path].play()