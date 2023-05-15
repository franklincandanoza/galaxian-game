import pygame
import esper
import random

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar



def system_screen_star(world: esper.World, screen: pygame.Surface):
    scr_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagStar)
    
    c_t: CTransform
    c_s: CSurface
    
    for start_entity, (c_t, c_s, _) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        
        if random.randint(0, 1) == 0:
            alpha = 0
        else:
            alpha = 255
        c_s.surf.set_alpha(alpha)
        if not scr_rect.contains(bullet_rect):
            c_t.pos = pygame.Vector2(c_t.pos.x, 0)
