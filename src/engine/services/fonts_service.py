
import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}
    
    def get(self, font: str, size : int) -> pygame.Surface:
        # Carga perezosa (En caso de no encontrarlo la carga y la retorna, de lo contrario la retorna de una vez)
        if font+str(size) not in self._fonts:
            self._fonts[font+str(size)] = pygame.font.Font(font, size)
        return self._fonts[font+str(size)]