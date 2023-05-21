import pygame
import esper

from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew

def system_steering_draw_debug(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSteering)
    for _, (c_t, c_bs) in components:
        # Draw vectors for debugging
        final_vector = c_bs.follow_vector + c_bs.gravity_vector
        pygame.draw.line(screen, pygame.Color(0, 255, 0), c_t.pos, c_t.pos + c_bs.follow_vector)
        pygame.draw.line(screen, pygame.Color(255, 0, 0), c_t.pos, c_t.pos + c_bs.gravity_vector)
        pygame.draw.line(screen, pygame.Color(255, 255, 255), c_t.pos, c_t.pos + final_vector)
        
    components = world.get_components(CTransform, CTagEnemyNew,CSurface)
    for _, (c_t, c_te,c_s) in components:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        pygame.draw.rect(screen,pygame.Color(200, 200, 200),ene_rect)