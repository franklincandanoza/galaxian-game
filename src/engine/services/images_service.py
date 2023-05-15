
import pygame

class ImagesService:
    def __init__(self) -> None:
        self._images = {}
    
    def get(self, path: str) -> pygame.Surface:
        # Carga perezosa (En caso de no encontrarlo la carga y la retorna, de lo contrario la retorna de una vez)
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]